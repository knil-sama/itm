import datetime as dt
from typing import Any

import pymongo

import backend


def load_image(collection: pymongo.Collection, event: dict) -> None:
    collection.update(
        {"md5": event["md5"]},
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


def load_result(**context: dict[str, Any]) -> None:
    downloaded_images = context["task_instance"].xcom_pull(task_ids="download_image")
    for downloaded_image in downloaded_images:
        if downloaded_image["success"]:
            event = backend.EVENTS.find_one({"id": downloaded_image["event_id"]})
            load_image(backend.IMAGES, event)
            # drop event
            backend.EVENTS.delete_one({"id": downloaded_image["event_id"]})
