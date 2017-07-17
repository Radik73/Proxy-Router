import json

from jsonschema import validate
from jsonschema import exceptions


class Validator():
    def __init__(self, data):
        self.request = data

    def is_json(self):
        try:
            self.__request_data = json.loads(self.request)
            return True
        except json.decoder.JSONDecodeError:
            return False

    def is_structure(self):
        list_for_checked = ['device_id', 'request_id', 'status', 'data']
        for key in list_for_checked:
            key_exists = key in self.__request_data
            if not key_exists:
                return False
        return True

    def is_valid(self):
        schema = {"type": "object",
                  "properties": {
                  "device_id": {"type": "string",
                                "pattern": "^[0-9]{1,}$"},
                  "request_id": {"type": "number"},
                  "status": {"type": "string",
                             "pattern": "^[OK]{2}$"},
                  "data": {"type": "string"}},}
        try:
            validate(self.__request_data, schema)
        except exceptions.ValidationError:
            return False
        else:
            return True