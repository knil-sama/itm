from pydantic import AnyHttpUrl, BaseModel


class Url(BaseModel):
    url: AnyHttpUrl
