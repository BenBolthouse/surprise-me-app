from flask import Blueprint
from flask_socketio import emit, send


from app import socketio


socket_connection_events = Blueprint("connections", __name__)

# TODO @socketio.on("connect")
# get session token from the initial request before upgrading protocols
#   perform user authentication with the token
#       if invalid then reject the connection
#       inform client
#       else establish the connection
#       inform client

# TODO @socketio.on("disconnect")
# allow client to disconnect
