import random
import requests
import time
import json
import device.connection_controller as ctcn
import device.delay_controller as dlcn
import sys
import logging

class Device():
    def __init__(self, ip, number_of_port, identifier_of_device):
        self.ip = ip
        self.port = number_of_port
        self.id_device = identifier_of_device
        self.__requester(ip, self.port)

    def __set_log(self, name):
        self.file_name = 'device/' + name + '_device.log'
        logging.basicConfig(filename=self.file_name, level=logging.INFO)
        self.logger = logging.getLogger("Device")
        self.fh = logging.FileHandler(self.file_name)
        self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.fh.setFormatter(self.formatter)
        self.logger.addHandler(self.fh)
        return self.logger

    def __request_shaper(self, identifier_of_device):
        identifier_of_request = random.randint(0, 1000000)
        payload = {'device_id': identifier_of_device, 'request_id': identifier_of_request, 'status': 'OK',
                   'data': '{something information}'}
        data = json.dumps(payload)
        return data

    def __requester(self, ip, number_of_port):
        log = self.__set_log(self.id_device)
        delay = dlcn.delay_config()
        try:
            while True:
                time.sleep(int(delay))
                data  = self.__request_shaper(self.id_device)
                print('Request: ' + str(data) + '\n')
                log.info('Request: ' + str(data) + ' to ' + ip + ':' + number_of_port)
                response = requests.post('http://' + ip + ':' + number_of_port, data=data)
                header = response.headers
                message = response.text
                log.info('Headers: ' + str(header) + ' Response: ' + message)
                print('Headers of response: ' + str(header) + '\n')
                print('Response: ' + message + '\n')
                print('\n')
                if not ctcn.controller(message):
                    sys.exit()
        except requests.exceptions.ConnectionError:
            notification = 'Proxy server is not available'
            log.info(notification)
            print(notification)
        except KeyboardInterrupt:
            notification = 'Device is finished'
            print(notification)
