from boto3 import resource
from flask import Response


from config import Config


def upload_file(file_name, file_object):
    try:
        s3 = resource('s3')
        file_result = s3.Object(BUCKET_NAME, file_name).put(Body=file_object)
    except Exception as e:
        return False
    return True


def download_file(file_name):
    file_result = None
    content_type = "text/plain"
    mimetypes = {
        ".jpeg": "image/jpeg",
        ".jpg": "image/jpeg",
        ".png": "image/png",
        ".svg": "image/svg+xml",
    }
    for key in mimetypes:
        if key in file_name:
            content_type = mimetypes[key]
    try:
        s3 = resource('s3')
        file_result = s3.Object(Config.AWS_S3_BUCKET, file_name).get()
    except Exception as e:
        return False
    return Response(file_result["Body"].read(), mimetype=content_type)
