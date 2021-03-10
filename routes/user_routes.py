from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user


from models import db, User


from .user_routes_validation_password import validate_password_update
from .user_routes_validation import user_validate_on_post, user_validate_on_patch  # noqa

user_routes = Blueprint("users", __name__, url_prefix="/api/users")


@user_routes.route("", methods=["POST"])
@user_validate_on_post()
def post_user():

    # Respond 400 if requested email is in use
    User.check_is_email_unique(request.json.get("email"))

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
        "message": "Success",
        "data": user.to_json_on_create()
    }), 201


@user_routes.route("", methods=["PATCH"])
@login_required
@user_validate_on_patch()
def patch_user():

    # Get user
    user = User.get_by_id(current_user.id)

    # Respond 400 if requested email is in use
    User.check_is_email_unique(request.json.get("email"))

    # Catch requests to update password
    password = request.json.get("password")
    if password:
        validate_password_update(password)
        user.password = password
        db.session.commit()
        return jsonify({
            "message": "Password updated successfully."
        }), 200

    # Convert camel to snake and update user object
    user.first_name = request.json.get("firstName") or user.first_name
    user.last_name = request.json.get("lastName") or user.last_name
    user.email = request.json.get("email") or user.email
    user.coord_lat = request.json.get("coordLat") or user.coord_lat
    user.coord_long = request.json.get("coordLong") or user.coord_long

    # Special case for booleans
    share_location = request.json.get("shareLocation")
    user.share_location = True if share_location is True else False

    # Commit to the store
    db.session.commit()

    # Respond 200 if successful
    return jsonify({
        "message": "Success",
        "data": user.to_json_on_patch()
    }), 200


@user_routes.route("/is_email_unique", methods=["POST"])
def is_email_unique():

    # Check if the email is in use
    User.is_email_unique(request.json.get("email"))

    # Respond 200 if successful
    return jsonify({
        "message": "Email is unique.",
    }), 200
