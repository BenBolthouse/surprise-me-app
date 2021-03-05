from boto3 import client, resource


def upload(file_name, bucket, object_name):
    # TODO finish docstring
    """
    Upload a file to the s3 file store.

    String `file_name`...

    String `bucket`...
    """
    s3_client = client('s3')
    response = s3_client.upload_file(file_name, bucket, object_name)

    return response


def download(file_name, bucket, download_dir):
    # TODO finish docstring
    """
    Download a file from the 23 file store.

    String `file_name`...

    String `bucket`...
    """
    s3 = resource('s3')
    output = s3.Bucket(bucket).download_file(file_name, download_dir)
