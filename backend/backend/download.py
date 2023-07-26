import datetime as dt
import logging
import pathlib
import uuid

import pymongo
import requests

import backend
from backend.backend import EventStatus

logger = logging.getLogger(__name__)


def load_event(
    collection: pymongo.collection.Collection,
    event_id: str,
    url: str,
    status: EventStatus,
    image: bytes,
) -> None:
    collection.update_one(
        {"id": event_id},
        {
            "$set": {
                "image": image,
                "url": url,
                "status": str(status),
                "insert_time": dt.datetime.now(dt.UTC),
            },
        },
        upsert=True,
    )


def download_url(
    url: str,
    save_directory: pathlib.Path,
    error_directory: pathlib.Path,
) -> tuple[str, EventStatus, pathlib.Path]:
    url_uuid = uuid.uuid1()
    download_status: EventStatus = EventStatus.ERROR
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        download_status = EventStatus.SUCCESS
        filepath = save_directory / pathlib.Path(str(url_uuid))
        filepath.open("wb").write(response.content)
    except requests.HTTPError as e:
        filepath = error_directory / pathlib.Path(str(url_uuid))
        filepath.open("w").write("")
        msg = f"got {e} written file in {filepath.absolute()}"
        logger.exception(msg)
    return str(url_uuid), download_status, filepath


def download_urls(generated_urls: list[str]) -> list[dict]:
    downloaded_images = []
    for url in generated_urls:
        url_uuid, status, result_filepath = download_url(
            url=url.strip(),
            save_directory=backend.BACKEND_DOWNLOAD_DIRECTORY,
            error_directory=backend.BACKEND_ERROR_DIRECTORY,
        )
        image: bytes = None
        with result_filepath.open("rb") as image_file:
            image = image_file.read()
        downloaded_images.append({"status": status, "url": url, "event_id": url_uuid})
        load_event(backend.EVENTS, url_uuid, url, status, image)
        # Removed downloaded file
        result_filepath.unlink()
    return downloaded_images
