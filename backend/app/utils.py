import json
from bson.objectid import ObjectId


class JSONEncoder(json.JSONEncoder):
    """ Json encoder with ObjectId support"""
    def default(self, obj):
        if isinstance(obj, ObjectId):
            # encode ObjectID as string
            return str(obj)
        return json.JSONEncoder.default(self, obj)
