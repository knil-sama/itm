import datetime as dt
import logging
import pathlib
import uuid

import pymongo
import requests

import backend

logger = logging.getLogger(__name__)


def load_event(
    collection: pymongo.collection.Collection,
    event_id: str,
    url: str,
    image: str,
) -> None:
    collection.update_one(
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
    save_directory: pathlib.Path,
    error_directory: pathlib.Path,
) -> tuple[str, bool, pathlib.Path]:
    url_uuid = uuid.uuid1()
    download_success = False
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        download_success = True
        filepath = save_directory / pathlib.Path(str(url_uuid))
        filepath.open("wb").write(response.content)
    except requests.HTTPError as e:
        filepath = error_directory / pathlib.Path(str(url_uuid))
        filepath.open("w").write("")
        msg = f"got {e} written file in {filepath.absolute()}"
        logger.exception(msg)
    return str(url_uuid), download_success, filepath


def download_urls(generated_urls: list[str]) -> list[dict]:
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
