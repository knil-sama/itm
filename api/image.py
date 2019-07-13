from flask import make_response, send_file
import flask_restful
import base64
import api


class Image(flask_restful.Resource):
    def get(self, md5: str):
        """
        Return existing image if found

        Args:
            md5(str): Id of the image
        Returns:
           Image returned if found else None
        """
        result = api.CLIENT["image_bank"].images.find_one(
            {"md5": md5}, {"grayscale": 1}
        )
        if result:
            response = make_response(base64.b64decode(result["grayscale"]))
            response.headers.set("Content-Type", "image/png")
            response.headers.set(
                "Content-Disposition", "attachment", filename="image.png"
            )
            return response
        else:
            return {"message": "Image not found"}, 404
