from flask import Blueprint, jsonify
from flask_wtf.csrf import generate_csrf


csrf_routes = Blueprint("csrf_routes", __name__, url_prefix="/api/v1/csrf_token")


# GET https://surprise-me.benbolt.house/api/v1/csrf_token
# Issues a new anti CSRF token to the client in a JSON body.
@csrf_routes.route("", methods=["GET"])
def post():
    return jsonify({
        "message": "Success",
        "data": generate_csrf(),
    }), 200
