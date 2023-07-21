import os
from typing import Literal, Self

import flask_restful
import pymongo

MONGO_INITDB_ROOT_USERNAME = os.environ["MONGO_INITDB_ROOT_USERNAME"]
MONGO_INITDB_ROOT_PASSWORD = os.environ["MONGO_INITDB_ROOT_PASSWORD"]

CLIENT = pymongo.MongoClient(
    "mongodb://mongo:27017",
    username=MONGO_INITDB_ROOT_USERNAME,
    password=MONGO_INITDB_ROOT_PASSWORD,
)


class Index(flask_restful.Resource):
    """
    itm api
    """

    def get(self: Self) -> tuple[dict[str, str], Literal[200]]:
        """
        Returns:
            str: Hello world for people calling the api
        """
        json = {"message": "Hello, this api exist to query data"}
        return json, 200
