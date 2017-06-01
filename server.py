import server.checking as check
import server.cmd_parser as prs
import json
import server.checking as chek
import server.response_shaper as rs
import logging
import server.config as cnfg
import time
import server.select as slc
import tornado.web
from tornado.ioloop import IOLoop
from tornado import gen


@gen.coroutine
def async_sleep(seconds):
    yield gen.Task(IOLoop.instance().add_timeout, time.time() + seconds)


class MainHandler(tornado.web.RequestHandler):
    def __set_log(self):
        self.logger = logging.getLogger("Server")

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        self.__set_log()
        payload = self.parse()
        if payload != None:
            data = json.dumps(payload)
            response = bytes(data, "utf-8")
            version = slc.select(namespace.number_of_port)
            self.add_header("Server", version)
            self.add_header("Content-Type", 'text/html')
            self.add_header("Content-Length", str(len(response)))
            yield async_sleep(delay)
            self.logger.info('Sent a response: ' + str(payload))
            self.write(response)
            self.finish()
        elif payload == None:
            notification = 'Structure of request is not correct'
            response = bytes(json.dumps(notification), "utf-8")
            print('Res: ' + notification)
            version = slc.select(namespace.number_of_port)
            self.add_header("Server", version)
            self.add_header("Content-Type", 'text/html')
            self.add_header("Content-Length", str(len(response)))
            yield async_sleep(delay)
            self.logger.info('Sent a response: ' + str(notification))
            self.write(response)
            self.finish()


    def parse(self):
        parsed_string = json.loads(self.request.body.decode('utf-8'))
        self.logger.info('The request received: ' + str(parsed_string))
        if chek.inspect(parsed_string) == True:
            json_package = rs.shaper(parsed_string)
            return json_package

app_settings = dict(
        debug=True,
        )

application = tornado.web.Application([
    (r"/", MainHandler)
], **app_settings)

def create_settings_of_server(port):
    try:
        application.listen(port)
        print('Server Running...')
        print('Press ctrl + c to close')
        IOLoop.instance().start()
    except OSError:
        print('There are no access rights to the socket')
    except KeyboardInterrupt:
        print('Server is finished')


if __name__ == '__main__':
    parser = prs.createParser()
    namespace = parser.parse_args()
    delay = int(cnfg.delay_config())
    logging.basicConfig(filename="server/" + namespace.number_of_port + "_server.log", level=logging.INFO)
    if check.inspect_for_numdber_of_port(namespace.number_of_port):
        num_port = namespace.number_of_port
        create_settings_of_server(num_port)
    else:
        print('Server startup parameters are not correct')