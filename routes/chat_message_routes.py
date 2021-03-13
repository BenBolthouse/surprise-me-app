from datetime import datetime
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user


from config import Config
from models import db, User, UserConnection
from models import ChatMessage


chat_message_routes = Blueprint(
    "chat_messages",
    __name__,
    url_prefix="/api/user_connections")


@chat_message_routes.route(
    "/<connection_id>/messages",
    methods=["POST"])
@login_required
def post_connection_message(connection_id):

    # Get the connection
    connection = UserConnection.get_by_id(int(connection_id))

    # Get user with collections from session user id
    user = User.get_by_id(current_user.id)

    # Don't allow users to send messages until the connection is established
    connection.require_establishment()

    # Don't allow unassociated users ability to post messages
    connection.user_by_id_is_associated(user.id)

    # Create a new chat message
    message_body = request.json.get("body")
    message = ChatMessage(connection.id, user.id, message_body)

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

    # From URL args
    messages_offset = int(request.args.get("offset"))
    messages_qty = int(request.args.get("quantity"))

    # Get the connection
    connection = UserConnection.get_by_id(int(id))

    # Get user with collections from session user id
    user = User.get_by_id(current_user.id)

    # Check if the user is part of the connection
    connection.user_by_id_is_associated(user.id)

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
    db.session.commit()

    # Respond 200 if successful
    return jsonify({
        "message": "Success",
        "data": message.to_json_on_patch()
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
