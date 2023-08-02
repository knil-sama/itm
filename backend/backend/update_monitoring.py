from backend.database import upsert_monitoring
from models.event import Event


def update_monitoring(downloaded_images: list[Event], execution_date: str) -> None:
    for downloaded_image in downloaded_images:
        upsert_monitoring(downloaded_image.status, execution_date)
