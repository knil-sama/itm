import typing
import numpy as np
from PIL import Image
import backend
import os


def grayscale(**context):
    downloaded_images = context["task_instance"].xcom_pull(task_ids="download_image")
    dict_gray_metadata = dict()
    for downloaded_image in downloaded_images:
        if downloaded_image["success"]:
            gray_metadata = img_to_gray(downloaded_image["filepath"])
            dict_gray_metadata[downloaded_image["filepath"]] = gray_metadata
    return dict_gray_metadata


def img_to_gray(filepath: str):
    # https://stackoverflow.com/questions/12201577/how-can-i-convert-an-rgb-image-into-grayscale-in-python
    img = Image.open(filepath, "r")
    rgb = np.array(img)
    r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    gray = np.mean([r, g, b], axis=0)
    # fromarray(gray, "L") not working
    gray_img = Image.fromarray(gray)
    gray_img = gray_img.convert("L")
    gray_filepath = os.path.join(
        backend.BACKEND_GRAYSCALE_DIRECTORY, os.path.split(filepath)[-1]
    )
    gray_img.save(gray_filepath, format="png")
    width, height = img.size
    return {"filepath": gray_filepath, "width": width, "height": height}
