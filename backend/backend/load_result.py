from backend.database import (
    create_image,
    drop_event,
    drop_partial_image,
    get_partial_image,
)
from models.event import Event, EventStatus
from models.image import Image


def load_result(events: list[Event]) -> None:
    for event in events:
        if event.status == EventStatus.SUCCESS:
            partial_image = get_partial_image(event.id)
            partial_image_dict = partial_image.dict(exclude_none=True)
            del partial_image_dict["event_id"]
            image = Image.parse_obj(partial_image_dict)
            create_image(image)
            # drop event
            drop_event(event.id)
            drop_partial_image(event.id)
