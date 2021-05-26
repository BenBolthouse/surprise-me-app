from flask import Blueprint, request
from flask_login import login_required
from werkzeug import secure_filename
from os import path

from .utilities import random_string

file_routes = Blueprint("file_routes", __name__, url_prefix="/file/v1")


# POST https://surprise-me.benbolt.house/file/v1/t
# Accepts a file object and persists to temporary storage. Returns the
# filename for frontend followup downloads.
@file_routes.route("/t", methods=["POST"])
def post_temp():
    file = request.files[0]

    filename = random_string(16)

    file.save(path.join("..", "temp", filename))

    return jsonify({
        "data": filename,
    }), 201


# POST https://surprise-me.benbolt.house/file/v1
# Retrieves and sends a file from cloud storage.
@file_routes.route("/t", methods=["GET"])
@login_required
def get():
    raise Exception("Not implemented")
