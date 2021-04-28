from flask import Blueprint, jsonify, request
from flask_login import login_required
from werkzeug.exceptions import BadRequest, InternalServerError


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
    try:
        # Two units of work exist here because a commit to the database is
        # initially needed in order to get the user ID from the sequence. The
        # ID is needed to establish a relationship with the newly created user
        # and the user's email address and password.
        body = request.json.get
        user = User(body("first_name"), body("last_name"))

        db.session.add(user)
        db.session.commit()

        user.active_email_address = body("email")
        user.active_password = body("password")

        db.session.add(user)
        db.session.commit()

    except(Exception) as exception:
        raise InternalServerError("Exception raised while trying to create a new user.")

    return jsonify({
        "message": "User created successfully",
    })


# GET https://surprise-me.benbolt.house/api/v1/users/<id>
# Retrieves a logged in user's own profile data.
@user_routes.route("/<id>", methods=["GET"])
@login_required
def get(id):
    # First check is if the session user is requesting their own account. A
    # bit redundant but it's following the RESTful convention of
    # <collection>/<item_id>.
    if user.id != current_user.id:
        raise BadRequest(
            "This API endpoint only allows retrieval of a user's own profile data. Use the logged in user's ID in the URL for the request.")

    try:
        user = User.query.get(int(id))

    except(Exception) as exception:
        raise BadRequest("The user with the provided id was not found.")

    return jsonify({
        "message": "Success",
        "data": {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.active_email_address,
        }
    }), 200


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


# What are these doing here?!?!
# These look like connections routes; they actually modify the state of a
# user's connections collection, more so than they modify any particular
# connection. Therefore, they exist here. It's more RESTful!


# POST https://surprise-me.benbolt.house/api/v1/users/<id>/connections/new/<recipient_id>
# Creates a new unestablished user connection with another user by
# recipient ID. In order to leverage connection interactivity the recipient
# must approve the requested connection beforehand.
# ...
# Approval routes are found in the connections router, they aren't here! :)
@connection_routes.route("/<id>/connections/add/<recipient_id>", methods=["POST"])
@login_required
def post(id, recipient_id):
    raise Exception("Not implemented")


# GET https://surprise-me.benbolt.house/api/v1/users/<id>/connections
# Retrieves all of a logged in user's own pending and approved connections.
@connection_routes.route("/<id>/connections", methods=["GET"])
@login_required
def get(id):
    raise Exception("Not implemented")
