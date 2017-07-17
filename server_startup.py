import tornado.web
from tornado.ioloop import IOLoop

from server.cmd_parser import create_parser
from server.server_main import MainHandler
from server.startup_control import StartupControl
from server.config_parser import config_parser
from utilities.logger_operator import Logger


app_settings = dict(
        debug=True,
        )

application = tornado.web.Application([
    (r"/", MainHandler)
], **app_settings)

package = 'server'
service = 'Server'
log_extension = '.log'
full_path_config = 'server/config.ini'

if __name__ == '__main__':
    try:
        parser = create_parser()
        namespace = parser.parse_args()
        delay = config_parser(full_path_config)
        control = StartupControl()
        if control.check_numdber_of_port(namespace.number_of_port) and\
                control.check_version(namespace.version):
            logger = Logger(package, namespace.number_of_port,
                                service, log_extension).get_logger()
            application.logger = logger
            application.version = namespace.version
            application.delay = delay
            application.listen(namespace.number_of_port)
            print('Server Running...')
            print('Press ctrl + c to close')
            IOLoop.instance().start()
        else:
             print('Server startup parameters are not correct')
    except KeyboardInterrupt:
        print('Server is finished')
    except (ValueError, AttributeError):
        print('Server startup parameters or content '
              'of config file are not correct \n'
              'Check the contents of the configuration file and try again')
    except FileNotFoundError:
        print('Route table was not found')
    except OSError:
        print('There are no access rights to the socket')