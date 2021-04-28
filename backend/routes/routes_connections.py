from flask import Blueprint
from flask_login import login_required


from models import db, User


connection_routes = Blueprint("connections", __name__, url_prefix="/api/v1/users")


# POST https://surprise-me.benbolt.house/api/v1/users/<user_id>/connections/new/<recipient_id>
# Creates a new unestablished user connection with another user by
# recipient ID. In order to leverage connection interactivity the recipient
# must approve the requested connection beforehand.
@connection_routes.route("/<user_id>/connections/new/<recipient_id>", methods=["POST"])
@login_required
def post(user_id, recipient_id):
    raise Exception("Not implemented")


# GET https://surprise-me.benbolt.house/api/v1/users/<user_id>/connections
# Retrieves all of a logged in user's own pending and approved connections.
@connection_routes.route("/<user_id>/connections", methods=["GET"])
@login_required
def get(user_id):
    raise Exception("Not implemented")


# PATCH https://surprise-me.benbolt.house/api/v1/users/<user_id>/connections/<id>/approve
# Updates an unestablished connection to an established state via recipient
# approval. The user must be the recipient of the connection.
@connection_routes.route("/<user_id>/connections/<id>/approve", methods=["PATCH"])
@login_required
def patch_approve(user_id, id):
    raise Exception("Not implemented")


# PATCH https://surprise-me.benbolt.house/api/v1/users/<user_id>/connections/<id>/deny
# Updates an unestablished connection to a refused state via recipient
# denial. The user must be the recipient of the connection.
@connection_routes.route("/<user_id>/connections/<id>/deny", methods=["PATCH"])
@login_required
def patch_deny(user_id, id):
    raise Exception("Not implemented")


# DELETE https://surprise-me.benbolt.house/api/v1/users/<user_id>/connections/<id>
# Performs a soft delete of the connection in the database.
@connection_routes.route("/<user_id>/connections/<id>", methods=["DELETE"])
@login_required
def delete_soft(user_id, id):
    raise Exception("Not implemented")


# DELETE https://surprise-me.benbolt.house/api/v1/users/<user_id>/connections/<id>/hard
# Performs a hard delete of the connection from the database.
@connection_routes.route("/<user_id>/connections/<id>/hard", methods=["DELETE"])
@login_required
def delete_hard(user_id, id):
    raise Exception("Not implemented")
