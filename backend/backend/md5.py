import hashlib

from backend.database import get_partial_image, upsert_partial_image
from models.event import Event, EventStatus
from models.image import PartialImage


def img_to_md5(image: bytes) -> PartialImage:
    # set usedforsecurity at False here to both improve performance
    # and avoid the need to mock value when testing because it keep it stable
    return PartialImage(id=hashlib.md5(image, usedforsecurity=False).hexdigest())


def md5(events: list[Event]) -> None:
    for event in events:
        if event.status == EventStatus.SUCCESS:
            partial_image = get_partial_image(event.id)
            image_md5 = img_to_md5(partial_image.content)
            upsert_partial_image(event.id, image_md5)
