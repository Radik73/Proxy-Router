import json
import tornado.web
import tornado.ioloop
import tornado.websocket
import tornado.gen
import tornado.escape
import tornado.httpclient
import proxy.server_search as ips
import logging

logging.basicConfig(filename="proxy/proxy_info.log", level=logging.INFO)

class MainHandler(tornado.web.RequestHandler):

    def __set_log(self):
        self.logger = logging.getLogger("Proxy")

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        data, device_id = self.__id_search()
        self.__set_log()
        self.logger.info('The request received from client: ' + str(data))
        ip_adress = ips.ip_search_engine(device_id)
        self.adress = ips.check(ip_adress)
        try:
            http = tornado.httpclient.AsyncHTTPClient()
            self.logger.info('To ' + self.adress +  ' Sent a request: ' + str(json.dumps(data)))
            request=tornado.httpclient.HTTPRequest('http://' + self.adress, body=json.dumps(data), method="POST")
            response = yield http.fetch(request)
            self.answer = self.__packaging(response)
            self.__header_hendler(response)
        except ConnectionRefusedError:
            notification = 'Relevant server is not available'
            self.logger.info('To client sent a response: ' + str(notification))
            self.write(notification)
        else:
            self.write(self.answer)
            self.logger.info('To client sent a response: ' + str(self.answer))
        finally:
            self.finish()

    def __packaging(self, response):
        payload = json.loads(response.body.decode('utf-8'))
        self.logger.info('From: ' + self.adress + ' Response received: ' + str(payload))
        data = json.dumps(payload)
        return data

    def __id_search(self):
        key = 'device_id'
        data = json.loads(self.request.body.decode('utf-8'))
        device_id = data[key]
        return data, device_id

    def __header_hendler(self, response):
        for key in response.headers:
            self.clear_header(key)
            self.add_header(key, response.headers[key])


app_settings = dict(
            debug=True,
        )

application = tornado.web.Application([
    (r"/", MainHandler)
], **app_settings)