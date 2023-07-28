import pydantic


class Image(pydantic.BaseModel):
    id: str  # noqa: A003
    content: bytes
    grayscale: bytes
    height: pydantic.types.PositiveInt
    width: pydantic.types.PositiveInt


# insert_time": dt.datetime.now(dt.UTC),


class PartialImage(pydantic.BaseModel):
    id: str | None  # noqa: A003
    content: bytes | None
    grayscale: bytes | None
    height: pydantic.types.PositiveInt | None
    width: pydantic.types.PositiveInt | None
