from flask import Blueprint
from flask_socketio import send


from app import socketio


error_routes = Blueprint("errors_routes", __name__)


# EVENT error
# Captures all error events and sends them back to the client.
@socketio.on_error_default
def event_error_default(error):
    send(error)
