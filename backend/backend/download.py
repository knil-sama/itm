import datetime as dt
import logging
import uuid

import pymongo
import requests

import backend
from models.event import Event, EventStatus
from models.image import PartialImage
from models.url import Url

logger = logging.getLogger(__name__)


def load_event(collection: pymongo.collection.Collection, event: Event) -> None:
    collection.update_one(
        {"id": event.id},
        {
            "$set": {
                "image": event.part,
                "url": event.url,
                "status": str(event.status),
                "insert_time": dt.datetime.now(dt.UTC),
            },
        },
        upsert=True,
    )


def download_url(url: Url) -> Event:
    url_uuid = uuid.uuid1()
    download_status: EventStatus = EventStatus.ERROR
    exception_log = None
    partial_image = None
    try:
        response = requests.get(str(url.url), timeout=10)
        response.raise_for_status()
        download_status = EventStatus.SUCCESS
        partial_image = PartialImage(content=response.content)
    except requests.HTTPError as e:
        msg = f"got {e} while downloading url"
        logger.exception(msg)
        exception_log = msg
    return Event(
        id=url_uuid,
        url=str(url.url),
        status=download_status,
        exception_log=exception_log,
        partial_image=partial_image,
    )


def download_urls(generated_urls: list[Url]) -> list[Event]:
    downloaded_images = []
    for url in generated_urls:
        event = download_url(url=url)
        downloaded_images.append(event)
        load_event(backend.EVENTS, event)
    return downloaded_images
