import cv2
import numpy as np

from backend.database import get_partial_image, upsert_partial_image
from models.event import Event, EventStatus
from models.image import PartialImage


def grayscale(events: list[Event]) -> None:
    for event in events:
        if event.status == EventStatus.SUCCESS:
            partial_image = get_partial_image(event.id)
            gray_image = img_to_gray(partial_image.content)
            upsert_partial_image(event.id, gray_image)


def img_to_gray(image: bytes) -> PartialImage:
    # https://stackoverflow.com/questions/12201577/how-can-i-convert-an-rgb-image-into-grayscale-in-python
    image_np = np.frombuffer(image, np.uint8)
    image_gray = cv2.imdecode(image_np, cv2.IMREAD_GRAYSCALE)
    _, buffer = cv2.imencode(".png", image_gray)
    data_encode = np.array(buffer)
    return PartialImage(grayscale=bytearray(data_encode.tobytes()))
