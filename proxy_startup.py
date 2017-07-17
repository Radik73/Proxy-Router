import tornado.web
import tornado.httpclient
from tornado.ioloop import IOLoop


from proxy.proxy_main import MainHandler
from proxy.route_table import RouteTable
from proxy.settings_parser import settings_parser
from utilities.logger_operator import Logger

app_settings = dict(
             debug=True,
        )

application = tornado.web.Application(
    [(r"/", MainHandler)], **app_settings)

package = 'proxy'
service = 'Proxy'
extension = '.log'
name = 'Info'
full_path_config = 'proxy/settings.conf'

if __name__ == "__main__":
    try:
        additional_server, path_to_table, port = settings_parser(full_path_config)
        logger = Logger(package, name, service, extension).get_logger()
        table = RouteTable(logger, path_to_table, additional_server)
        application.logger = logger
        application.table = table
        application.listen(port)
        print('Server Running...')
        print('Press ctrl + c to close')
        IOLoop.instance().start()
    except KeyboardInterrupt:
        print('Server is finished')
    except (ValueError, AttributeError):
        print('Server startup parameters are not correct')
    except FileNotFoundError:
        print('Route table was not found')
    except OSError:
        print('There are no access rights to the socket')
    except SyntaxError:
        print('Incorrect port number entered if settings.py')
    except ValueError:
        print('Check the contents of the configuration file and try again')