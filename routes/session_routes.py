from flask import Blueprint, request, jsonify, make_response
from flask_login import login_user, current_user, login_required


from models import User


session_routes = Blueprint("sessions", __name__, url_prefix="/api/sessions")


# ** «««««««««««««««« POST Routes »»»»»»»»»»»»»»»» **


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
        "message": "Success",
        "data": user.to_json()
    }), 200


# ** «««««««««««««««« GET Routes »»»»»»»»»»»»»»»» **


@session_routes.route("", methods=["GET"])
@login_required
def get_session():

    # Respond 200
    return jsonify({
        "message": "Success",
        "data": current_user.to_json()
    }), 200


# ** «««««««««««««««« DELETE Routes »»»»»»»»»»»»»»»» **


@session_routes.route("", methods=["DELETE"])
@login_required
def delete_session():

    # Delete cookie in response
    response = make_response({
        "message": "Success",
    })
    response.delete_cookie("session")

    # Respond 200
    return response
