from datetime import datetime
from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required, logout_user
from werkzeug.exceptions import BadRequest


from models import db, User, Email


# validation decorators
from validation import user_validate_on_post
from validation import user_validate_on_patch
from validation import user_validate_on_patch_password
from validation import user_validate_on_patch_email


user_routes = Blueprint("user_routes", __name__, url_prefix="/api/v1/users")

# GET https://surprise-me.benbolt.house/api/v1/users/check_email_is_unique?email=<email>
# Determines if an email is in use and responds accordingly.
@user_routes.route("/check_email_is_unique", methods=["POST"])
def check_email_is_unique():
    get = request.args.get

    email = get("email")

    if Email.query.filter(Email.value == email).first():
        raise BadRequest(response={
            "notification": {
                "body": f"The email address {email} is already in use. Do you already have an account?",
                "type": "card_notifications",
                "action_label": "Sign in here",
                "action": f"/sign_in?email={email}",
            }
        })

    return {}, 200

# POST https://surprise-me.benbolt.house/api/v1/users
# Creates a new unverified user in the database. Email verification is
# required for the user to login and begin using the application.
@user_routes.route("", methods=["POST"])
@user_validate_on_post()
def post():
    get = request.json.get

    user = User()
    user.first_name = get("first_name")
    user.last_name = get("last_name")
    user.bio = get("bio")

    db.session.add(user)
    db.session.commit()

    user.set_active_email_address(get("email"))
    user.set_active_password(get("password"))

    db.session.commit()

    return jsonify({
        "data": {
            **current_user.to_dict(),
            "password": None,
            "confirm_password": None,
        },
        "notification": {
            "body": f"Welcome, {user.first_name}!",
            "type": "card_notifications",
            "action_label": "Take me to Surprise Me",
            "action": "/#/home",
        },
    }), 201


# GET https://surprise-me.benbolt.house/api/v1/users
# Retrieves a logged in user's own profile data.
@user_routes.route("", methods=["GET"])
@login_required
def get():
    return jsonify({
        "data": current_user.to_dict(),
    }), 200


# PATCH https://surprise-me.benbolt.house/api/v1/users
# Updates a logged in user's own simple profile data.
@user_routes.route("", methods=["PATCH"])
@user_validate_on_patch()
@login_required
def patch():
    get = request.json.get

    current_user.first_name = get("first_name")
    current_user.last_name = get("last_name")
    current_user.bio = get("bio")

    db.session.commit()

    return jsonify({
        "data": current_user.to_dict(),
        "notification": {
            "body": "Your profile has been updated.",
            "type": "popup_notifications",
            "delay": 3,
        }
    }), 200


# PATCH https://surprise-me.benbolt.house/api/v1/users/password
# Updates a logged in user's own password requiring a new session.
# This route is used in the workflow requiring a user to be currently
# logged in, not to be confused with a forgot my password scenario.
@user_routes.route("/password", methods=["PATCH"])
@user_validate_on_patch_password()
@login_required
def patch_password():
    get = request.json.get

    try:
        current_user.set_active_password(get("password"))

    except Exception as exception:
        raise BadRequest(response={
            "notification": {
                "body": "You have already used this password. Please use another.",
                "type": "popup_notifications",
                "delay": 3,
            }
        })

    db.session.commit()

    return jsonify({
        "data": {
            "password": None,
            "confirm_password": None,
        },
        "notification": {
            "body": "Your password has been updated",
            "type": "popup_notifications",
            "delay": 3,
        }
    }), 200


# PATCH https://surprise-me.benbolt.house/api/v1/users/email
# Updates a logged in user's own password requiring a new email
# verification.
@user_routes.route("/email", methods=["PATCH"])
@user_validate_on_patch_email()
@login_required
def patch_email(id):
    get = request.json.get

    try:
        session_user.set_active_email_address(get("email"))

    except Exception as exception:
        raise BadRequest(response={
            "notification": {
                "body": "You have already used this email address. Please use another.",
                "type": "popup_notifications",
                "delay": 3,
            }
        })

    db.session.commit()

    logout_user()

    return jsonify({
        "notification": {
            "body": "Email updated successfully. You have been signed out until you verify your email address. Please check your email for the verification link.",
            "type": "card_notifications",
        }
    }), 200


# DELETE https://surprise-me.benbolt.house/api/v1/users
# Performs a soft delete of the user's profile in the database.
@user_routes.route("", methods=["DELETE"])
@login_required
def delete_soft(id):
    session_user.set_deleted_at()

    db.session.commit()

    logout_user()

    return jsonify({
        "notification": {
            "body": "Your account has been deleted",
            "type": "popup_notifications",
            "delay": 3,
        }
    }), 200


# DELETE https://surprise-me.benbolt.house/api/v1/users/hard
# Performs a hard delete of the user's profile from the database.
@user_routes.route("/hard", methods=["DELETE"])
@login_required
def delete_hard(id):
    raise Exception("Not implemented")
