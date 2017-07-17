import xml.etree.ElementTree as ET


class RouteTable():
    def __init__(self, logger, path_to_table, additional_server):
        self.log = logger
        self.__additional_address = additional_server
        self.__create_table(path_to_table)

    def get_address(self, id):
        try:
            address = self.__route_table[id]
            self.log.info('Select: {address} for device with id: {id} '
                          .format(address=address, id=self.__route_table[id]))
            return address
        except KeyError:
            self.log.info('Select: {address} for device with id: {id} '
                          .format(address=self.__additional_address, id=self.__route_table[id]))
            return self.__additional_address

    def __create_table(self, path_to_table):
        self.__route_table = {}
        tree = ET.parse(path_to_table)
        root = tree.getroot()
        for address_block in root:
            address = address_block.attrib['value']
            for id_block in address_block:
                id = id_block.text
                self.valid(id)
                self.__write_to_table(id, address)

    def __write_to_table(self, id, address):
        old_address = self.__route_table.get(id)
        if old_address is not None:
            self.__print_id_collision(id, address, old_address)
        self.__route_table[id] = address

    def valid(self, id):
        if not id.isdigit():
            warning_message_incorrect_id = 'Route table create warning: ' \
                                           'Id: {id} is not correct'
            message = warning_message_incorrect_id.format(id=id)
            self.log.info(message)
            return False
        else:
            return True

    def __print_id_collision(self, id, address, old_address):
        warning_message_template = 'Route table create warning: ' \
                                   'Id: {id} is already exists with address:  ' \
                                   '{old_address} Address has replaced with: {address}'
        message = warning_message_template\
                  .format(id=id, address=address, old_address=old_address)
        self.log.info(message)