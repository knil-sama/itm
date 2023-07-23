import pydantic


class Image(pydantic.BaseModel):
    id: str  # noqa: A003
    content: str
    grayscale: str
    height: pydantic.types.PositiveInt
    width: pydantic.types.PositiveInt


# insert_time": dt.datetime.now(dt.UTC),
