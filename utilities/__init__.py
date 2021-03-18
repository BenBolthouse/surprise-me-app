from boto3 import resource
from flask import Response
import os

from config import Config


BUCKET_NAME = Config.S3_BUCKET


def normalize_to_dictionary(input_list):
    """
    Converts a list to a dictionary using list member id property as the
    output dictionary key.
    """

    output = {a["id"]: a for a in input_list}
    return output


def upload_file(file_name, file_object):
    """
    Upload a file to the S3 file store.

    String `file_name`: Name of the file from Flask.request.form

    FileStorage `file_object`: File object from Flask.request.form
    """

    # Put the request file or return false if an exception is raised
    try:
        s3 = resource('s3')
        file_result = s3.Object(BUCKET_NAME, file_name).put(Body=file_object)
    except Exception as e:
        return False

    # If successful return true
    return True


def download_file(file_name):
    """
    Download a file from the S3 file store returning `Flask.Response` with the
    requested file.

    String `file_name`: Name of the file as absolute path in S3 bucket, e.g.
    `path/to/file.pdf`
    """

    # Default to text/plain mimetype if not in dictionary
    content_type = "text/plain"

    # Dictionary of extensions and cooresponding mimetypes
    mimetypes = {
        ".jpeg": "image/jpeg",
        ".jpg": "image/jpeg",
        ".png": "image/png",
        ".svg": "image/svg+xml",
    }

    # Iterate over mimetypes dictionary
    for key in mimetypes:
        if key in file_name:
            content_type = mimetypes[key]

    # Scoped file result
    file_result = None

    # Get the request file or return false if an exception is raised
    try:
        s3 = resource('s3')
        file_result = s3.Object(BUCKET_NAME, file_name).get()
    except Exception as e:
        return False

    # If successful return the response
    return Response(file_result["Body"].read(), mimetype=content_type)
