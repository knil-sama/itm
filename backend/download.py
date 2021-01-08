import os
import typing
import uuid
import base64
import datetime as dt
import requests
import backend


def load_event(collection, event_id: str, url: str, image: str):
    collection.update(
        {"id": event_id},
        {"$set": {"image": image, "url": url, "insert_time": dt.datetime.utcnow()}},
        upsert=True,
    )


def download_url(
    url: str, save_directory: str, error_directory: str
) -> typing.Tuple[str, bool, str]:
    url_uuid = uuid.uuid1()
    download_success = False
    try:
        r = requests.get(url)
        if r.status_code == 200:
            download_success = True
    except Exception as e:
        print(e)
    if download_success:
        filepath = f"{save_directory}/{url_uuid}"
        open(filepath, "wb").write(r.content)
    else:
        # write empty file to simplify branching logic
        filepath = f"{error_directory}/{url_uuid}"
        open(filepath, "w").write("")
    return str(url_uuid), download_success, filepath


def download_urls(**context):
    generated_urls = context["task_instance"].xcom_pull(task_ids="generate_url")
    downloaded_images = []
    for url in generated_urls:
        url_uuid, success, result_filepath = download_url(
            url=url.strip(),
            save_directory=backend.BACKEND_DOWNLOAD_DIRECTORY,
            error_directory=backend.BACKEND_ERROR_DIRECTORY,
        )
        image_string = ""
        with open(result_filepath, "rb") as image_file:
            image_string = image_file.read()
        downloaded_images.append({"success": success, "url": url, "event_id": url_uuid})
        load_event(backend.EVENTS, url_uuid, url, image_string)
        # Removed downloaded file
        os.remove(result_filepath)
    return downloaded_images
