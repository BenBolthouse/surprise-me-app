from flask import Blueprint
from flask_login import login_required


from models import db, User


# validation decorators
from validation import user_validate_on_post
from validation import user_validate_on_patch
from validation import user_validate_on_patch_password
from validation import user_validate_on_patch_email


user_routes = Blueprint("users", __name__, url_prefix="/api/v1/users")


# POST https://surprise-me.benbolt.house/api/v1/users
# Creates a new unverified user in the database. Email verification is
# required for the user to login and begin using the application.
@user_routes.route("", methods=["POST"])
@user_validate_on_post()
def post():
    raise Exception("Not implemented")


# GET https://surprise-me.benbolt.house/api/v1/users/<id>
# Retrieves a logged in user's own profile data.
@user_routes.route("/<id>", methods=["GET"])
@login_required
def get(id):
    raise Exception("Not implemented")


# PATCH https://surprise-me.benbolt.house/api/v1/users/<id>
# Updates a logged in user's own simple profile data.
@user_routes.route("/<id>", methods=["PATCH"])
@user_validate_on_patch()
@login_required
def patch(id):
    raise Exception("Not implemented")


# PATCH https://surprise-me.benbolt.house/api/v1/users/<id>/password
# Updates a logged in user's own password requiring a new session.
# This route is used in the workflow requiring a user to be currently
# logged in, not to be confused with a forgot my password scenario.
@user_routes.route("/<id>/password", methods=["PATCH"])
@user_validate_on_patch_password()
@login_required
def patch_password(id):
    raise Exception("Not implemented")


# PATCH https://surprise-me.benbolt.house/api/v1/users/email
# Updates a logged in user's own password requiring a new email
# verification.
@user_routes.route("/<id>/email", methods=["PATCH"])
@user_validate_on_patch_email()
@login_required
def patch_email(id):
    raise Exception("Not implemented")


# DELETE https://surprise-me.benbolt.house/api/v1/users/<id>
# Performs a soft delete of the user's profile in the database.
@user_routes.route("/<id>", methods=["DELETE"])
@login_required
def delete_soft(id):
    raise Exception("Not implemented")


# DELETE https://surprise-me.benbolt.house/api/v1/users/<id>/hard
# Performs a hard delete of the user's profile from the database.
@user_routes.route("/<id>/hard", methods=["DELETE"])
@login_required
def delete_hard(id):
    raise Exception("Not implemented")
