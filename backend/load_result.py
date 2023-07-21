import backend
import datetime as dt


def load_image(collection, event: dict):
    collection.update(
        {"md5": event["md5"]},
        {
            "$set": {
                "image": event["image"],
                "grayscale": event["grayscale"],
                "height": event["height"],
                "width": event["width"],
                "insert_time": dt.datetime.utcnow(),
            }
        },
        upsert=True,
    )


def load_result(**context):
    downloaded_images = context["task_instance"].xcom_pull(task_ids="download_image")
    for downloaded_image in downloaded_images:
        if downloaded_image["success"]:
            event = backend.EVENTS.find_one({"id": downloaded_image["event_id"]})
            load_image(backend.IMAGES, event)
            # drop event
            backend.EVENTS.delete_one({"id": downloaded_image["event_id"]})
