from pydantic import AnyHttpUrl, BaseModel
from pydantic.types import PositiveInt


class UrlPicsum(BaseModel):
    url: AnyHttpUrl
    height: PositiveInt
    width: PositiveInt

    class Config:
        allow_mutation = False
