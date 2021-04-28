import os


class Config:
    AWS_S3_BUCKET = os.environ.get('AWS_S3_BUCKET')
    HOST_NAME = os.environ.get('PUBLIC_URL')
    IS_PRODUCTION_ENV = os.environ.get('ENVIRONMENT') == 'production'
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
