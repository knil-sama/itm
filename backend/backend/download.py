import logging
import uuid

import requests

from backend.database import create_event
from models.event import Event, EventStatus
from models.image import PartialImage
from models.url import Url

logger = logging.getLogger(__name__)


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
        create_event(event)
    return downloaded_images
