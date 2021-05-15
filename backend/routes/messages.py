from datetime import datetime
from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required
from flask_socketio import emit
from socketio.exceptions import SocketIOError
from sqlalchemy import and_, desc, or_
from werkzeug.exceptions import BadRequest, Forbidden

from app import socketio
from models import db, Connection, Message


message_routes = Blueprint("message_routes", __name__, url_prefix="/api/v1/connections")


# POST https://surprise-me.benbolt.house/api/v1/connections/<connection_id>/messages
# Creates a new message for the given connection and handles emitting the
# message to connected parties.
@message_routes.route("/<connection_id>/messages", methods=["POST"])
@login_required
def post(connection_id):
    get = request.json.get

    body = get("body")

    connection = Connection.query.filter(
        and_(
            or_(
                Connection.requestor_id == current_user.id,
                Connection.approver_id == current_user.id),
            Connection.id == int(connection_id))).first()

    # handle bad requests for non-member users
    if not connection:
        raise BadRequest(response={
            "notification": {
                "body": "You cannot send a message to this user.",
                "type": "popup_notifications",
                "delay": 3,
            },
        })

    other_user = connection.other_user(current_user.id)
    recipient_id = other_user.id

    message = Message()
    message.connection_id = int(connection_id)
    message.sender_id = current_user.id
    message.recipient_id = recipient_id
    message.body = body

    notification = Notification()
    notification.recipient_id = recipient_id
    notification.type = "message"
    notification.body = body,
    notification.action = f"/#/connections/{connection.id}"

    db.session.add(message)
    db.session.add(notification)
    db.session.commit()

    # emit to user's message room
    socketio.emit("deliver_message", {
        "data": message.to_dict(),
        "notification": {
            "body": {
                "sender_name": current_user.first_name,
                "sender_id": current_user.id,
                "message": body,
            },
            "action": f"/#/connections/{connection_id}/messages",
            "type": "message_notifications",
            "delay": 3,
        },
    }, to=f"message_{recipient_id}")

    return jsonify({
        "data": message.to_dict(),
    }), 201


# GET https://surprise-me.benbolt.house/api/v1/connections/<connection_id>/messages
# Retrieves a set and offset quantity of messages based on url queries.
@message_routes.route("/<connection_id>/messages", methods=["GET"])
@login_required
def get(connection_id):
    offset = request.args.get("ofs")
    limit = request.args.get("lim")

    # handle bad requests for poorly-formatted requests
    if not offset or not limit:
        raise BadRequest()

    connection = Connection.query.filter(
        and_(
            or_(
                Connection.requestor_id == current_user.id,
                Connection.approver_id == current_user.id),
            Connection.id == int(connection_id))).first()

    # handle bad requests for non-member users
    if not connection or connection.is_deleted:
        raise Forbidden(response={
            "notification": {
                "body": "This connection no longer exists.",
                "type": "popup_notifications",
                "delay": 3,
            },
        })

    # get offset limit of messages and format for json response
    messages = Message.query.filter(Message.connection_id == int(connection_id))\
        .order_by(Message.id.desc())\
        .offset(offset)\
        .limit(limit)\
        .all()

    messages = [x.to_dict() for x in messages]

    return jsonify({
        "data": messages,
    }), 200


# PATCH https://surprise-me.benbolt.house/api/v1/connections/<connection_id>/messages/<id>
# Updates a specific message for the given connection and handles emitting the
# message to connected parties.
@message_routes.route("/<connection_id>/messages/<id>", methods=["PATCH"])
@login_required
def patch(connection_id, id):
    get = request.json.get

    body = get("body")

    connection = Connection.query.filter(
        and_(
            or_(
                Connection.requestor_id == current_user.id,
                Connection.approver_id == current_user.id),
            Connection.id == int(connection_id))).first()

    # handle bad requests for non-member users
    if not connection or connection.is_deleted:
        raise BadRequest(response={
            "notification": {
                "body": "This connection no longer exists.",
                "type": "popup_notifications",
                "delay": 3,
            },
        })

    other_user = connection.other_user(current_user.id)
    recipient_id = other_user.id

    message = Message.query.filter(
        and_(
            Message.id == int(id),
            Message.connection_id == int(connection_id),
            Message.sender_id == current_user.id)).first()

    # handle requests for non-existend messages
    if not message or message.is_deleted:
        raise BadRequest()

    message.update(body=body)

    db.session.commit()

    # emit to user's message room
    socketio.emit("amend_message", {
        "data": message.to_dict(),
    }, to=f"message_{recipient_id}")

    return jsonify({
        "data": message.to_dict(),
    }), 201


# DELETE https://surprise-me.benbolt.house/api/v1/connections/<connection_id>/messages/<id>
# Deletes a specific message for the given connection and handles emitting
# the update to connected parties.
@message_routes.route("/<connection_id>/messages/<id>", methods=["DELETE"])
@login_required
def delete(connection_id, id):
    connection = Connection.query.filter(
        and_(
            or_(
                Connection.requestor_id == current_user.id,
                Connection.approver_id == current_user.id),
            Connection.id == int(connection_id))).first()

    # handle bad requests for non-member users
    if not connection or connection.is_deleted:
        raise BadRequest(response={
            "notification": {
                "body": "This connection no longer exists.",
                "type": "popup_notifications",
                "delay": 3,
            },
        })

    other_user = connection.other_user(current_user.id)
    recipient_id = other_user.id

    message = Message.query.filter(
        and_(
            Message.id == int(id),
            Message.connection_id == int(connection_id),
            Message.sender_id == current_user.id)).first()

    # handle requests for non-existend messages
    if not message or message.is_deleted:
        raise BadRequest(response={
            "notification": {
                "body": "This message no longer exists.",
                "type": "popup_notifications",
                "delay": 3,
            },
        })

    message.set_deleted_at()

    db.session.commit()

    # emit to user's message room
    socketio.emit("discard_message", {
        "data": message.to_deleted_dict(),
    }, to=f"message_room_{recipient_id}")

    return jsonify({
        "data": message.to_deleted_dict(),
    }), 201
