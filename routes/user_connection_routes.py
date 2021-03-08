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

    # Get session user
    user = current_user

    # Respond 400 if connection user nonexistent
    recipient_id = request.json.get("connectionUserId")
    recipient_user = User.query.get(recipient_id)
    if recipient_user is None:
        return jsonify({
            "message": "Recipient user does not exist",
        }), 400

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
        "message": "success",
        "data": new_connection.to_json_on_create()
    }), 201


@user_connection_routes.route("<id>", methods=["PATCH"])
@login_required
def patch_fulfill_user_connection(id):

    connection_id = int(id)

    # Get session user
    user = current_user

    # Respond 400 if connection nonexistent
    connection = [c for c in user.connections if c.id == connection_id]
    connection = connection[0] if len(connection) != 0 else None
    if connection is None:
        return jsonify({
            "message": "Connection does not exist",
        }), 404

    # Respond 400 if user not associated with connection
    # (prevents requestor from establishing own requested connections)
    if connection.connection_user_id != user.id:
        return jsonify({
            "message": "Connection does not exist",
        }), 404

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

    else:
        # Else delete the connection request
        db.session.delete(connection)

    # Commit changes
    db.session.commit()

    # Respond 200 if successful
    return jsonify({
        "message": "success",
        "data": connection.to_json_on_create() if establish else "deleted"  # noqa
    }), 200


@user_connection_routes.route("<id>/messages", methods=["POST"])
@login_required
def post_connection_message(id):

    connection_id = int(id)

    # Get session user
    user = current_user

    # Respond 400 if connection nonexistent
    connection = [c for c in user.connections if c.id == connection_id]
    connection = connection[0] if len(connection) != 0 else None
    connection_nonexistent = connection is None
    if connection_nonexistent:
        return jsonify({
            "message": "connection_nonexistent",
        }), 400

    # Create a new chat message
    message_body = request.json.get("body")
    message = ChatMessage(user.id, message_body)
    connection.messages = message

    # Commit changes
    db.session.commit()

    # Return 201 if successful
    return jsonify({
        "message": "success",
        "data": message.to_json_on_create()
    }), 201


@user_connection_routes.route("<id>/messages/d", methods=["GET"])
@login_required
def get_messages_after_datetime(id):

    connection_id = int(id)
    filter_date_format = "%Y-%m-%dT%H:%M:%S.%f"
    filter_date_string = request.args.get("after")
    filter_date_obj = datetime.strptime(filter_date_string, filter_date_format)

    # Get session user
    user = current_user

    # Respond 400 if connection nonexistent
    connection = [c for c in user.connections if c.id == connection_id]
    connection = connection[0] if len(connection) != 0 else None
    if connection is None:
        return jsonify({
            "message": "connection_nonexistent",
        }), 400

    # Make a list of filtered messages
    filtered_message_list = [m.to_json_on_create()
                             for m in connection.messages
                             if m.created_at > filter_date_obj]

    # Return 200 if successful
    return jsonify({
        "message": "success",
        "data": {
            "chat_messages": filtered_message_list
        }
    }), 200


@user_connection_routes.route("<id>/messages/o", methods=["GET"])
@login_required
def get_messages_with_offset(id):

    connection_id = int(id)
    messages_offset = int(request.args.get("offset"))
    messages_qty = int(request.args.get("quantity"))

    # Get session user
    user = current_user

    # Respond 400 if connection nonexistent
    connection = [c for c in user.connections if c.id == connection_id]
    connection = connection[0] if len(connection) != 0 else None
    if connection is None:
        return jsonify({
            "message": "connection_nonexistent",
        }), 400

    # Reverse messages list to make reverse chronological order
    chat_list = connection.messages.copy()
    chat_list.reverse()

    # Slice off requested range
    offset_end = messages_offset + messages_qty
    chat_list = chat_list[messages_offset:offset_end]

    # Make a list of filtered messages
    chat_list = [m.to_json_on_create()
                 for m in chat_list]

    # Respond 200 if successful
    return jsonify({
        "message": "success",
        "data": {
            "chat_messages": chat_list
        }
    }), 200
