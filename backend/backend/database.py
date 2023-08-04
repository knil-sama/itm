# TODO(clement): refactor into a "storage" layer
# https://github.com/knil-sama/itm/issues/14

import os
from datetime import UTC, datetime
from typing import Any
from uuid import UUID

import pymongo

from models.event import Event, EventStatus
from models.image import Image, PartialImage

MONGO_INITDB_ROOT_USERNAME = os.environ["MONGO_INITDB_ROOT_USERNAME"]
MONGO_INITDB_ROOT_PASSWORD = os.environ["MONGO_INITDB_ROOT_PASSWORD"]


def get_collection(
    database_name: str,
    collection_name: str,
) -> pymongo.collection.Collection:
    client: pymongo.MongoClient[dict[str, Any]] = pymongo.MongoClient(
        "mongodb://mongo:27017",
        username=MONGO_INITDB_ROOT_USERNAME,
        password=MONGO_INITDB_ROOT_PASSWORD,
        uuidRepresentation="standard",
    )
    db = client[database_name]
    return db[collection_name]


IMAGES = get_collection("image_bank", "images")
IMAGES_MONITORING = get_collection("image_bank", "monitoring")
EVENTS = get_collection("event", "events")
PARTIAL_IMAGE = get_collection("event", "partial_images")


def create_image(
    image: Image,
    collection: pymongo.collection.Collection = IMAGES,
) -> None:
    collection.insert_one(
        {
            "id": image.id,
            "content": image.content,
            "grayscale": image.grayscale,
            "height": image.height,
            "width": image.width,
            "created_at": image.created_at,
        },
    )


def get_event(
    event_id: UUID,
    event_collection: pymongo.collection.Collection = EVENTS,
) -> Event:
    return Event.parse_obj(event_collection.find_one({"id": event_id}))


def create_event(
    event: Event,
    collection: pymongo.collection.Collection = EVENTS,
) -> None:
    collection.insert_one(
        {
            "id": event.id,
            "url": event.url,
            "status": str(event.status),
            "created_at": event.created_at,
            "updated_at": datetime.now(UTC),
        },
    )


def upsert_partial_image(
    event_id: UUID,
    current_partial_image: PartialImage,
    collection: pymongo.collection.Collection = PARTIAL_IMAGE,
) -> None:
    collection.update_one(
        {"event_id": event_id},
        {
            "$set": {
                "updated_at": datetime.now(UTC),
                **current_partial_image.dict(exclude_none=True),
            },
        },
        upsert=True,
    )


def get_partial_image(
    event_id: UUID,
    event_collection: pymongo.collection.Collection = PARTIAL_IMAGE,
) -> PartialImage:
    return PartialImage.parse_obj(event_collection.find_one({"event_id": event_id}))


def drop_event(
    event_id: str,
    event_collection: pymongo.collection.Collection = EVENTS,
) -> None:
    event_collection.delete_one({"id": event_id})


def drop_partial_image(
    event_id: str,
    event_collection: pymongo.collection.Collection = PARTIAL_IMAGE,
) -> None:
    event_collection.delete_one({"event_id": event_id})


def upsert_monitoring(
    event_status: EventStatus,
    execution_date: str,
    collection: pymongo.collection.Collection = IMAGES_MONITORING,
) -> None:
    collection.find_one_and_update(
        {"execution_date": execution_date},
        {"$inc": {event_status: 1}},
        upsert=True,
    )
