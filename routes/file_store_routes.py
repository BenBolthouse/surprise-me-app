from utilities import aws_s3
from flask import Blueprint, request, send_file
import os


from config import Config
from utilities import aws_s3
import routes


UPLOAD_FOLDER = "uploads"
BUCKET = "surprise-me-file-store"

file_store_routes = Blueprint(
    "file_store_routes",
    __name__,
    url_prefix="/file_store")


@file_store_routes.route("<path:file_name>", methods=["GET"])
def download_file(file_name):
    file_path = f"/{file_name}"
    routes_abs_path = os.path.dirname(routes.__file__)
    download_folder = f"{routes_abs_path}/files/{file_name}"
    try:
        file_response = aws_s3.download(file_path, BUCKET, download_folder)
    except Exception as e:
        print(e)

    return send_file(
        download_folder,
        as_attachment=True,
        attachment_filename=file_name), 200


@file_store_routes.route("", methods=["POST"])
def upload_file():
    form_file = request.files["file"]
    form_filename = request.form["filename"]

    this_dir = os.path.dirname(__file__)
    temp_file_dir = os.path.join(this_dir, "files")
    temp_filepath = os.path.join(temp_file_dir, form_filename)

    # Save file to temp file directory
    form_file.save(temp_filepath)

    # Upload to AWS S3
    aws_s3.upload(temp_filepath, BUCKET, os.path.join("/", form_filename))

    return {
        "message": "success",
        "data": {
            "path": f"{Config.HOST_NAME}/file_store_routes/{form_filename}"  # noqa
        }
    }, 201
