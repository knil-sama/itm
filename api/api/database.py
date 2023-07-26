import os

import pymongo

from models.image import Image
from models.monitoring import Monitoring

MONGO_INITDB_ROOT_USERNAME = os.environ["MONGO_INITDB_ROOT_USERNAME"]
MONGO_INITDB_ROOT_PASSWORD = os.environ["MONGO_INITDB_ROOT_PASSWORD"]

MONGO_CLIENT = pymongo.MongoClient(
    "mongodb://mongo:27017",
    username=MONGO_INITDB_ROOT_USERNAME,
    password=MONGO_INITDB_ROOT_PASSWORD,
)


def get_image(
    image_id: str,
    client: pymongo.MongoClient = MONGO_CLIENT,
) -> Image | None:
    mongo_object = client["image_bank"].images.find_one({"id": image_id})
    return Image.parse_raw(mongo_object)


def get_images(client: pymongo.MongoClient = MONGO_CLIENT) -> list[Image]:
    return [
        Image.parse_raw(mongo_object)
        for mongo_object in client["image_bank"].images.find({}, {"id": 1})
    ]


def get_monitoring(client: pymongo.MongoClient = MONGO_CLIENT) -> list[Monitoring]:
    return [
        Monitoring.parse_raw(mongo_object)
        for mongo_object in client["image_bank"].monitoring.find({})
    ]
