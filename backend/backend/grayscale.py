import io
from io import BytesIO
from typing import Any

import numpy as np
import pymongo
from PIL import Image

import backend


def load_event_grayscale(
    collection: pymongo.collection.Collection,
    event_id: str,
    grayscale: dict,
) -> None:
    collection.update_one({"id": event_id}, {"$set": grayscale}, upsert=True)


def grayscale(downloaded_images: list[dict]) -> None:
    for downloaded_image in downloaded_images:
        if downloaded_image["success"] == backend.EventStatus.SUCCESS:
            event = backend.EVENTS.find_one({"id": downloaded_image["event_id"]})
            gray_metadata = img_to_gray(event["image"])
            load_event_grayscale(
                backend.EVENTS,
                downloaded_image["event_id"],
                gray_metadata,
            )


def img_to_gray(image: bytes) -> dict[str, Any]:
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
    return {
        "grayscale": buffered.getvalue(),
        "width": width,
        "height": height,
    }
