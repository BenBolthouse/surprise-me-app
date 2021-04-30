from datetime import datetime
from flask import Blueprint
from flask_login import current_user, login_required
from flask_socketio import emit
from werkzeug.exceptions import BadRequest, Forbidden


from app import socketio
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
        and_(Connection.requestor == int(recipient_id),
             Connection.recipient == int(current_user.id)),
        and_(Connection.requestor == int(current_user.id),
             Connection.recipient == int(recipient_id))
    ).first()

    # handle requests for non-existent recipients
    if not recipient or not recipient.is_deleted():
        raise BadRequest(response={
            "message": "Recipient does not exist",
        })

    # handle requests for existing connection
    if existing_connection:
        # handle requests where the connection was soft deleted
        if existing_connection.is_deleted():
            existing_connection.unset_deleted_at()

            return jsonify({
                "message": "Existing connection restored",
            }), 200

        # handle requests where the connection is not deleted
        else:
            raise BadRequest(response={
                "message": "Connection already exists",
            })

    else:
        connection = Connection(current_user.id, int(recipient_id))

        # session commit needed to obtain next connection id in sequence
        db.session.add(connection)
        db.session.commit()

        notification = Notification(
            "CONNECTION",
            recipient=recipient.id,
            body=f"{current_user.first_name} {current_user.last_name} wants to connect",
            action=f"{PUBLIC_URL}/connections/{connection.id}/approve")

        # Emit a websocket message to the recipient's room if available.
        emit(f"connected_user", notification.to_ws_response(), room=f"user_{recipient.id}")

        db.session.add(notification)
        db.session.commit()

        return jsonify({
            "message": "Connection created successfully",
        }), 201


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
    if connection.recipient_id != current_user.id:
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
            "message": "Connection was approved",
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
    if connection.recipient_id != current_user.id:
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
            "message": "Connection was denied",
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
    connections = Connection.query.filter(
        or_(Connection.requestor == current_user.id),
        or_(Connection.recipient == current_user.id),
        and_(Connection.id == int(id))).first()

    if connection is None:
        raise BadRequest(response={
            "message": "Connection does not exist for user",
        })

    connection.set_deleted_at()

    return jsonify({
        "message": "Connection deleted successfully",
    }), 200


# DELETE https://surprise-me.benbolt.house/api/v1/users/<user_id>/connections/<id>/hard
# Performs a hard delete of the connection from the database.
@ connection_routes.route("/<id>/hard", methods=["DELETE"])
@ login_required
def delete_hard(user_id, id):
    raise Exception("Not implemented")
