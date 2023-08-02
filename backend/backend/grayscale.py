import io
from io import BytesIO

import numpy as np
from PIL import Image

from backend.database import upsert_event
from models.event import Event, EventStatus
from models.image import PartialImage


def grayscale(downloaded_images: list[Event]) -> None:
    for downloaded_image in downloaded_images:
        if downloaded_image.status == EventStatus.SUCCESS:
            gray_image = img_to_gray(downloaded_image.partial_image.content)
            upsert_event(downloaded_image.id, gray_image)


def img_to_gray(image: bytes) -> PartialImage:
    # https://stackoverflow.com/questions/12201577/how-can-i-convert-an-rgb-image-into-grayscale-in-python

    rgb = np.array(Image.open(io.BytesIO(image)))
    r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    gray = np.mean([r, g, b], axis=0)
    # fromarray(gray, "L") not working
    gray_img = Image.fromarray(gray)
    gray_img = gray_img.convert("L")
    buffered = BytesIO()
    gray_img.save(buffered, format="png")
    width, height = gray_img.size
    return PartialImage(grayscale=buffered.getvalue(), width=width, height=height)
