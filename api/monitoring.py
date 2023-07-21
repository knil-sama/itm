from typing import Any, Literal, Self

import flask_restful

import api


class Monitoring(flask_restful.Resource):
    def get(
        self: Self,
    ) -> (
        tuple[dict[str, list[dict[str, Any]]], Literal[200]]
        | tuple[dict[str, str], Literal[200]]
    ):
        """
        Returns:
           Stats of succes and error
        """
        response = {"message": "Nothing to monitor yet"}, 200
        result_cursor = api.CLIENT["image_bank"].monitoring.find({})
        list_result = list(result_cursor)
        monitoring: list[dict[str, Any]] = [
            {
                "execution_date": result["execution_date"].strftime(
                    "%m/%d/%Y, %H:%M:%S",
                ),
                "success": result["success"],
                "error": result["error"],
            }
            for result in list_result
        ]
        if monitoring:
            response = {"message": monitoring}, 200
        return response
