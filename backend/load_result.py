import pymongo
import base64
import backend
import datetime as dt


def load_image(
    collection, filepath: str, grayscale: bytes, md5: str, height: int, width: int
):
    with open(grayscale, "rb") as image_file:
        base64_img = base64.b64encode(image_file.read())
    collection.update(
        {"md5": md5},
        {
            "$set": {
                "grayscale": base64_img,
                "height": height,
                "width": width,
                "insert_time": dt.datetime.utcnow(),
            }
        },
        upsert=True,
    )


def load_result(**context):
    client = pymongo.MongoClient(
        "mongodb://mongo:27017",
        username=backend.MONGO_INITDB_ROOT_USERNAME,
        password=backend.MONGO_INITDB_ROOT_PASSWORD,
    )
    db = client["image_bank"]
    collection = db.images
    downloaded_images = context["task_instance"].xcom_pull(task_ids="download_image")
    grayscale_images = context["task_instance"].xcom_pull(task_ids="grayscale_image")
    md5_images = context["task_instance"].xcom_pull(task_ids="md5_image")
    for downloaded_image in downloaded_images:
        if downloaded_image["success"]:
            image_filepath = downloaded_image["filepath"]
            image_grayscale = grayscale_images[image_filepath]["filepath"]
            image_width = grayscale_images[image_filepath]["width"]
            image_height = grayscale_images[image_filepath]["height"]
            image_md5 = md5_images[image_filepath]
            load_image(
                collection,
                image_filepath,
                image_grayscale,
                image_md5,
                image_height,
                image_width,
            )
