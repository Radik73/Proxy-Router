import json


class Body():
    def __init__(self, input, logger):
        self.__data = json.loads(input)
        self.__data_str = str(input)
        logger.info('The request received from client: {request_from_client}: '
                    .format(request_from_client=str(self.__data_str)))

    def get_id(self):
        key = 'device_id'
        device_id = self.__data[key]
        return device_id

    def get_string(self):
        return self.__data_str