from flask import current_app, Blueprint, jsonify, make_response, request
from flask_login import current_user, login_required, login_user
from flask_socketio import join_room, leave_room, send
from socketio.exceptions import ConnectionRefusedError
from werkzeug.exceptions import BadRequest

from .utilities.decode_session_cookie import decode_session_cookie
from app import socketio
from models import Email, User


session_routes = Blueprint("session_routes", __name__, url_prefix="/api/v1/sessions")


# POST https://surprise-me.benbolt.house/api/v1/session
# Creates a new user session and sends a session cookie to the client.
@session_routes.route("", methods=["POST"])
def post():
    json = request.json.get

    email = Email.query.filter(Email._value == json("email")).first()

    if not email:
        raise BadRequest(response={
            "message": "Invalid email",
        })

    if email.is_deleted:
        raise BadRequest(response={
            "message": "Email is expired",
        })

    user = User.query.get(email._user_id)

    password_is_valid = user.active_password.validate(json("password"))

    if not password_is_valid:
        raise BadRequest(response={
            "message": "Email is expired",
        })

    login_user(user)

    return jsonify({
        "message": "Success",
        "data": user.to_dict(),
    }), 201


# GET https://surprise-me.benbolt.house/api/v1/session Retrieves session
# data and sends to the client if authenticated, otherwise sends an OK
# response without data. This prevents error code responses if the user
# isn't logged in.
@session_routes.route("", methods=["GET"])
def get():
    if current_user.is_active:
        data = current_user.to_dict()
    else:
        data = {}

    return jsonify({
        "message": "Success",
        "data": data,
    }), 200


# DELETE https://surprise-me.benbolt.house/api/v1/session
# Deletes the session via deletion of the session cookie on the response to
# the client.
@session_routes.route("", methods=["DELETE"])
@login_required
def delete():
    response = make_response({"message": "Success"})
    response.delete_cookie("session")
    return response


# EVENT connect
# Creates a socket connection with the server. Connection event will be
# rejected if a session cannot be decoded.
@socketio.on("connect")
def connect():
    cookie = request.cookies.get("session")

    try:
        decode_session_cookie(cookie)
    except Exception:
        raise ConnectionRefusedError("Session is invalid")

    send("Client connected successfully")


# EVENT join
# Joins a user to a room.
@socketio.on("join")
def connect(payload):
    room_id = payload["room_id"]

    join_room(room_id)

    send(f"Client joined room '{room_id}'")


# EVENT leave
# Removes a user to a room.
@socketio.on("leave")
def connect(payload):
    room_id = payload["room_id"]

    join_room(room_id)

    send(f"Client left room '{room_id}'")
