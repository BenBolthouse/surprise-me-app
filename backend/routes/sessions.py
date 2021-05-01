from flask import Blueprint, jsonify, make_response, request
from flask_login import login_required, login_user
from werkzeug.exceptions import BadRequest


from models import Email, User


session_routes = Blueprint("session_routes", __name__, url_prefix="/api/v1/sessions")


# POST https://surprise-me.benbolt.house/api/v1/session
# Creates a new user session and sends a session cookie to the client.
@session_routes.route("", methods=["POST"])
def post():
    json = request.json.get

    email = Email.query.filter(Email.value == json("email")).first()

    if email.is_deleted:
        raise BadRequest(response={
            "message": "Email is expired",
        })

    user = User.query.get(email.user)

    password_is_valid = user.active_password.validate(json("password"))

    if not password_is_valid:
        raise BadRequest(response={
            "message": "Email is expired",
        })

    login_user(user)

    return jsonify({
        "message": "Success",
    }), 201


# DELETE https://surprise-me.benbolt.house/api/v1/session
# Deletes the session via deletion of the session cookie on the response to
# the client.
@session_routes.route("", methods=["DELETE"])
@login_required
def delete():
    response = make_response({"message": "Success"})
    response.delete_cookie("session")
    return response
