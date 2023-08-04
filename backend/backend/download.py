import logging
import uuid

import requests

from backend.database import create_event, upsert_partial_image
from models.event import Event, EventStatus
from models.image import PartialImage
from models.url import UrlPicsum

logger = logging.getLogger(__name__)


def download_url(url: UrlPicsum) -> tuple[Event, PartialImage | None]:
    event_uuid = uuid.uuid1()
    download_status: EventStatus = EventStatus.ERROR
    exception_log = None
    partial_image = None
    try:
        response = requests.get(str(url.url), timeout=10)
        response.raise_for_status()
        download_status = EventStatus.SUCCESS
        partial_image = PartialImage(
            event_id=event_uuid,
            content=response.content,
            width=url.width,
            height=url.height,
        )
    except requests.HTTPError as e:
        msg = f"got {e} while downloading url"
        logger.exception(msg)
        exception_log = msg
    event = Event(
        id=event_uuid,
        url=str(url.url),
        status=download_status,
        exception_log=exception_log,
    )
    return event, partial_image


def download_urls(generated_urls: list[UrlPicsum]) -> list[Event]:
    events = []
    for url in generated_urls:
        event, partial_image = download_url(url=url)
        events.append(event)
        create_event(event)
        if partial_image is not None:
            upsert_partial_image(event.id, partial_image)
    return events
