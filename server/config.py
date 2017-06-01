import xml.etree.ElementTree as ET

def delay_config():
    tree = ET.parse('server/config.xml')
    root = tree.getroot()
    delay = root.text
    return delay