from backend.database import create_image, drop_event, get_event
from models.event import Event, EventStatus
from models.image import Image


def load_result(downloaded_images: list[Event]) -> None:
    for downloaded_image in downloaded_images:
        if downloaded_image.status == EventStatus.SUCCESS:
            event = get_event(downloaded_image.id)
            image = Image.parse_obj(event.partial_image.dict(exclude_none=True))
            create_image(image)
            # drop event
            drop_event(downloaded_image.id)
