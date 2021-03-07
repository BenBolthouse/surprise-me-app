from datetime import datetime
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user


from config import Config
from models import db, User, UserConnection, UserNotification


user_connection_routes = Blueprint("user_connections", __name__,
                                   url_prefix="/api/user_connections")


@user_connection_routes.route("", methods=["POST"])
@login_required
def post_user_connection():

    # Get session user
    user = current_user

    # Respond 400 if connection user nonexistent
    connection_user_id = request.json.get("connectionUserId")
    connection_user = User.query.get(connection_user_id)
    connection_user_nonexistent = connection_user is None
    if connection_user_nonexistent:
        return jsonify({
            "message": "connection_user_nonexistent",
        }), 400

    # Define the new connection
    connection = UserConnection(connection_user.id)

    # Add connection to the session user
    user.connections = connection

    # Commit changes
    db.session.commit()

    # Create notifications for connection user
    notification = UserNotification(
        connection_user.id,
        "USER_CONN_REQ",
        f"{Config.HOST_NAME}/api/user_connections/{connection.id}",
        f"{user.first_name} {user.last_name} sent you a friend request.")
    connection_user.notifications = notification

    # Commit changes
    db.session.commit()

    return jsonify({
        "message": "success",
        "data": connection.to_json_on_create()
    }), 201


@user_connection_routes.route("<user_connection_id>",
                              methods=["PATCH"])
@login_required
def patch_fulfill_user_connection(user_connection_id):

    # Get session user
    user = current_user

    # Respond 400 if connection nonexistent
    connection = UserConnection.query.get(int(user_connection_id))
    connection_nonexistent = connection is None
    if connection_nonexistent:
        return jsonify({
            "message": "connection_nonexistent",
        }), 400

    # Establish or delete connection
    establish_connection = request.json.get("establish")
    if establish_connection:
        connection.established_at = datetime.now()

        # Send the requestor a notification
        requestor_user = User.query.get(connection.requestor_user_id)
        notification = UserNotification(
            user.id,
            "USER_CONN_REQ_EST",
            None,
            f"{user.first_name} {user.last_name} accepted your friend request.")
        requestor_user.notifications = notification

    else:
        # Else delete the connection request
        db.session.delete(connection)

    # Commit changes
    db.session.commit()

    return jsonify({
        "message": "success",
        "data": connection.to_json_on_create() if establish_connection else "deleted"
    }), 200
