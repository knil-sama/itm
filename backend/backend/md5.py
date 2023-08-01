import hashlib

from backend.database import upsert_event
from models.event import Event, EventStatus
from models.image import PartialImage


def img_to_md5(image: bytes) -> PartialImage:
    # set usedforsecurity at False here to both improve performance
    # and avoid the need to mock value when testing because it keep it stable
    return PartialImage(id=hashlib.md5(image, usedforsecurity=False).hexdigest())


def md5(downloaded_images: list[Event]) -> None:
    for downloaded_image in downloaded_images:
        if downloaded_image.status == EventStatus.SUCCESS:
            image_md5 = img_to_md5(downloaded_image.partial_image.content)
            upsert_event(downloaded_image.id, image_md5)
