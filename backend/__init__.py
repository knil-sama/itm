import os
import pymongo

BACKEND_DOWNLOAD_DIRECTORY = os.environ["BACKEND_DOWNLOAD_DIRECTORY"]
BACKEND_ERROR_DIRECTORY = os.environ["BACKEND_ERROR_DIRECTORY"]
BACKEND_GRAYSCALE_DIRECTORY = os.environ["BACKEND_GRAYSCALE_DIRECTORY"]
MONGO_INITDB_ROOT_USERNAME = os.environ["MONGO_INITDB_ROOT_USERNAME"]
MONGO_INITDB_ROOT_PASSWORD = os.environ["MONGO_INITDB_ROOT_PASSWORD"]


def get_collection(database_name: str, collection_name: str):
    client = pymongo.MongoClient(
        "mongodb://mongo:27017",
        username=MONGO_INITDB_ROOT_USERNAME,
        password=MONGO_INITDB_ROOT_PASSWORD,
    )
    db = client[database_name]
    return db[collection_name]


IMAGES = get_collection("image_bank", "images")
IMAGES_MONITORING = get_collection("image_bank", "monitoring")
EVENTS = get_collection("event", "images")
