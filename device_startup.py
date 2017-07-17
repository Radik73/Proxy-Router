import device.utilities_device as utilities
from device.device_main import Device
from device.startup_control import StartupControl
from device.config_parser import config_parser
from utilities.logger_operator import Logger


package_path = 'device'
service = 'Device'
log_extension = '.log'
full_path_config = 'device/config.ini'

if __name__ == '__main__':
    try:
        parser = utilities.create_parser()
        namespace = parser.parse_args()
        delay, timeout = config_parser(full_path_config)
        control = StartupControl()
        if control.check_digit(namespace.number_of_port) and control.check_ip(namespace.ip) and\
                               control.check_digit(namespace.id):
            logger = Logger(package_path, namespace.id,
                            service, log_extension).get_logger()
            Device(namespace.id, namespace.ip, namespace.number_of_port,
                   timeout, delay, logger)
            utilities.work_simulation()
        else:
            print('Startup parameters are not correct')
    except (ValueError, AttributeError):
        print('Server startup parameters or content '
            'of config file are not correct \n'
            'Check the contents of the configuration file and try again')
    except KeyboardInterrupt:
        print('Device is finished')