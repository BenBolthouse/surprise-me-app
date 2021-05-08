from datetime import datetime
from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required, logout_user
from werkzeug.exceptions import InternalServerError


from models import db, User


# validation decorators
from validation import user_validate_on_post
from validation import user_validate_on_patch
from validation import user_validate_on_patch_password
from validation import user_validate_on_patch_email


user_routes = Blueprint("user_routes", __name__, url_prefix="/api/v1/users")


# POST https://surprise-me.benbolt.house/api/v1/users
# Creates a new unverified user in the database. Email verification is
# required for the user to login and begin using the application.
@user_routes.route("", methods=["POST"])
@user_validate_on_post()
def post():
    get = request.json.get

    user = User(
        first_name=get("first_name"),
        last_name=get("last_name"))

    db.session.add(user)

    db.session.commit()

    user.set_active_email_address(get("email"))

    user.set_active_password(get("password"))

    db.session.commit()

    return jsonify({
        "message": "User created successfully",
        "data": user.to_dict(),
    }), 201


# GET https://surprise-me.benbolt.house/api/v1/users
# Retrieves a logged in user's own profile data.
@user_routes.route("", methods=["GET"])
@login_required
def get():
    return jsonify({
        "message": "Success",
        "data": current_user.to_dict(),
    }), 200


# PATCH https://surprise-me.benbolt.house/api/v1/users
# Updates a logged in user's own simple profile data.
@user_routes.route("", methods=["PATCH"])
@user_validate_on_patch()
@login_required
def patch():
    json = request.json.get

    session_user.update(
        first_name=json("first_name"),
        last_name=json("last_name"))

    db.session.commit()

    return jsonify({
        "message": "User updated successfully",
        "data": current_user.to_dict(),
    }), 200


# PATCH https://surprise-me.benbolt.house/api/v1/users/password
# Updates a logged in user's own password requiring a new session.
# This route is used in the workflow requiring a user to be currently
# logged in, not to be confused with a forgot my password scenario.
@user_routes.route("/password", methods=["PATCH"])
@user_validate_on_patch_password()
@login_required
def patch_password():
    json = request.json.get

    try:
        session_user.set_active_password(json("password"))

    except Exception as exception:
        raise BadRequest(response="You have already used this password. Please try another.")

    db.session.commit()

    return jsonify({
        "message": "Password updated successfully",
    }), 200


# PATCH https://surprise-me.benbolt.house/api/v1/users/email
# Updates a logged in user's own password requiring a new email
# verification.
@user_routes.route("/email", methods=["PATCH"])
@user_validate_on_patch_email()
@login_required
def patch_email(id):
    json = request.json.get

    try:
        # * Important to prevent users with fake unverified email
        # * addresses having continued authorized access.
        logout_user()

        session_user.set_active_email_address(json("email"))

    except Exception as exception:
        raise BadRequest(response="You have already used this email address. Please try another.")

    db.session.commit()

    return jsonify({
        "message": "Email updated successfully",
    }), 200


# DELETE https://surprise-me.benbolt.house/api/v1/users
# Performs a soft delete of the user's profile in the database.
@user_routes.route("", methods=["DELETE"])
@login_required
def delete_soft(id):
    # * The user has opted out of further sessions and this session
    # * must be deleted.
    logout_user()

    session_user.set_deleted_at()

    db.session.commit()

    return jsonify({
        "message": "User was successfully removed",
    }), 200


# DELETE https://surprise-me.benbolt.house/api/v1/users/hard
# Performs a hard delete of the user's profile from the database.
@user_routes.route("/hard", methods=["DELETE"])
@login_required
def delete_hard(id):
    raise Exception("Not implemented")
