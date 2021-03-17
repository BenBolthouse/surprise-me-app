from datetime import datetime
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user


from config import Config
from models import db, User, UserConnection
from models import UserNotification, ChatMessage


user_connection_routes = Blueprint(
    "connections",
    __name__,
    url_prefix="/api/connections")


# ** «««««««««««««««« POST Routes »»»»»»»»»»»»»»»» **


@user_connection_routes.route("", methods=["POST"])
@login_required
def post_user_connection():

    # Get session user
    session_user = current_user

    # Properties from JSON request
    recipient_user_id = request.json.get("recipientUserId")

    # Respond 400 if connection user nonexistent
    recipient_user = User.get_by_id(recipient_user_id)

    # Check if the users are already connected
    session_user.other_user_is_not_a_connection(recipient_user_id)

    # Define the new connection
    connection = UserConnection({
        "requestor_user_id": session_user.id,
        "recipient_user_id": recipient_user_id,
    })

    # Add connection to the session user
    session_user.add_connection(connection)

    # Commit changes
    db.session.commit()

    # Create notifications for connection user
    notification = UserNotification({
        "user_id": recipient_user_id,
        "notification_type", "Connection Request",
        "hook", f"{Config.HOST_NAME}/api/connections/{connection.id}",
        "body", f"{session_user.first_name} {session_user.last_name} sent you a friend request.",  # noqa
    })

    # Get recipient user
    recipient_user = User.query.get(recipient_user_id)

    # Add notification to recipient
    recipient_user.add_notification(notification)

    # Commit changes
    db.session.commit()

    # Respond 201 if successful
    return jsonify({
        "message": "Success",
        "data": connection.to_json()
    }), 201


# ** «««««««««««««««« GET Routes »»»»»»»»»»»»»»»» **


@user_connection_routes.route("/", methods=["GET"])
@login_required
def get_all_user_connections():

    # Get session user
    session_user = current_user

    # Get all connections to a list
    json_response = session_user.to_json_connections()

    # Respond 200 if successful
    return jsonify({
        "message": "Success",
        "data": json_response["connections"]
    }), 200


# ** «««««««««««««««« PATCH Routes »»»»»»»»»»»»»»»» **


@user_connection_routes.route("/<id>/accept", methods=["PATCH"])
@login_required
def patch_accept_user_connection_request(id):

    # Get session user
    session_user = current_user

    # Get the connection
    connection = UserConnection.get_by_id(int(id))

    # Respond 400 if user not associated with connection
    connection.user_is_recipient(user.id)

    # Establish the connection and notify the recipient
    connection.established_at = datetime.now()
    notification = UserNotification({
        "user_id": connection.requestor_user_id,
        "notification_type", "Connection Request Accepted",
        "hook", f"{Config.HOST_NAME}/users/{session_user.id}",
        "body", f"{connection.recipient.first_name} {connection.recipient.last_name} accepted your friend request.",  # noqa
    })
    connection.requestor.add_notification(notification)
    db.session.commit()

    # Respond 200 if successful
    return jsonify({
        "message": "Success",
        "data": connection.to_json()
    }), 200
