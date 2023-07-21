"""
All code must follow json api spec
"""
from flask import Flask
from flask_cors import CORS
from flask_restful import Api

from api import Index
from api.image import Image
from api.images import Images
from api.monitoring import Monitoring


def create_app() -> Flask:
    """
    Create the app and setting all the road here
    Returns:
        Flask: Flask application for the api
    """

    application = Flask(__name__)
    # bugsnag integration
    CORS(application)

    application.config["JSON_AS_ASCII"] = False
    application.config["DEBUG"] = True
    api = Api(application)
    # default index
    api.add_resource(Index, "/")
    api.add_resource(Image, "/image/<string:md5>")
    api.add_resource(Images, "/images")
    api.add_resource(Monitoring, "/monitoring")
    return application


if __name__ == "__main__":  # pragma: no cover
    application = create_app()
    application.run(host="0.0.0.0", port=5000)
