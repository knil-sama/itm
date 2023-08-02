# TODO(clement): refactor into a "storage" layer
# https://github.com/knil-sama/itm/issues/14

import datetime as dt
from uuid import UUID

import pymongo

import backend
from models.event import Event
from models.image import Image, PartialImage


def create_image(
    image: Image,
    collection: pymongo.collection.Collection = backend.IMAGES,
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
    event_collection: pymongo.collection.Collection = backend.EVENTS,
) -> Event:
    return Event.parse_obj(event_collection.find_one({"id": event_id}))


def create_event(
    event: Event,
    collection: pymongo.collection.Collection = backend.EVENTS,
) -> None:
    collection.insert_one(
        {
            "id": event.id,
            "url": event.url,
            "status": str(event.status),
            "created_at": event.created_at,
            "updated_at": dt.datetime.now(dt.UTC),
            "partial_image": event.partial_image.dict(exclude_none=True),
        },
    )


def upsert_event(
    event_id: UUID,
    current_partial_image: PartialImage,
    collection: pymongo.collection.Collection = backend.EVENTS,
) -> None:
    collection.update_one(
        {"id": event_id},
        {
            "$set": {
                "updated_at": dt.datetime.now(dt.UTC),
                "partial_image": current_partial_image.dict(exclude_none=True),
            },
        },
        upsert=True,
    )


def drop_event(
    event_id: str,
    event_collection: pymongo.collection.Collection = backend.EVENTS,
) -> None:
    event_collection.delete_one({"id": event_id})
