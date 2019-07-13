import pymongo
import base64
import backend
import datetime as dt


def update_monitoring(url_filepath: str, **context):
    client = pymongo.MongoClient(
        "mongodb://mongo:27017",
        username=backend.MONGO_INITDB_ROOT_USERNAME,
        password=backend.MONGO_INITDB_ROOT_PASSWORD,
    )
    db = client["image_bank"]
    collection = db.monitoring
    downloaded_images = context["task_instance"].xcom_pull(task_ids="download_image")
    execution_date = context["execution_date"]
    for downloaded_image in downloaded_images:
        if downloaded_image["success"]:
            collection.update(
                {"execution_date": execution_date},
                {"$inc": {"success": 1, "error": 0}},
                True,
            )
        else:
            collection.update(
                {"execution_date": execution_date},
                {"$inc": {"success": 0, "error": 1}},
                True,
            )
