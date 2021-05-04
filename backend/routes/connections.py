from datetime import datetime
from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required
from flask_socketio import emit
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
            and_(Connection._requestor_id == approver_id,
                 Connection._approver_id == current_user.id),
            and_(Connection._approver_id == approver_id,
                 Connection._requestor_id == current_user.id))).first()

    # handle requests for non-existent approvers
    if approver is None or approver.is_deleted:
        raise BadRequest(response={
            "message": "User does not exist",
        })

    # In the case of an existing, active connection we'll send the client a
    # reminder that they are already connected to this user.
    if existing_connection and not existing_connection.is_deleted:
        raise BadRequest(response={
            "message": "Connection already exists",
        })

    # If the route compiles to this point then it means we're either
    # creating or restoring a connection. Either way, a notification must
    # be sent to the approver.
    elif existing_connection:
        connection = existing_connection
        connection.rejoin(current_user.id)

        message = "Existing connection restored"
        status_code = 200

    else:
        connection = Connection(current_user.id, approver_id)

        db.session.add(connection)
        db.session.commit()

        message = "Connection created successfully"
        status_code = 201

    notification = Notification(
        "CONNECTION",
        approver.id,
        f"{current_user.first_name} {current_user.last_name} wants to connect",
        f"{Config.PUBLIC_URL}/connections/{connection.id}/approval")

    # Emit a websocket message to the approver's room if available.
    emit("connection",
         notification.to_ws_response(),
         namespace="notifications",
         room=f"user_{approver.id}")

    db.session.add(notification)
    db.session.commit()

    return jsonify({
        "message": message,
        "data": connection.to_dict(current_user),
    }), status_code


# GET https://surprise-me.benbolt.house/api/v1/users/<id>/connections
# Retrieves all of a logged in user's own pending and approved connections.
@connection_routes.route("", methods=["GET"])
@login_required
def get():
    connections = Connection.query.filter(
        or_(
            Connection._requestor_id == current_user.id,
            Connection._approver_id == current_user.id)
    ).order_by(
        Connection._approved_at.asc(),
        Connection._created_at.desc()).all()

    connections = [x.to_dict(current_user.id) for x in connections]

    return jsonify({
        "message": "Success",
        "data": connections,
    }), 200


# PATCH https://surprise-me.benbolt.house/api/v1/connections/<id>/approve
# Updates an unestablished connection to an established state via approver
# approval. The user must be the approver of the connection.
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

    # handle requests for connections for which the user isn't approver
    if connection.approver_id != current_user.id:
        raise Forbidden(response={
            "message": "User not approver",
        })

    connection.approve()

    db.session.commit()

    return jsonify({
        "message": "Connection approved successfully",
        "data": connection.to_dict(current_user),
    }), 200


# PATCH https://surprise-me.benbolt.house/api/v1/connections/<id>/deny
# Updates an unestablished connection to a refused state via approver
# denial. The user must be the approver of the connection.
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

    # handle requests for connections for which the user isn't approver
    if connection.approver_id != current_user.id:
        raise Forbidden(response={
            "message": "User not approver",
        })

    connection.deny()

    db.session.commit()

    return jsonify({
        "message": "Connection denied successfully",
        "data": connection.to_dict(current_user),
    }), 200


# DELETE https://surprise-me.benbolt.house/api/v1/users/<user_id>/connections/<id>
# Performs a soft delete of the connection in the database.
@ connection_routes.route("/<id>", methods=["DELETE"])
@ login_required
def delete_soft(id):
    connection = Connection.query.filter(
        or_(
            and_(Connection._requestor_id == current_user.id,
                 Connection._id == int(id)),
            and_(Connection._approver_id == current_user.id,
                 Connection._id == int(id)))).first()

    if connection is None:
        raise Forbidden(response={
            "message": "User not member",
        })

    connection.leave()

    db.session.commit()

    return jsonify({
        "message": "Connection deleted successfully",
    }), 200


# DELETE https://surprise-me.benbolt.house/api/v1/users/<user_id>/connections/<id>/hard
# Performs a hard delete of the connection from the database.
@ connection_routes.route("/<id>/hard", methods=["DELETE"])
@ login_required
def delete_hard(user_id, id):
    raise Exception("Not implemented")
