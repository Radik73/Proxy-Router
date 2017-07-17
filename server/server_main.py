import json
import time
import tornado.web
from tornado import gen
from tornado.ioloop import IOLoop

from server.response_creater import ResponseCreater
from utilities.validator import Validator


class MainHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        self.log = self.application.logger
        self.log.info('The request received: {request_data}'
                    .format(request_data=self.request.body.decode('utf-8')))
        valid = self.__request_handler(self.request.body.decode('utf-8'))
        yield self.__async_sleep(self.application.delay)
        if valid:
            response_body = ResponseCreater(
                            json.loads(self.request.body.decode('utf-8'))).get_response()
            self.__positive_response(response_body)
        if not valid:
            self.__negative_response()
        self.set_header("Version", self.application.version)
        self.finish()

    @gen.coroutine
    def __async_sleep(self, seconds):
        yield gen.Task(IOLoop.instance().add_timeout, time.time() + seconds)

    def __request_handler(self, request_data):
        val = Validator(request_data)
        if val.is_json() and val.is_structure() and val.is_valid():
            return True
        else:
            return False

    def __positive_response(self, response_body):
        response_data = json.dumps(response_body)
        self.response = bytes(response_data, "utf-8")
        self.set_header("Content-Type", 'application/json')
        self.set_status(200)
        self.log.info('Sent a response: {response}'
                      .format(response=str(self.response)))
        self.write(self.response)

    def __negative_response(self):
        notification = ' Bad Request'
        self.set_header("Content-Type", 'application/json')
        self.set_status(400, reason=notification)
        self.log.info('Sent a response: {response}'
                      .format(response=notification))