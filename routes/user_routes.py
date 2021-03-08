from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user


from models import db, User


from .user_routes_validation import user_validate_on_post, user_validate_on_patch  # noqa

user_routes = Blueprint("users", __name__, url_prefix="/api/users")


@user_routes.route("", methods=["POST"])
@user_validate_on_post()
def post_user():

    # Respond 400 if body data validation failed
    body_data_validation_failed = request.validation_result is False
    if body_data_validation_failed:
        return jsonify({
            "message": "Data validation failed on user POST",
            "data": request.validation_errors
        }), 400

    # Respond 400 if requested email is in use
    email = request.json["email"]
    requested_email_is_in_use = User.query.filter(
        User.email == email).first()
    if requested_email_is_in_use:
        return jsonify({
            "message": "Email conflict",
            "data": {
                "details": f"The email {email} is already in use."
            }
        }), 400

    # Create the user and commit
    user = User({
        "password": request.json.get("password"),
        "first_name": request.json.get("firstName"),
        "last_name": request.json.get("lastName"),
        "email": request.json.get("email"),
        "share_location": request.json.get("shareLocation"),
        "coord_lat": request.json.get("coordLat"),
        "coord_long": request.json.get("coordLong"),
    })
    db.session.add(user)
    db.session.commit()

    # Respond 201 if successful
    return jsonify({
        "message": "success",
        "data": user.to_json_on_create()
    }), 201


@user_routes.route("", methods=["GET"])
@login_required
def get_session_user():
    return jsonify({
        "message": "success",
        "data": current_user.to_json_on_session_get()
    }), 200


@user_routes.route("", methods=["PATCH"])
@login_required
@user_validate_on_patch()
def patch_user():

    # Get session user
    user = current_user

    # Respond 400 if body data validation failed
    body_data_validation_failed = request.validation_result is False
    if body_data_validation_failed:
        return jsonify({
            "message": "Data validation failed on user PATCH",
            "data": request.validation_errors
        }), 400

    # Respond 400 if requested email is in use
    email = request.json.get("email")
    if email is not None:
        requested_email_is_in_use = User.query.filter(
            User.email == email).first()
        if requested_email_is_in_use:
            return jsonify({
                "message": "Email conflict",
                "data": {
                    "details": f"The email {email} is already in use."
                }
            }), 400

    # Convert camel to snake and update user object
    user.first_name = request.json.get("firstName") or user.first_name
    user.last_name = request.json.get("lastName") or user.last_name
    user.email = request.json.get("email") or user.email
    user.coord_lat = request.json.get("coordLat") or user.coord_lat
    user.coord_long = request.json.get("coordLong") or user.coord_long

    # Special case for booleans
    if request.json.get("shareLocation") is True:
        user.share_location = True
    if request.json.get("shareLocation") is False:
        user.share_location = False

    # Commit to the store
    db.session.commit()

    # Respond 200 if successful
    return jsonify({
        "message": "success",
        "data": user.to_json_on_patch()
    }), 200
