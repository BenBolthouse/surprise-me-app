from datetime import datetime
from flask import Blueprint, jsonify
from flask_login import current_user, login_required
from flask_socketio import emit
from sqlalchemy import and_, or_
from werkzeug.exceptions import BadRequest, Forbidden


from app import socketio
from config import Config
from models import db, Connection, Notification, User


connection_routes = Blueprint("connection_routes", __name__, url_prefix="/api/v1/connections")


# POST
# https://surprise-me.benbolt.house/api/v1/connections/add/<recipient_id>
# Creates a new connection between users. Connections must be approved by
# the recipient to become active. Existing connection between user raises
# an exception. Existing soft deleted connections between users are
# reactivated.
@connection_routes.route("/add/<recipient_id>", methods=["POST"])
@login_required
def post(recipient_id):
    # find existing recipient user and/or existing connection
    recipient = User.query.get(int(recipient_id))
    existing_connection = Connection.query.filter(
        or_(
            and_(Connection.requestor == int(recipient_id),
                 Connection.recipient == current_user.id),
            and_(Connection.recipient == int(recipient_id),
                 Connection.requestor == current_user.id))).first()

    # handle requests for non-existent recipients
    if recipient is None or recipient.is_deleted:
        raise BadRequest(response={
            "message": "Recipient does not exist",
        })

    # In the case of an existing, active connection we'll send the client a
    # reminder that they are already connected to this user.
    if existing_connection and not existing_connection.is_deleted:
        raise BadRequest(response={
            "message": "Connection already exists",
        })

    # If the route compiles to this point then it means we're either
    # creating or restoring a connection. Either way, a notification must
    # be sent to the recipient.
    elif existing_connection:
        connection = existing_connection
        connection.rejoin(current_user.id)

        message = "Existing connection restored"
        status_code = 200

    else:
        connection = Connection(current_user.id, int(recipient_id))
        db.session.add(connection)
        db.session.commit()

        message = "Connection created successfully"
        status_code = 201

    notification = Notification(
        "CONNECTION",
        recipient=recipient.id,
        body=f"{current_user.first_name} {current_user.last_name} wants to connect",
        action=f"{Config.PUBLIC_URL}/connections/{connection.id}/approval")

    # Emit a websocket message to the recipient's room if available.
    emit("connection",
         notification.to_ws_response(),
         namespace="notifications",
         room=f"user_{recipient.id}")

    db.session.add(notification)
    db.session.commit()

    return jsonify({
        "message": message,
    }), status_code


# PATCH https://surprise-me.benbolt.house/api/v1/connections/<id>/approve
# Updates an unestablished connection to an established state via recipient
# approval. The user must be the recipient of the connection.
@connection_routes.route("/<id>/approve", methods=["PATCH"])
@login_required
def patch_approve(id):
    try:
        # handle requests for non-existent connections
        connection = Connection.query.get(int(id))

    except(Exception) as exception:
        raise BadRequest(response={
            "message": "Connection does not exist",
        })

    # handle requests for connections for which the user isn't recipient
    if connection.recipient != current_user.id:
        raise Forbidden(response={
            "message": "User not recipient",
        })

    try:
        connection.approve()

        db.session.commit()

    except(Exception) as exception:
        raise InternalServerError()

    else:
        return jsonify({
            "message": "Connection approved successfully",
        }), 200


# PATCH https://surprise-me.benbolt.house/api/v1/connections/<id>/deny
# Updates an unestablished connection to a refused state via recipient
# denial. The user must be the recipient of the connection.
@connection_routes.route("/<id>/deny", methods=["PATCH"])
@login_required
def patch_deny(id):
    try:
        # handle requests for non-existent connections
        connection = Connection.query.get(int(id))

    except(Exception) as exception:
        raise BadRequest(response={
            "message": "Connection does not exist",
        })

    # handle requests for connections for which the user isn't recipient
    if connection.recipient != current_user.id:
        raise Forbidden(response={
            "message": "User not recipient",
        })

    try:
        connection.deny()

        db.session.commit()

    except(Exception) as exception:
        raise InternalServerError()

    else:
        return jsonify({
            "message": "Connection denied successfully",
        }), 200


# GET https://surprise-me.benbolt.house/api/v1/users/<id>/connections
# Retrieves all of a logged in user's own pending and approved connections.
@connection_routes.route("", methods=["GET"])
@login_required
def get(id):
    connections = Connection.query.filter(
        or_(Connection.requestor == current_user.id),
        or_(Connection.recipient == current_user.id))

    connections = [x.to_http_response() for x in connections]

    return jsonify({
        "message": "Success",
        "data": connections,
    }), 200


# DELETE https://surprise-me.benbolt.house/api/v1/users/<user_id>/connections/<id>
# Performs a soft delete of the connection in the database.
@ connection_routes.route("/<id>", methods=["DELETE"])
@ login_required
def delete_soft(id):
    connection = Connection.query.filter(
        or_(
            and_(Connection.requestor == current_user.id,
                 Connection.id == int(id)),
            and_(Connection.recipient == current_user.id,
                 Connection.id == int(id)))).first()

    if connection is None:
        raise Forbidden(response={
            "message": "User not member",
        })

    connection.leave()

    return jsonify({
        "message": "Connection deleted successfully",
    }), 200


# DELETE https://surprise-me.benbolt.house/api/v1/users/<user_id>/connections/<id>/hard
# Performs a hard delete of the connection from the database.
@ connection_routes.route("/<id>/hard", methods=["DELETE"])
@ login_required
def delete_hard(user_id, id):
    raise Exception("Not implemented")
