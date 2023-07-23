# from pydantic import BaseModel
from typing import Any

from fastapi import FastAPI, HTTPException, Response

from api.database import get_image, get_images, get_monitoring

app = FastAPI()


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "Hello, this api exist to query data, see the docs/"}


@app.get("/image/{md5}", responses={200: {"content": {"image/png": {}}}})
def read_image(md5: str) -> dict:
    result = get_image(md5)
    if result is not None:
        # response = make_response(base64.b64decode(result["grayscale"]))
        response = Response(result.grayscale, media_type="image/png")
    else:
        msg = f"Image {md5} not found"
        raise HTTPException(status_code=404, detail=msg)
    return response


@app.get("/images/")
def read_images() -> list[str]:
    """
    Return list of all md5 in db
    """
    results = get_images()
    return [result.md5 for result in results]


@app.get("/monitoring/")
def read_monitoring() -> list[dict[str, Any]] | str:
    """
    Returns:
        Stats of succes and error
    """
    response: str | list[dict[str, Any]] = "Nothing to monitor yet"
    list_result = get_monitoring()
    if list_result:
        response = [
            {
                "execution_date": result["execution_date"].strftime(
                    "%m/%d/%Y, %H:%M:%S",
                ),
                "success": result["success"],
                "error": result["error"],
            }
            for result in list_result
        ]
    return response
