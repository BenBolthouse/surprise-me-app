from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user, login_user


from models import db, User


from .user_routes_validation_password import validate_password_update
from .user_routes_validation import user_validate_on_post
from .user_routes_validation import user_validate_on_patch

user_routes = Blueprint("users", __name__, url_prefix="/api/users")


# ** «««««««««««««««« POST Routes »»»»»»»»»»»»»»»» **


@user_routes.route("", methods=["POST"])
@user_validate_on_post()
def post_user():

    # Properties from JSON request
    config_object = {
        "password": request.json.get("password"),
        "email": request.json.get("email"),
        "first_name": request.json.get("first_name"),
        "last_name": request.json.get("last_name"),
        "email": request.json.get("email"),
        "share_location": request.json.get("share_location"),
        "coord_lat": request.json.get("coord_lat"),
        "coord_long": request.json.get("coord_long"),
    }

    # Respond 400 if requested email is already in use
    User.email_address_is_unique(config_object["email"])

    # Create the user and commit
    user = User(config_object)
    db.session.add(user)
    db.session.commit()

    # Automatically log in
    login_user(user)

    # Respond 201 if successful
    return jsonify({
        "message": "Success",
        "data": session_user.to_json()
    }), 201


@user_routes.route("/is_email_unique", methods=["POST"])
def is_email_unique():

    # Respond 400 if requested email is already in use
    User.email_address_is_unique(request.json.get("email"))

    # Respond 200 if successful
    return jsonify({
        "message": "The requested email is available for use.",
    }), 200


# ** «««««««««««««««« PATCH Routes »»»»»»»»»»»»»»»» **


@user_routes.route("", methods=["PATCH"])
@login_required
@user_validate_on_patch()
def patch_user():

    # Get session user
    session_user = current_user

    # Properties from JSON request
    config_object = {
        "password": request.json.get("password"),
        "first_name": request.json.get("firstName"),
        "last_name": request.json.get("lastName"),
        "email": request.json.get("email"),
        "share_location": request.json.get("shareLocation"),
        "coord_lat": request.json.get("coordLat"),
        "coord_long": request.json.get("coordLong"),
    }

    # Respond 400 if requested email is already in use
    User.email_address_is_unique(config_object["email"])

    # Handle special requests to update password
    if config_object["password"]:
        validate_password_update(password)
        session_user.password = password
        db.session.commit()
        return jsonify({
            "message": "Password updated successfully."
        }), 200

    # Convert camel to snake and update user object
    session_user.update(config_object)

    # Commit to the store
    db.session.commit()

    # Respond 200 if successful
    return jsonify({
        "message": "Success",
        "data": session_user.to_json()
    }), 200
