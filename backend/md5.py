import typing
import os
import hashlib
import backend


def load_event_md5(collection, event_id: str, md5: str):
    collection.update({"id": event_id}, {"$set": {"md5": md5}}, upsert=True)


def md5(**context):
    downloaded_images = context["task_instance"].xcom_pull(task_ids="download_image")
    for downloaded_image in downloaded_images:
        if downloaded_image["success"]:
            event = backend.EVENTS.find_one({"id": downloaded_image["event_id"]})
            image_md5 = hashlib.md5(event["image"]).hexdigest()
            load_event_md5(backend.EVENTS, downloaded_image["event_id"], image_md5)
