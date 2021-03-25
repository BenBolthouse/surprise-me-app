from datetime import datetime
from flask import Blueprint
from flask_login import current_user
from flask_socketio import emit, send, join_room, leave_room
from flask_socketio import ConnectionRefusedError


from app import socketio
from models import db, User, UserConnection, ChatMessage, ChatNotification


events = Blueprint("events", __name__)


@socketio.on("connect")
def on_connect():
    send("Socketio Host: Client connected")


@socketio.on("join")
def on_join_room(data):
    room_id = data['roomId']
    join_room(room_id)
    send(f"Socketio Host: Client joined room {room_id}")


@socketio.on("leave")
def on_leave_room(data):
    room = data["roomId"]
    leave_room(room)
    send(f"Socketio Host: Client left room {room}")


@socketio.on("composer_interacting")
def post_chat_message(payload):
    emit("composer_interacting", payload, room=payload["roomId"])
    if payload["interacting"]:
        send("Socketio Host: Client is composing")
    else:
        send("Socketio Host: Client has stopped composing")


@socketio.on("chat_message")
def post_chat_message(payload):
    sender_user_id = payload["message"]["sender"]["id"]
    msg_conn_id = payload["message"]["userConnectionId"]
    user_connection = UserConnection.get_by_id(msg_conn_id)
    recipient_user_id = user_connection.user_is_associated(sender_user_id)
    sender_user = User.query.get(sender_user_id)
    chat_message = ChatMessage({
        "user_connection_id": msg_conn_id,
        "sender_user_id": sender_user_id,
        "recipient_user_id": recipient_user_id,
        "body": payload["message"]["body"],
    })
    db.session.add(chat_message)
    db.session.commit()
    existing_notification = ChatNotification.query.filter(
        ChatNotification.user_connection_id == user_connection.id,
        ChatNotification.recipient_user_id == recipient_user_id).first()
    if not existing_notification:
        chat_notification = ChatNotification({
            "user_connection_id": user_connection.id,
            "recipient_user_id": recipient_user_id,
            "notification_type": "message",
            "hook": f"/messages/{msg_conn_id}",
            "body": f"{sender_user.first_name} {sender_user.last_name} sent you a message"
        })
        db.session.add(chat_notification)
        db.session.commit()
    emit("chat_message", payload["message"], room=recipient_user_id)


@socketio.on_error_default
def default_error_handler(e):
    send(f"Socketio Host: Error in event: {e.args}")
