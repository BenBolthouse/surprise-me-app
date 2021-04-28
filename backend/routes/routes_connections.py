from flask import Blueprint
from flask_login import login_required


from models import db, User


connection_routes = Blueprint("connections", __name__, url_prefix="/api/v1/connections")


# PATCH https://surprise-me.benbolt.house/api/v1/users/<user_id>/connections/<id>/approve
# Updates an unestablished connection to an established state via recipient
# approval. The user must be the recipient of the connection.
@connection_routes.route("/<id>/approve", methods=["PATCH"])
@login_required
def patch_approve(id):
    raise Exception("Not implemented")


# PATCH https://surprise-me.benbolt.house/api/v1/users/<user_id>/connections/<id>/deny
# Updates an unestablished connection to a refused state via recipient
# denial. The user must be the recipient of the connection.
@connection_routes.route("/<id>/deny", methods=["PATCH"])
@login_required
def patch_deny(id):
    raise Exception("Not implemented")


# DELETE https://surprise-me.benbolt.house/api/v1/users/<user_id>/connections/<id>
# Performs a soft delete of the connection in the database.
@connection_routes.route("/<id>", methods=["DELETE"])
@login_required
def delete_soft(user_id, id):
    raise Exception("Not implemented")


# DELETE https://surprise-me.benbolt.house/api/v1/users/<user_id>/connections/<id>/hard
# Performs a hard delete of the connection from the database.
@connection_routes.route("/<id>/hard", methods=["DELETE"])
@login_required
def delete_hard(user_id, id):
    raise Exception("Not implemented")
