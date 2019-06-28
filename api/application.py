"""
All code must follow json api spec
"""
from flask import Flask
from flask_restful import Api
from flask_cors import CORS
import json
import os
import logging

from api.image import Image
from api import Index

def create_app():
    """
    Create the app and setting all the road here
    Returns:
        Flask: Flask application for the api
    """

    application = Flask(__name__)
    # bugsnag integration
    handle_exceptions(application)
    CORS(application)

    application.config["JSON_AS_ASCII"] = False
    if RELEASE_STAGE == "production":
        application.config["DEBUG"] = False
    else:
        application.config["DEBUG"] = True
    api = Api(application)
    # default index
    api.add_resource(Index, "/")
    api.add_resource(Image, "/".join(["/image", "<string:md5>"]))
    return application


def main():
    application = create_app()
    return application
