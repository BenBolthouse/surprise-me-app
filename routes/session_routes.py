from flask import Blueprint, request, jsonify
from flask_login import login_user


from models import User


session_routes = Blueprint("sessions", __name__, url_prefix="/api/sessions")


@session_routes.route("", methods=["POST"])
def post_session():

    # Find user in data store
    email = request.json["email"]
    user = User.query.filter(User.email == email).first()

    # Respond 404 if user not found
    user_not_found = user is None
    if user_not_found:
        return jsonify({
            "message": "user_not_found",
            "data": {
                "details": f"A user does not exist with the email address {email}."  # noqa
            },
        }), 404

    # Respond 400 if password is invalid
    password = request.json["password"]
    password_is_invalid = user.password_is_valid(password) is False
    if password_is_invalid:
        return jsonify({
            "message": "password_is_invalid",
        }), 400

    # If successful log the user in
    login_user(user)

    # Respond 200 if successful
    return jsonify({
        "message": "success",
        "data": user.to_json_on_login()
    }), 200
