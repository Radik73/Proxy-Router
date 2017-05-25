from http.server import HTTPServer
import server.checking as check
import server.cmd_parser as prs
from http.server import BaseHTTPRequestHandler
import json
import time
import server.checking as chek
import server.response_shaper as rs
import logging
import server.config as cnfg


class HttpProcessor(BaseHTTPRequestHandler):
    def __set_log(self):
        self.name = namespace.number_of_port
        self.file_name = 'server/' + str(self.name) + '_server.log'
        logging.basicConfig(filename=self.file_name, level=logging.INFO)
        self.logger = logging.getLogger("Server")

    def do_POST(self):
        self.__set_log()
        payload = self.parse()
        if payload != None:
            data = json.dumps(payload)
            response = bytes(data, "utf-8")
            self.logger.info('Sent a response: ' + str(payload))
            time.sleep(delay)
            self.send_response(200)
            self.send_header("Content-Type", 'text/html')
            self.send_header("Content-Length", str(len(response)))
            self.end_headers()
            self.wfile.write(response)
        elif payload == None:
            notification = 'Structure of request is not correct'
            response = bytes(json.dumps(notification), "utf-8")
            self.logger.info('Sent a response: ' + str(notification))
            time.sleep(delay)
            self.send_response(200)
            self.send_header("Content-Type", 'text/html')
            self.send_header("Content-Length", str(len(response)))
            self.end_headers()
            self.wfile.write(response)

    def parse(self):
        length = int(self.headers["Content-Length"])
        post_data = str(self.rfile.read(length), "utf-8")
        parsed_string = json.loads(post_data)
        self.logger.info('The request received: ' + str(parsed_string))
        if chek.inspect(parsed_string) == True:
            json_package = rs.shaper(parsed_string)
            return json_package

def create_settings_of_server(port):
    try:
        serv = HTTPServer(("127.0.0.1", int(port)), HttpProcessor)
        print('Server Running...')
        print('Press ctrl + c to close')
        serv.serve_forever()
    except OSError:
        print('There are no access rights to the socket')
    except KeyboardInterrupt:
        print('Server is finished')


if __name__ == '__main__':
    parser = prs.createParser()
    namespace = parser.parse_args()
    delay = int(cnfg.delay_config())
    if check.inspect_for_numdber_of_port(namespace.number_of_port):
        num_port = namespace.number_of_port
        create_settings_of_server(num_port)
    else:
        print('Server startup parameters are not correct')