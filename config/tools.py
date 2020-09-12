"""
by shenjack(shenjackyuanjie)
"""

import xml
import xml.dom.minidom
from xml.dom.minidom import parse

def get_At(name, in_xml, need_type=str):
    name_type = type(name)
    if name_type == list:
        At_list = []
        for need_name in name:
            get = in_xml.getAttribute(need_name)
            At_list.append(need_type(get))
        return At_list
    elif name_type == str:
        At = in_xml.getAttribute(name)
    else:
        raise TypeError('only str and list type is ok but you give me a' + name_type + 'type')
    return need_type(At)

def load_xml(xml_name, getEBTN=''):
    xml_load = xml.dom.minidom.parse(xml_name)
    if not (getEBTN == ''):
        xml_get = xml_load.getElementsByTagName(getEBTN)
        return xml_get
    else:
        return xml_load
