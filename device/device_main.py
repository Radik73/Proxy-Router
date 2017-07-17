import json
import socket
import sys
import urllib.request
import urllib.error

from threading import Timer
from device.request_creater import Request


class Device():
    def __init__(self, id, ip, port, timeout, delay, log):
        self.__id = id
        self.__ip = ip
        self.__port = port
        self.__timeout = timeout
        self.__delay = delay
        self.__log = log
        self.__request_loop()

    def __request_loop(self):
        thread = Timer(self.__delay, self.__request_loop)
        thread.daemon = True
        thread.start()
        self.__request_handler()

    def __request_handler(self):
        try:
            data = Request(self.__id).get_data()
            response = self.__send_request(data)
            print(' ')
            self.__log.info('Response received: {text}'
                            .format(text=str(response.read())))
            self.__log.info('Headers of response: {headers}'
                            .format(headers=str(response.info())))
        except socket.timeout:
            timeout_message = 'Time of waiting for response by request {id} is out'\
                            .format(id=str(data['request_id']))
            self.__log.info(timeout_message)
        except urllib.error.HTTPError as err:
            warning_message = '{code} {reason}'.format(code=err.code, reason=err.reason)
            self.__log.info(warning_message)
            if err.code == 400:
                sys.exit(1)
        except (ConnectionResetError, ConnectionRefusedError, urllib.error.URLError):
            non_connecting_message = 'Server is not available'
            self.__log.info(non_connecting_message)

    def __send_request(self, data):
        self.__log.info('Sent the request: {data}'.format(data=str(data)))
        response = urllib.request.urlopen('http://{ip}:{port}'.format(ip=self.__ip, port=self.__port),
                                          bytes(json.dumps(data), "utf-8"), timeout=self.__timeout)
        print('')
        return response