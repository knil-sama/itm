import typing
import os
import hashlib
import backend


def md5(**context):
    downloaded_images = context["task_instance"].xcom_pull(task_ids="download_image")
    dict_md5 = dict()
    for downloaded_image in downloaded_images:
        if downloaded_image["success"]:
            with open(downloaded_image["filepath"], "rb") as image_file:
                image_md5 = hashlib.md5(image_file.read()).hexdigest()
                dict_md5[downloaded_image["filepath"]] = image_md5
    return dict_md5
