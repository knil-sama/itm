import backend


def update_monitoring(downloaded_images: list[dict], execution_date: str) -> None:
    for downloaded_image in downloaded_images:
        if downloaded_image["success"]:
            backend.IMAGES_MONITORING.find_one_and_update(
                {"execution_date": execution_date},
                {"$inc": {"success": 1, "error": 0}},
                upsert=True,
            )
        else:
            backend.IMAGES_MONITORING.find_one_and_update(
                {"execution_date": execution_date},
                {"$inc": {"success": 0, "error": 1}},
                upsert=True,
            )
