import datetime as dt
import logging
import pathlib
import uuid
from typing import Any

import pymongo
import requests

import backend

logger = logging.getLogger(__name__)


def load_event(
    collection: pymongo.Collection,
    event_id: str,
    url: str,
    image: str,
) -> None:
    collection.update(
        {"id": event_id},
        {
            "$set": {
                "image": image,
                "url": url,
                "insert_time": dt.datetime.now(dt.UTC),
            },
        },
        upsert=True,
    )


def download_url(
    url: str,
    save_directory: str,
    error_directory: str,
) -> tuple[str, bool, pathlib.Path]:
    url_uuid = uuid.uuid1()
    download_success = False
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        download_success = True
        filepath = pathlib.Path(f"{save_directory}/{url_uuid}")
        filepath.open("wb").write(response.content)
    except requests.HTTPError as e:
        filepath = pathlib.Path(f"{error_directory}/{url_uuid}")
        filepath.open("w").write("")
        msg = f"got {e} written file in {filepath.absolute()}"
        logger.exception(msg)
    return str(url_uuid), download_success, filepath


def download_urls(**context: dict[str, Any]) -> list[str]:
    generated_urls = context["task_instance"].xcom_pull(task_ids="generate_url")
    downloaded_images = []
    for url in generated_urls:
        url_uuid, success, result_filepath = download_url(
            url=url.strip(),
            save_directory=backend.BACKEND_DOWNLOAD_DIRECTORY,
            error_directory=backend.BACKEND_ERROR_DIRECTORY,
        )
        image_string = ""
        with result_filepath.open("rb") as image_file:
            image_string = image_file.read().decode()
        downloaded_images.append({"success": success, "url": url, "event_id": url_uuid})
        load_event(backend.EVENTS, url_uuid, url, image_string)
        # Removed downloaded file
        result_filepath.unlink()
    return downloaded_images
