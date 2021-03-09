from flask import Blueprint, request, jsonify
from flask_login import login_user


from models import User


session_routes = Blueprint("sessions", __name__, url_prefix="/api/sessions")


@session_routes.route("", methods=["POST"])
def post_session():

    # Find user in data store
    user = User.get_by_email(request.json.get("email"))

    # Respond 400 if password is invalid
    user.password_is_valid(request.json.get("password"))

    # If successful log the user in
    login_user(user)

    # Respond 200 if successful
    return jsonify({
        "message": "success",
        "data": user.to_json_on_login()
    }), 200
