import base64
from typing import Any, Literal, Self

import flask_restful
from flask import make_response

import api


class Image(flask_restful.Resource):
    def get(
        self: Self,
        md5: str,
    ) -> tuple[dict[str, Any], Literal[200]] | tuple[dict[str, str], Literal[404]]:
        """
        Return existing image if found

        Args:
            md5(str): Id of the image
        Returns:
           Image returned if found else None
        """
        result = api.CLIENT["image_bank"].images.find_one(
            {"md5": md5},
            {"grayscale": 1},
        )
        response = {"message": "Image not found"}, 404
        if result:
            response = make_response(base64.b64decode(result["grayscale"]))
            response.headers.set("Content-Type", "image/png")
            response.headers.set(
                "Content-Disposition",
                "attachment",
                filename="image.png",
            )
        return response
