import backend


def update_monitoring(**context):
    downloaded_images = context["task_instance"].xcom_pull(task_ids="download_image")
    execution_date = context["execution_date"]
    for downloaded_image in downloaded_images:
        if downloaded_image["success"]:
            backend.IMAGES_MONITORING.update(
                {"execution_date": execution_date},
                {"$inc": {"success": 1, "error": 0}},
                True,
            )
        else:
            backend.IMAGES_MONITORING.update(
                {"execution_date": execution_date},
                {"$inc": {"success": 0, "error": 1}},
                True,
            )
