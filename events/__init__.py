from flask import Blueprint
from flask_login import current_user
from flask_socketio import emit, send, join_room, leave_room
from flask_socketio import ConnectionRefusedError


from app import socketio


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
    room = data['room']
    leave_room(room)
    send(f"Socketio Host: Client left room {room}")


@socketio.on("post_chat_message")
def post_chat_message(payload):
    emit("")


@socketio.on_error_default
def default_error_handler(e):
    send(f"Socketio Host: Error in event: {e.args}")
