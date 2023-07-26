import datetime as dt

import pymongo

import backend


def load_image(collection: pymongo.collection.Collection, event: dict) -> None:
    collection.update_one(
        {"id": event["id"]},
        {
            "$set": {
                "image": event["image"],
                "grayscale": event["grayscale"],
                "height": event["height"],
                "width": event["width"],
                "insert_time": dt.datetime.now(dt.UTC),
            },
        },
        upsert=True,
    )


def drop_event(
    event_id: str,
    event_collection: pymongo.collection.Collection = backend.EVENTS,
) -> None:
    event_collection.delete_one({"id": event_id})


def get_event(
    event_id: str,
    event_collection: pymongo.collection.Collection = backend.EVENTS,
) -> dict:
    return event_collection.find_one({"id": event_id})


def load_result(downloaded_images: list[dict]) -> None:
    for downloaded_image in downloaded_images:
        if downloaded_image["success"] == backend.EventStatus.SUCCESS:
            event = get_event(downloaded_image["event_id"])
            load_image(backend.IMAGES, event)
            # drop event
            drop_event(downloaded_image["event_id"])
