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
            "message": "User not connected to recipient user",
        })

    other_user = connection.other_user(current_user.id)
    recipient_id = other_user.id

    message_room_name = f"message_room_{recipient_id}"

    message = Message(int(connection_id), current_user.id, recipient_id, body)

    db.session.add(message)
    db.session.commit()

    response = {
        "message": "Success",
        "data": {
            "connection_id": int(connection_id),
            "messages": [message.to_dict()],
        }
    }

    # emit to user's message room
    socketio.emit("deliver_message", response, to=message_room_name)

    return jsonify(response), 201


# GET https://surprise-me.benbolt.house/api/v1/connections/<connection_id>/messages
# Retrieves a set and offset quantity of messages based on url queries.
@message_routes.route("/<connection_id>/messages", methods=["GET"])
@login_required
def get(connection_id):
    offset = request.args.get("ofs")
    limit = request.args.get("lim")

    # handle bad requests for poorly-formatted requests
    if not offset or not limit:
        raise BadRequest(response={
            "message": "Missing request args"
        })

    connection = Connection.query.filter(
        and_(
            or_(
                Connection.requestor_id == current_user.id,
                Connection.approver_id == current_user.id),
            Connection.id == int(connection_id))).first()

    # handle bad requests for non-member users
    if not connection or connection.is_deleted:
        raise Forbidden(response={
            "message": "User not member",
        })

    # get offset limit of messages and format for json response
    messages = Message.query.filter(Message.connection_id == int(connection_id))\
        .order_by(Message.id.desc())\
        .offset(offset)\
        .limit(limit)\
        .all()

    messages = [x.to_dict() for x in messages]

    return jsonify({
        "message": "Success",
        "data": {
            "connection_id": int(connection_id),
            "messages": messages,
        }
    }), 200


# PATCH https://surprise-me.benbolt.house/api/v1/connections/<connection_id>/messages/<id>
# Updates a specific message for the given connection and handles emitting the
# message to connected parties.
@message_routes.route("/<connection_id>/messages/<id>", methods=["PATCH"])
@login_required
def patch(connection_id, id):
    get = request.json.get

    body = get("body")
    updated_at = get("updated_at")

    connection = Connection.query.filter(
        and_(
            or_(
                Connection.requestor_id == current_user.id,
                Connection.approver_id == current_user.id),
            Connection.id == int(connection_id))).first()

    # handle bad requests for non-member users
    if not connection or connection.is_deleted:
        raise BadRequest(response={
            "message": "User not connected to recipient user",
        })

    other_user = connection.other_user(current_user.id)
    recipient_id = other_user.id

    message_room_name = f"message_room_{recipient_id}"

    message = Message.query.filter(
        and_(
            Message.id == int(id),
            Message.connection_id == int(connection_id),
            Message.sender_id == current_user.id)).first()

    # handle requests for non-existend messages
    if not message or message.is_deleted:
        raise BadRequest(response={
            "message": "Message does not exist",
        })

    message.update(body=body, updated_at=updated_at)

    db.session.commit()

    response = {
        "message": "Success",
        "data": {
            "connection_id": int(connection_id),
            "messages": [message.to_dict()],
        }
    }

    # emit to user's message room
    socketio.emit("amend_message", response, to=message_room_name)

    return jsonify(response), 201


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
            "message": "User not connected to recipient user",
        })

    other_user = connection.other_user(current_user.id)
    recipient_id = other_user.id

    message_room_name = f"message_room_{recipient_id}"

    message = Message.query.filter(
        and_(
            Message.id == int(id),
            Message.connection_id == int(connection_id),
            Message.sender_id == current_user.id)).first()

    # handle requests for non-existend messages
    if not message or message.is_deleted:
        raise BadRequest(response={
            "message": "Message does not exist",
        })

    message.update(deleted_at=datetime.now())

    db.session.commit()

    response = {
        "message": "Success",
        "data": {
            "connection_id": int(connection_id),
            "messages": [message.to_deleted_dict()],
        }
    }

    # emit to user's message room
    socketio.emit("discard_message", response, to=message_room_name)

    return jsonify(response), 201
