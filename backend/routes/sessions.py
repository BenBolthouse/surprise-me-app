from datetime import datetime
from flask import current_app, Blueprint, jsonify, make_response, request
from flask_login import current_user, login_required, login_user, logout_user
from flask_socketio import join_room, leave_room, send
from flask_wtf.csrf import generate_csrf
from socketio.exceptions import ConnectionRefusedError
from werkzeug.exceptions import BadRequest

from .utilities.decode_session_cookie import decode_session_cookie
from app import socketio
from models import Email, User


session_routes = Blueprint("session_routes", __name__, url_prefix="/api/v1/sessions")


# POST https://surprise-me.benbolt.house/api/v1/sessions
# Creates a new user session and sends a session cookie to the client.
@session_routes.route("", methods=["POST"])
def post():
    if current_user.is_active:
        raise BadRequest(response={
            "notification": {
                "body": "You are already signed in.",
                "type": "popup",
                "deladurationy": 3,
            },
        })

    json = request.json.get

    email = Email.query.filter(Email.value == json("email")).first()

    if not email:
        raise BadRequest(response={
            "notification": {
                "body": "Invalid email address",
                "type": "popup",
                "duration": 3,
            },
        })

    if email.is_deleted:
        raise BadRequest(response={
            "notification": {
                "body": "Email address is expired. Please use the email address associated with your account.",
                "type": "popup",
                "duration": 5,
            },
        })

    user = User.query.get(email.user_id)

    password_is_valid = user.active_password.validate(json("password"))

    if not password_is_valid:
        raise BadRequest(response={
            "notification": {
                "body": "Invalid password",
                "type": "popup",
                "duration": 3,
            },
        })

    login_user(user)

    return jsonify({
        "data": {
            "active": True,
            "timestamp": datetime.now().isoformat(),
        },
        "notification": {
            "body": f"Welcome back, {user.first_name}!",
            "type": "popup",
            "duration": 2,
            "importance": "success",
        },
    }), 201


# GET https://surprise-me.benbolt.house/api/v1/sessions/csrf
# Issues a new anti CSRF token to the client in a JSON body.
@session_routes.route("/csrf", methods=["GET"])
def getCsrf():
    return jsonify({
        "data": {
            "csrf_token": generate_csrf(),
        },
    }), 200


# GET https://surprise-me.benbolt.house/api/v1/sessions
# Retrieves session data and sends to the client if authenticated,
# otherwise sends an OK response without data. This prevents error code
# responses if the user isn't logged in.
@session_routes.route("", methods=["GET"])
def get():
    if current_user.is_active:
        data = {
            "active": True,
            "timestamp": datetime.now().isoformat(),
        }
    else:
        data = {
            "active": False,
            "timestamp": datetime.now().isoformat(),
        }

    return jsonify({
        "data": data,
    }), 200


# DELETE https://surprise-me.benbolt.house/api/v1/sessions
# Deletes the session via deletion of the session cookie on the response to
# the client.
@session_routes.route("", methods=["DELETE"])
@login_required
def delete():
    response = make_response({
        "notification": {
            "body": "You have signed out",
            "type": "popup",
            "duration": 3,
        },
    })

    logout_user()

    test = response.delete_cookie("session", path="/")

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
# Removes a user from a room.
@socketio.on("leave")
def connect(payload):
    room_id = payload["room_id"]

    join_room(room_id)

    send(f"Client left room '{room_id}'")
