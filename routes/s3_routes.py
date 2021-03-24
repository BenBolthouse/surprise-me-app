from flask import Blueprint, request, send_file
from werkzeug.exceptions import NotFound
import os


from utilities import upload_file, download_file
from config import Config
import routes


s3_routes = Blueprint("s3_routes", __name__, url_prefix="/f")


@s3_routes.route("", methods=["POST"])
def upload_a_file():
    file_object = request.files["file"]
    file_name = request.form["filename"]

    file_uploaded = upload_file(file_name, file_object)

    if file_uploaded:
        return {
            "message": "success",
            "data": {
                "path": f"{Config.HOST_NAME}/f/{file_name}"  # noqa
            }
        }, 201
    else:
        return {
            "message": "file_upload_error",
        }, 500


@s3_routes.route("/<path:file_name>", methods=["GET"])
def download_a_file(file_name):
    response = download_file(file_name)

    # Catch 404
    if response is False:
        raise NotFound(response={
            "message": "File not found",
        })

    # Send file in response
    return response
