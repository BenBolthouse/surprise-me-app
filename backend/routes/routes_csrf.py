from flask import Blueprint, jsonify
from flask_wtf.csrf import generate_csrf


csrf_routes = Blueprint("csrf", __name__, url_prefix="/api/v1/csrf_token")


# GET https://surprise-me.benbolt.house/api/v1/csrf_token
# Issues a new anti CSRF token to the client in a JSON body.
@csrf_routes.route("", methods=["POST"])
def post():
    return jsonify({
        "message": "Success",
        "data": {
            "token": generate_csrf()
        }
    }), 200
