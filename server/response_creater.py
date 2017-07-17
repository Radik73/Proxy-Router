class ResponseCreater():
    def __init__(self, dict_of_data):
        self.__set_response(dict_of_data)

    def __set_response(self, dict_of_data):
        self.response = {'device_id': dict_of_data['device_id'],
                         'request_id': dict_of_data['request_id'], 'status': 'OK'}

    def get_response(self):
        return self.response