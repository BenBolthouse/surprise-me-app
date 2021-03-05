from flask import Blueprint, session, make_response
from flask_wtf.csrf import generate_csrf, session as csrf_session


from .route_decorator import RouteDecorator


csrf_routes = Blueprint("csrf", __name__, url_prefix="/api/csrf")


@csrf_routes.route("", methods=["GET"])
def get_new_csrf_token():
    """ Creates and sends a csrf token response. """

    return {
        "message": "success",
        "data": {
            "token": generate_csrf()
        }
    }, 200
