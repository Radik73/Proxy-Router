import configparser
import sys


def settings_parser(full_path_config):
    config = configparser.ConfigParser()
    file = full_path_config
    config.read(file)
    try:
        additional_server = config.get('settings','address_of_additional_server')
        path_to_table = config.get('settings','path_to_table')
        port = config.getint('settings','proxy_port_number')
        return additional_server, path_to_table, port
    except (TypeError, configparser.NoSectionError, configparser.NoOptionError):
        print('Config file is not correct or not found')
        sys.exit(1)