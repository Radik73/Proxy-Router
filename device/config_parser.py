import configparser
import sys


def config_parser(full_path):
    config = configparser.ConfigParser()
    file = full_path
    config.read(file)
    try:
        delay = config.getfloat('startup_parameters','delay')
        timeout = config.getfloat('startup_parameters','timeout')
        print("Delay = {time} seconds".format(time=delay))
        print("Timeout = {time} seconds".format(time=timeout))
        return delay, timeout
    except (TypeError, configparser.NoSectionError, configparser.NoOptionError):
        print('Config file is not correct or not found')
        sys.exit(1)