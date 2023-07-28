import hashlib

import pymongo

import backend
from models.event import EventStatus


def load_event_md5(
    collection: pymongo.collection.Collection,
    event_id: str,
    md5: str,
) -> None:
    collection.update_one({"id": event_id}, {"$set": {"md5": md5}}, upsert=True)


def md5(downloaded_images: list[dict]) -> None:
    for downloaded_image in downloaded_images:
        if downloaded_image["success"] == EventStatus.SUCCESS:
            event = backend.EVENTS.find_one({"id": downloaded_image["event_id"]})
            image_md5 = hashlib.md5(event["image"]).hexdigest()
            load_event_md5(backend.EVENTS, downloaded_image["event_id"], image_md5)
