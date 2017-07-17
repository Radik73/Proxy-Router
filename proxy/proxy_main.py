import tornado.web
import tornado.ioloop
import tornado.websocket
import tornado.gen
import tornado.escape
import tornado.httpclient

from proxy.Body import Body
from utilities.validator import Validator


class MainHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        self.log = self.application.logger
        valid = self.__check_request(self.request.body.decode('utf-8'))
        if valid:
            '''
            Handling the request by client
            '''
            body = Body(self.request.body.decode('utf-8'), self.log)
            address = self.application.table.get_address(body.get_id())
            try:
                '''
                Sending the request to ip
                '''
                request = self.__create_request_to_server(address, self.request.body.decode('utf-8'))
                http = tornado.httpclient.AsyncHTTPClient()
                response = yield http.fetch(request)
                self.log.info('From: {address} received the response: {response}'
                              .format(address=address, response=str(response.body.decode('utf-8'))))
                '''
                Copying headers
                '''
                self.__header_hendler(response)
                '''
                Sending the response to client
                '''
            except ConnectionRefusedError:
                self.__response_about_not_found()
            except tornado.httpclient.HTTPError:
                self.__response_about_failed_connection()
            else:
                self.__positive_response(response)
        if not valid:
            self.__response_about_incorrect_request()
        self.finish()

    def __create_request_to_server(self, address, data):
        self.log.info('To {address} sent the request: {data}'.format(address=address, data=data))
        request = tornado.httpclient.HTTPRequest('http://{address}'.format(address=address),
                                                 body=data, method="POST", request_timeout=0)
        return request

    def __header_hendler(self, response):
        for key in response.headers:
            self.clear_header(key)
            self.add_header(key, response.headers[key])

    def __positive_response(self, response):
        self.write(response.body.decode('utf-8'))
        self.log.info('To client sent the response: {response}'
                      .format(response=str(response.body.decode('utf-8'))))
        self.set_status(200)

    def __response_about_incorrect_request(self):
        notification = ' Bad Request'
        self.log.info('To client sent a response: {notification}'
                      .format(notification=str(notification)))
        self.set_status(400, reason=notification)

    def __response_about_not_found(self):
        notification = 'Relevant server is not available'
        self.log.info('To client sent a response: {notification}'
                      .format(notification=str(notification)))
        self.set_status(404, reason=notification)

    def __response_about_failed_connection(self):
        notification = 'Gateway Timeout'
        self.log.info('To client sent a response: {notification}'
                      .format(notification=str(notification)))
        self.set_status(504, reason=notification)

    def __check_request(self, request_data):
        val = Validator(request_data)
        if val.is_json() and val.is_structure() and val.is_valid():
            return True
        else:
            return False