import configparser
import sys


def config_parser(full_path_config):
    config = configparser.ConfigParser()
    file = full_path_config
    config.read(file)
    try:
        delay = config.getfloat('startup_parameters','delay')
        print("Delay = {time} seconds".format(time=delay))
        return delay
    except (TypeError, configparser.NoSectionError, configparser.NoOptionError):
        print('Config file is not correct or not found')
        sys.exit(1)