from datetime import UTC, datetime
from enum import StrEnum, auto
from uuid import UUID

from pydantic import (
    AnyHttpUrl,
    BaseModel,
    root_validator,
)

# root_validator is changed to model_validator in v2
from models.image import PartialImage


class EventStatus(StrEnum):
    SUCCESS = auto()
    ERROR = auto()


class Event(BaseModel):
    id: UUID  # noqa: A003
    url: AnyHttpUrl
    status: EventStatus
    exception_log: str | None
    partial_image: PartialImage | None
    created_at: datetime = datetime.now(UTC)

    @root_validator()
    def check_we_either_get_log_or_image(
        cls,  # noqa: ANN101, N805
        values: dict,
    ) -> dict:
        if values["exception_log"] is None and values["status"] == EventStatus.ERROR:
            msg = "When status is error we need to log the exception"
            raise ValueError(msg)
        if (
            values["exception_log"] is not None
            and values["status"] == EventStatus.SUCCESS
        ):
            msg = "When status is success we can`t log exception"
            raise ValueError(msg)
        if values["partial_image"] is None and values["status"] == EventStatus.SUCCESS:
            msg = "When status is success we should have a partial image"
            raise ValueError(msg)
        return values
