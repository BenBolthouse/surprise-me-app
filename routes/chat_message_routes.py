from datetime import datetime
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user


from config import Config
from models import db, User, UserConnection
from models import ChatMessage


chat_message_routes = Blueprint(
    "chat_messages",
    __name__,
    url_prefix="/api/connections")


@chat_message_routes.route(
    "/<connection_id>/messages",
    methods=["POST"])
@login_required
def post_connection_message(connection_id):

    # Get session user
    session_user = current_user

    # Get request body properties
    message_body = request.json.get("body")

    # Get the connection
    connection = UserConnection.get_by_id(int(connection_id))

    # Don't allow users to send messages until the connection is established
    connection.require_establishment()

    # Don't allow unassociated users ability to post messages
    other_user = connection.user_by_id_is_associated(user.id)

    # Don't allow empty messages
    ChatMessage.require_body_text_not_empty_or_none(message_body)

    # Create a new chat message
    message = ChatMessage({
        "user_connection_id": connection.id,
        "sender_user_id": user.id,
        "recipient_user_id": other_user,
        "body": request.json.get("body"),
    })

    # Add and commit changes
    db.session.add(message)
    db.session.commit()

    # Respond 201 if successful
    return jsonify({
        "message": "Success",
        "data": message.to_json()
    }), 201


@chat_message_routes.route("/<id>/messages/datetime", methods=["GET"])
@login_required
def get_messages_after_datetime(id):

    # Get the connection
    connection = UserConnection.get_by_id(int(id))

    # Get user with collections from session user id
    user = User.get_by_id(current_user.id)

    # Check if the user is part of the connection
    connection.user_by_id_is_associated(user.id)

    # Get a list of filtered messages
    date_time = request.args.get("after")
    messages = connection.get_chat_messages_after_datetime(date_time)

    # Jsonify messages
    messages = [m.to_json() for m in messages]

    # Respond 200 if successful
    return jsonify({
        "message": "Success",
        "data": messages
    }), 200


@chat_message_routes.route("/<id>/messages/range", methods=["GET"])
@login_required
def get_messages_with_offset(id):

    # Get session user
    session_user = current_user

    # From URL args
    messages_offset = int(request.args.get("ofs"))
    messages_qty = int(request.args.get("qty"))

    # Get the connection
    connection = UserConnection.get_by_id(int(id))

    # Check if the user is part of the connection
    connection.user_is_associated(session_user.id)

    # Get the messages
    messages = connection.get_chat_messages_by_offset(
        messages_offset,
        messages_qty)

    # Jsonify messages
    messages = [m.to_json() for m in messages]

    # Respond 200 if successful
    return jsonify({
        "message": "Success",
        "data": messages
    }), 200


@chat_message_routes.route("/<id>/messages", methods=["PATCH"])
@login_required
def patch_connection_message(id):

    # Get the connection
    message = ChatMessage.get_by_id(int(request.json.get("id")))

    # Check to see if the user is the sender
    message.user_by_id_is_sender(current_user.id)

    # Update the message
    message.body = request.json.get("body")
    message.updated = True
    db.session.commit()

    # Respond 200 if successful
    return jsonify({
        "message": "Success",
        "data": message.to_json()
    }), 200


@chat_message_routes.route("/<id>/messages/<message_id>", methods=["DELETE"])
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
