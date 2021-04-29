from flask import Blueprint
from flask_socketio import emit, send


from app import socketio


message_events = Blueprint("message_events", __name__)


@socketio.on("join_message_room")
def join_message_room(room_id):
    raise Exception("Not implemented")


@socketio.on("leave_message_room")
def leave_message_room(room_id):
    raise Exception("Not implemented")


@socketio.on("message_begin")
def message_begin(room_id):
    raise Exception("Not implemented")


@socketio.on("message_end")
def message_end(room_id):
    raise Exception("Not implemented")


@socketio.on("message_sent")
def message_sent(payload, room_id):
    raise Exception("Not implemented")


@socketio.on("message_received")
def message_received(message_id, room_id):
    raise Exception("Not implemented")


@socketio.on("message_seen")
def message_seen(message_id, room_id):
    raise Exception("Not implemented")


@socketio.on("message_updated")
def message_updated(message_id, payload, room_id):
    raise Exception("Not implemented")


@socketio.on("message_deleted")
def message_deleted(message_id, room_id):
    raise Exception("Not implemented")
