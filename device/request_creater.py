import random


class Request():
    def __init__(self, id):
        self.__form_request(id)

    def get_data(self):
        return self.data

    def __form_request(self, id):
        self.data = {'device_id': id, 'request_id': self.__id_creater(),
                     'status': 'OK', 'data': '{something information}'}

    def __id_creater(self):
        id = random.randint(1, 10000000)
        return id