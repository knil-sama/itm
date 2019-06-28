import os

MONGO_INITDB_ROOT_USERNAME = os.environ["MONGO_INITDB_ROOT_USERNAME"]
MONGO_INITDB_ROOT_PASSWORD = os.environ["MONGO_INITDB_ROOT_PASSWORD"]

CLIENT = pymongo.MongoClient("mongodb://mongo:27017",username=backend.MONGO_INITDB_ROOT_USERNAME,password=backend.MONGO_INITDB_ROOT_PASSWORD)
DB = CLIENT["image_bank"]
COLLECTION = DB.images


class Index(Resource):
    """
    itm api
    """

    def get(self):
        """
        Returns:
            str: Hello world for people calling the api
        """
        json = {
            "message": "Hello, this api exist to query data"
        }
        return json, 200
