from flask import send_file
import flask_restful
import api


class Images(flask_restful.Resource):
    def get(self):
        """
        Return list of all md5 in db
        """
        result_cursor = api.CLIENT["image_bank"].images.find({}, {"md5": 1})
        list_result = [result["md5"] for result in result_cursor]
        return {"md5 list": list_result}, 200
