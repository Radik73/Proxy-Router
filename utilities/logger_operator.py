import logging
import sys

class Logger():
    def __init__(self, package_path, identification, service, extension):
        self.set_log_file(package_path, identification, service, extension)

    def set_logger(self, extension):
        self.logger = logging.getLogger(extension)

    def set_log_file(self, package_path, identificator, service, extension):
        name = "{package}/{identification}_{service}{extension}"\
            .format(package=package_path, identification=identificator,
                service=service, extension=extension)

        logging.basicConfig(
            level=logging.DEBUG,
            format='[%(asctime)s]  %(levelname)-5s %(message)s',
            handlers=[
            logging.FileHandler(name, encoding='utf8'),
            logging.StreamHandler(stream=sys.stdout),
            ],
        )
        self.set_logger(service)

    def get_logger(self):
        return self.logger