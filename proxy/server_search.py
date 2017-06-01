import xml.etree.ElementTree as ET
import logging


adress_of_additional_server = '127.0.0.1:8886'
table = 'proxy/table.xml'


def ip_search_engine(id):
    tree = ET.parse('proxy/table.xml')
    id = str(id)
    root = tree.getroot()
    for i in root:
        for j in i:
            elem = j.text
            if elem == id:
                ach = i.attrib
                ip = str(ach['value'])
                return (ip)

def check(ip):
    if ip == None:
        logging.info('Target server selected: ' + adress_of_additional_server)
        return adress_of_additional_server
    else:
        logging.info('Target server selected: ' + ip)
        return ip