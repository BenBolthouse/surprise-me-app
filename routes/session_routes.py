from flask import Blueprint, request, jsonify
from flask_login import login_user, current_user, login_required


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
        "message": "Success",
        "data": user.to_json_on_login()
    }), 200


@session_routes.route("", methods=["GET"])
@login_required
def get_session():

    # Respond 200
    return jsonify({
        "message": "Success",
        "data": {
            "id": current_user.id,
            "firstName": current_user.first_name,
            "lastName": current_user.last_name,
            "email": current_user.email,
            "shareLocation": current_user.share_location,
            "coordLat": str(current_user.coord_lat),
            "coordLong": str(current_user.coord_long),
        }
    }), 200


@session_routes.route("/unauthorized")
@login_required
def unauthorized():

    # Respond 401
    return jsonify({
        "message": "Unauthorized",
    }), 401
