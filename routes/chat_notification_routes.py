from datetime import datetime
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user


from config import Config
from models import db, ChatNotification
from models import ChatMessage


chat_notification_routes = Blueprint(
    "chat_notifications",
    __name__,
    url_prefix="/api/chat_notifications")


# ** «««««««««««««««« GET Routes »»»»»»»»»»»»»»»» **


@chat_notification_routes.route("", methods=["GET"])
@login_required
def get_chat_notifications():

    # Get session user
    session_user = current_user

    # Jsonify messages
    notifications = [m.to_json() for m in session_user.chat_notifications]

    # Respond 200 if successful
    return jsonify({
        "message": "Success",
        "data": notifications
    }), 200


# ** «««««««««««««««« DELETE Routes »»»»»»»»»»»»»»»» **

@chat_notification_routes.route("", methods=["DELETE"])
@login_required
def delete_chat_notifications(id):

    # Get session user
    session_user = current_user

    # Find the chat notification
    notification = ChatNotification.query.filter(
        ChatNotification.recipient_user_id == session_user.id)

    # Then delete it
    db.session.delete(notification)
    db.session.commit()
    
    # Respond 200 if successful
    return jsonify({
        "message": "Success",
    }), 200


@chat_notification_routes.route("/<id>", methods=["DELETE"])
@login_required
def delete_chat_notification(id):

    # Find the chat notification
    notification = ChatNotification.query.filter(
        ChatNotification.user_connection_id == int(id)).first()

    # Then delete it
    if notification:
        db.session.delete(notification)
        db.session.commit()
    
    # Respond 200 if successful
    return jsonify({
        "message": "Success",
    }), 200
