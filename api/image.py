from flask import send_file
import flask_restful
import webargs.flaskparser as fparser
import api 

class Image(flask_restful.Resource):
    def get(self, md5: str):
        """
        Return most probable locale for job offer
        Args:
            md5(str): Id of the image
        Returns:
           Image returned if found else None
        """
        result = api.COLLECTION.find_one({"md5": md5}, {"filepath":"true"})             if result:
            result = result["filepath"]
        return send_file(result, mimetype='image/png')
