from datetime import datetime
from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required
from flask_socketio import emit
from socketio.exceptions import SocketIOError
from sqlalchemy import and_, or_
from werkzeug.exceptions import BadRequest, Forbidden


from app import socketio
from config import Config
from models import db, Connection, Notification, User


connection_routes = Blueprint("connection_routes", __name__, url_prefix="/api/v1/connections")


# POST https://surprise-me.benbolt.house/api/v1/connections
# Creates a new connection between users. Connections must be approved by
# the approver to become active. Existing connection between user raises
# an exception. Existing soft deleted connections between users are
# reactivated.
@connection_routes.route("", methods=["POST"])
@login_required
def post():
    approver_id = request.json.get("approver_id")

    # find existing approver user and/or existing connection
    approver = User.query.get(approver_id)
    existing_connection = Connection.query.filter(
        or_(
            and_(Connection.requestor_id == approver_id,
                 Connection.approver_id == current_user.id),
            and_(Connection.approver_id == approver_id,
                 Connection.requestor_id == current_user.id))).first()

    # handle requests for non-existent approvers
    if approver is None or approver.is_deleted:
        raise BadRequest(response={
            "notification": {
                "body": "The user you requested to connect with doesn't exist.",
                "type": "popup",
                "duration": 4,
            },
        })

    # In the case of an existing, active connection we'll send the client a
    # reminder that they are already connected to this user.
    if existing_connection and not existing_connection.is_deleted:
        raise BadRequest(response={
            "notification": {
                "body": "You are already connected with this user.",
                "type": "popup",
                "duration": 3,
            },
        })

    # If the route compiles to this point then it means we're either
    # creating or restoring a connection. Either way, a notification must
    # be sent to the approver.
    elif existing_connection:
        connection = existing_connection
        connection.rejoin(current_user.id)

        status_code = 200

    else:
        connection = Connection(current_user.id, approver_id)

        db.session.add(connection)
        db.session.commit()

        status_code = 201

    notification = Notification()
    notification.recipient_id = approver.id
    notification.type = "bell_notification"
    notification.body = f"{current_user.first_name} {current_user.last_name} wants to connect with you."
    notification.action = f"/#/approvals/{connection.id}"

    db.session.add(notification)
    db.session.commit()

    # Emit a notification to the approver's user notifications channel.
    emit("receive_user_notification", {
        "data": connection.to_dict(approver_id),
        "notification": {
            "id": notification.id,
            "body": notification.body,
            "type": notification.type,
            "action": notification.action,
        }
    }, room=f"user_notifications_{approver_id}")

    return jsonify({
        "data": connection.to_dict(current_user.id),
        "notification": {
            "body": f"A connection request has been sent to {approver.first_name}.",
            "type": "popup",
            "duration": 4,
        },
    }), status_code


# GET https://surprise-me.benbolt.house/api/v1/connections
# Retrieves all of a logged in user's own pending and approved connections.
@connection_routes.route("", methods=["GET"])
@login_required
def get():
    connections = Connection.query.filter(
        or_(
            Connection.requestor_id == current_user.id,
            Connection.approver_id == current_user.id)
    ).order_by(
        Connection.approved_at.asc(),
        Connection.created_at.desc()).all()

    connections = [x.to_dict(current_user.id) for x in connections]

    return jsonify({
        "data": connections,
    }), 200


# PATCH https://surprise-me.benbolt.house/api/v1/connections/<id>/approve
# Updates an unestablished connection to an established state via approver
# approval. The user must be the approver of the connection.
@connection_routes.route("/<id>/approve", methods=["PATCH"])
@login_required
def patch_approve(id):
    # handle requests for non-existent connections
    connection = Connection.query.get(int(id))

    if connection is None:
        raise BadRequest(response={
            "notification": {
                "body": "This connection request longer exists.",
                "type": "popup",
                "duration": 3,
            },
        })

    # handle requests for connections for which the user isn't approver
    if connection.approver_id != current_user.id:
        raise Forbidden(response={
            "notification": {
                "body": "You cannot approve this connection.",
                "type": "popup",
                "duration": 3,
            },
        })

    # handle requests for connections that are already approved
    if connection.approved_at is not None:
        raise BadRequest(response={
            "notification": {
                "body": "This connection is already approved.",
                "type": "popup",
                "duration": 3,
            },
        })

    connection.approve()

    db.session.commit()

    return jsonify({
        "data": connection.to_dict(current_user.id),
        "notification": {
            "body": "Connection approved",
            "type": "popup",
            "delay": 2,
        },
    }), 200


# PATCH https://surprise-me.benbolt.house/api/v1/connections/<id>/deny
# Updates an unestablished connection to a refused state via approver
# denial. The user must be the approver of the connection.
@connection_routes.route("/<id>/deny", methods=["PATCH"])
@login_required
def patch_deny(id):
    # handle requests for non-existent connections
    connection = Connection.query.get(int(id))

    if connection is None:
        raise BadRequest(response={
            "notification": {
                "body": "This connection request longer exists.",
                "type": "popup",
                "delay": 3,
            },
        })

    # handle requests for connections for which the user isn't approver
    if connection.approver_id != current_user.id:
        raise Forbidden(response={
            "notification": {
                "body": "You cannot deny this connection.",
                "type": "popup",
                "delay": 3,
            },
        })

    connection.deny()

    db.session.commit()

    return jsonify({
        "data": connection.to_dict(current_user.id),
        "notification": {
            "body": "Connection request removed",
            "type": "popup",
            "delay": 2,
        },
    }), 200


# DELETE https://surprise-me.benbolt.house/api/v1/users/<user_id>/connections/<id>
# Performs a soft delete of the connection in the database.
@ connection_routes.route("/<id>", methods=["DELETE"])
@ login_required
def delete_soft(id):
    connection = Connection.query.filter(
        or_(
            and_(Connection.requestor_id == current_user.id,
                 Connection.id == int(id)),
            and_(Connection.approver_id == current_user.id,
                 Connection.id == int(id)))).first()

    if connection is None:
        raise Forbidden(response={
            "notification": {
                "body": "You cannot leave this connection.",
                "type": "popup",
                "delay": 3,
            },
        })

    connection.leave()

    db.session.commit()

    return jsonify({
        "data": connection.to_dict(current_user.id),
        "notification": {
            "body": "You have left the connection.",
            "type": "popup",
            "delay": 3,
        },
    }), 200


# DELETE https://surprise-me.benbolt.house/api/v1/users/<user_id>/connections/<id>/hard
# Performs a hard delete of the connection from the database.
@ connection_routes.route("/<id>/hard", methods=["DELETE"])
@ login_required
def delete_hard(user_id, id):
    raise Exception("Not implemented")


# EVENT composing_message
# Notifies the other user of a connection of when the user is composing or
# has abandoned a new message for this connection.
@socketio.on("composing_message")
def handle_composing_message(payload):
    connection_id = payload["connection_id"]
    composing = payload["composing"]

    connection = Connection.query.filter(
        or_(
            and_(Connection.requestor_id == current_user.id,
                 Connection.id == connection_id),
            and_(Connection.approver_id == current_user.id,
                 Connection.id == connection_id))).first()

    # handle requests for non-existent connections
    if not connection or connection.is_deleted:
        raise SocketIOError()

    other_user = connection.other_user(current_user.id)

    recipient_id = other_user.id

    response = {
        "id": connection_id,
        "user_composing": composing,
    }

    # emit to user's message room
    socketio.emit("composing_message", response, to=f"message_room_{recipient_id}")
