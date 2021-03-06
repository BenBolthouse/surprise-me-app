import os


class Config:
    HOST_NAME = os.environ.get('HOST_NAME')
    S3_BUCKET = os.environ.get('S3_BUCKET')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
