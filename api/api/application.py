# from pydantic import BaseModel
from typing import Any

import pydantic
from fastapi import FastAPI, HTTPException, Response

from api.database import get_image, get_images, get_monitoring

app = FastAPI()


class MonitoringReponse(pydantic.BaseModel):
    execution_date: str
    success: pydantic.types.NonNegativeInt
    error: pydantic.types.NonNegativeInt


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "Hello, this api exist to query data, see the docs/"}


@app.get("/image/{image_id}", responses={200: {"content": {"image/png": {}}}})
def read_image(image_id: str) -> dict:
    result = get_image(image_id)
    if result is not None:
        # response = make_response(base64.b64decode(result["grayscale"]))
        response = Response(result.grayscale, media_type="image/png")
    else:
        msg = f"Image {image_id} not found"
        raise HTTPException(status_code=404, detail=msg)
    return response


@app.get("/images/")
def read_images() -> list[str]:
    """
    Return list of all id in db
    """
    results = get_images()
    return [result.id for result in results]


@app.get("/monitoring/")
def read_monitoring() -> list[MonitoringReponse] | str:
    """
    Returns:
        Stats of succes and error
    """
    response: str | list[dict[str, Any]] = "Nothing to monitor yet"
    list_result = get_monitoring()
    if list_result:
        response = [
            MonitoringReponse(
                execution_date=result.execution_date.strftime(
                    "%m/%d/%Y, %H:%M:%S",
                ),
                success=result.success,
                error=result.error,
            )
            for result in list_result
        ]
    return response
