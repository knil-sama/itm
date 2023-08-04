from datetime import UTC, datetime
from uuid import UUID

import pydantic


class Image(pydantic.BaseModel):
    id: str  # noqa: A003
    content: bytes
    grayscale: bytes
    height: pydantic.types.PositiveInt
    width: pydantic.types.PositiveInt
    created_at: datetime = datetime.now(UTC)

    class Config:
        allow_mutation = False


class PartialImage(pydantic.BaseModel):
    id: str | None  # noqa: A003
    content: bytes | None
    grayscale: bytes | None
    height: pydantic.types.PositiveInt | None
    width: pydantic.types.PositiveInt | None
    event_id: UUID | None

    class Config:
        allow_mutation = False
