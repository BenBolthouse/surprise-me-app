from flask import Blueprint
from flask_login import login_required

from .utils import upload_file, download_file


file_routes = Blueprint("file_routes", __name__, url_prefix="/file/v1")


# POST https://surprise-me.benbolt.house/file/v1
# Accepts a file object for upload and persists to cloud storage.
@file_routes.route("", methods=["POST"])
@login_required
def post():
    raise Exception("Not implemented")


# POST https://surprise-me.benbolt.house/file/v1
# Retrieves and sends a file from cloud storage.
@file_routes.route("", methods=["GET"])
@login_required
def get():
    raise Exception("Not implemented")
