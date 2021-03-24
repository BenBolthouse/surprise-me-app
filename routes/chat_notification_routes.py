from datetime import datetime
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user


from config import Config
from models import db, ChatNotification
from models import ChatMessage


chat_notification_routes = Blueprint(
    "chat_notifications",
    __name__,
    url_prefix="/api/connections")


# ** «««««««««««««««« GET Routes »»»»»»»»»»»»»»»» **


@chat_notification_routes.route("/<id>/chat_notifications", methods=["GET"])
@login_required
def get_chat_notifications(id):

    # Get session user
    session_user = current_user

    # Jsonify messages
    notifications = [m.to_json() for m in session_user.notifications]

    # Respond 200 if successful
    return jsonify({
        "message": "Success",
        "data": notifications
    }), 200


# ** «««««««««««««««« DELETE Routes »»»»»»»»»»»»»»»» **


@chat_notification_routes.route("/<id>/chat_notifications/<notification_id>", methods=["DELETE"])
@login_required
def delete_chat_notification(id, message_id):

    # Find the chat notification
    notification = ChatNotification.query.get(notification_id)

    # Then delete it
    db.session.delete(notification)
    db.session.commit()
    
    # Respond 200 if successful
    return jsonify({
        "message": "Success",
    }), 200
