from flask import Blueprint
from flask_socketio import emit, send


from app import socketio


error_events = Blueprint("error_events", __name__)


@socketio.on_error_default
def error(error):
    send({
        "message": "There was an error with your request.",
        "data": {
            "details": error,
        },
    })
