from flask import Blueprint, make_response
from flask_login import login_required


from models import User


session_routes = Blueprint("sessions", __name__, url_prefix="/api/sessions")


# POST https://surprise-me.benbolt.house/api/v1/session
# Creates a new user session and sends a session cookie to the client.
@session_routes.route("", methods=["POST"])
def post():
    raise Exception("Not implemented")


# GET https://surprise-me.benbolt.house/api/v1/session
# Retrieves the logged in user's own session and returns profile data to
# the client.
@session_routes.route("", methods=["GET"])
@login_required
def get():
    raise Exception("Not implemented")


# DELETE https://surprise-me.benbolt.house/api/v1/session
# Deletes the session via deletion of the session cookie on the response to
# the client.
@session_routes.route("", methods=["DELETE"])
@login_required
def delete():
    response = make_response({"message": "Success"})
    response.delete_cookie("session")
    return response
