import flask_restful
import api


class Monitoring(flask_restful.Resource):
    def get(self):
        """
        Returns:
           Stats of succes and error
        """
        result_cursor = api.CLIENT["image_bank"].monitoring.find({})
        list_result = list(result_cursor)
        monitoring = [
            {
                "execution_date": result["execution_date"].strftime(
                    "%m/%d/%Y, %H:%M:%S"
                ),
                "success": result["success"],
                "error": result["error"],
            }
            for result in list_result
        ]
        if monitoring:
            return {"message": monitoring}, 200
        else:
            return {"message": "Nothing to monitor yet"}, 200
