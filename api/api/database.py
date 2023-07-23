import os

import pymongo

from models.image import Image
from models.monitoring import Monitoring

MONGO_INITDB_ROOT_USERNAME = os.environ["MONGO_INITDB_ROOT_USERNAME"]
MONGO_INITDB_ROOT_PASSWORD = os.environ["MONGO_INITDB_ROOT_PASSWORD"]

CLIENT = pymongo.MongoClient(
    "mongodb://mongo:27017",
    username=MONGO_INITDB_ROOT_USERNAME,
    password=MONGO_INITDB_ROOT_PASSWORD,
)


def get_image(md5: str) -> Image | None:
    mongo_object = CLIENT["image_bank"].images.find_one({"md5": md5})
    return Image.parse_object(mongo_object)


def get_images() -> list[Image]:
    return [
        Image.parse_object(mongo_object)
        for mongo_object in CLIENT["image_bank"].images.find({}, {"md5": 1})
    ]


def get_monitoring() -> list[Monitoring]:
    return [
        Monitoring.parse_object(mongo_object)
        for mongo_object in CLIENT["image_bank"].monitoring.find({})
    ]
