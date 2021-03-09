from datetime import datetime
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user


from config import Config
from models import db, User, UserConnection
from models import UserNotification, ChatMessage
from utilities import normalize_to_dictionary


user_connection_routes = Blueprint(
    "user_connections",
    __name__,
    url_prefix="/api/user_connections")


@user_connection_routes.route("", methods=["POST"])
@login_required
def post_user_connection():

    # Data from request
    recipient_id = request.json.get("connectionUserId")

    # Get user with collections from session user id
    user = User.get_by_id(current_user.id)

    # Respond 400 if connection user nonexistent
    recipient_user = User.get_by_id(recipient_id)

    # Check if the users are already connected
    user.user_by_id_is_a_connection(recipient_id)

    # Define the new connection
    new_connection = UserConnection(recipient_id)

    # Add connection to the session user
    user.connections = new_connection

    # Commit changes
    db.session.commit()

    # Create notifications for connection user
    new_notification = UserNotification(
        recipient_id,
        "USER_CONN_REQ",
        f"{Config.HOST_NAME}/api/user_connections/{new_connection.id}",
        f"{user.first_name} {user.last_name} sent you a friend request.")

    recipient_user.notifications = new_notification

    # Commit changes
    db.session.commit()

    # Respond 201 if successful
    return jsonify({
        "message": "Success",
        "data": new_connection.to_json_on_create()
    }), 201


@user_connection_routes.route("<id>", methods=["PATCH"])
@login_required
def patch_fulfill_user_connection(id):

    # Get the connection
    connection = UserConnection.get_by_id(int(id))

    # Get user with collections from session user id
    user = User.get_by_id(current_user.id)

    # Respond 400 if user not associated with connection
    # (prevents requestor from establishing own requested connections)
    connection.user_by_id_is_recipient(user.id)

    # Establish or delete connection
    establish = request.json.get("establish")
    if establish:
        connection.established_at = datetime.now()

        # Send the requestor a notification
        requestor_user = User.query.get(connection.requestor_user_id)
        notification = UserNotification(
            user.id,
            "USER_CONN_REQ_EST",
            None,
            f"{user.first_name} {user.last_name} accepted your friend request.")  # noqa
        requestor_user.notifications = notification

        # Commit changes
        db.session.commit()
    else:
        # Else delete the connection request
        db.session.delete(connection)

    # Respond 200 if successful
    return jsonify({
        "message": "Success",
        "data": connection.to_json_on_create() if establish else "deleted"  # noqa
    }), 200


@user_connection_routes.route("<id>/messages", methods=["POST"])
@login_required
def post_connection_message(id):

    # Get the connection
    connection = UserConnection.get_by_id(int(id))

    # Get user with collections from session user id
    user = User.get_by_id(current_user.id)

    # Don't allow users to send messages until the connection is established
    connection.require_establishment()

    # Create a new chat message
    message_body = request.json.get("body")
    message = ChatMessage(user.id, message_body)
    connection.messages = message

    # Commit changes
    db.session.commit()

    # Respond 201 if successful
    return jsonify({
        "message": "Success",
        "data": message.to_json_on_create()
    }), 201


@user_connection_routes.route("<id>/messages/d", methods=["GET"])
@login_required
def get_messages_after_datetime(id):

    # Get the connection
    connection = UserConnection.get_by_id(int(id))

    # Get user with collections from session user id
    user = User.get_by_id(current_user.id)

    # Get a list of filtered messages
    date_time = request.args.get("after")
    messages = connection.get_chat_messages_after_datetime(date_time)

    # Respond 200 if successful
    return jsonify({
        "message": "Success",
        "data": messages
    }), 200


@user_connection_routes.route("<id>/messages/o", methods=["GET"])
@login_required
def get_messages_with_offset(id):

    connection_id = int(id)
    messages_offset = int(request.args.get("offset"))
    messages_qty = int(request.args.get("quantity"))

    # Get the connection
    connection = UserConnection.get_by_id(int(id))

    # Get user with collections from session user id
    user = User.get_by_id(current_user.id)

    # Get the messages
    messages = connection.get_chat_messages_by_offset(
        messages_offset,
        messages_qty)

    # Respond 200 if successful
    return jsonify({
        "message": "Success",
        "data": messages
    }), 200


@user_connection_routes.route("<id>/messages", methods=["PATCH"])
@login_required
def patch_connection_message(id):

    # Get the connection
    message = ChatMessage.get_by_id(int(request.json.get("id")))

    # Check to see if the user is the sender
    message.user_by_id_is_sender(current_user.id)

    # Update the message
    message.body = request.json.get("body")
    db.session.commit()

    # Respond 200 if successful
    return jsonify({
        "message": "Success",
        "data": message.to_json_on_patch()
    }), 200


@user_connection_routes.route("<id>/messages/<message_id>", methods=["DELETE"])
@login_required
def delete_connection_message(id, message_id):

    # Get the connection
    message = ChatMessage.get_by_id(int(message_id))

    # Check to see if the user is the sender
    message.user_by_id_is_sender(current_user.id)

    # Update the message
    db.session.delete(message)
    db.session.commit()

    # Respond 200 if successful
    return jsonify({
        "message": "Success",
    }), 200
