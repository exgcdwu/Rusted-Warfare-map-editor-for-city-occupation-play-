import xml.etree.ElementTree as et
import numpy as np

from xml.dom import minidom

import rwmap._frame as frame
import rwmap._util._str_util as str_utility

def get_etElement_properties(root:et.Element)->dict[str,str]:
    if root == None:
        return None
    dict_properties = {}
    for nproperty in root:
        if nproperty.attrib.get('value') == None:
            nproperty.attrib['value'] = ""
        dict_properties[nproperty.attrib['name']] = nproperty.attrib['value']
    return dict_properties

def output_etElement_properties(dict_properties:dict[str, str])->et.Element:
    root = et.Element("properties")
    if dict_properties != None:
        for name, value in dict_properties.items():
            root.append(et.Element("property", attrib = {"name":name, "value":value}))
    return root

def get_etElement_name_to_text_rm(root:et.Element, name:str)->str:
    if root == None:
        return None
    for nproperty in root:
        if nproperty.attrib['name'] == name:
            text = nproperty.text
            root.remove(nproperty)
            return text

def get_etElement_ndarray_from_text_packed(root:et.Element, reshape_Coordinate:frame.Coordinate)->np.ndarray:
    if root == None:
        return None
    nmatrix = str_utility.ndarray_from_text_packed(root.text, root.attrib["encoding"], root.attrib["compression"])
    nmatrix = np.reshape(nmatrix, [reshape_Coordinate.y(), reshape_Coordinate.x()])
    return nmatrix

def get_etElement_from_text_packed(tilematrix:np.ndarray, encoding:str, compression:str)->et.Element:
    root = et.Element("data", {"encoding": encoding, "compression": compression})
    root.text = str_utility.text_packed_from_ndarray(tilematrix, encoding, compression)
    return root

def get_etElement_callable_from_tagone(root:et.Element, tag:str)->et.Element:
    if root == None:
        return None
    for etchild in root:
        if etchild.tag == tag:
            return etchild
        
def get_etElement_callable_from_taglist(root:et.Element, tag_list:list[str])->et.Element:
    if root == None:
        return None
    for tagnow in tag_list:
        root = get_etElement_callable_from_tagone(root, tagnow)
    return root

def get_etElement_callable_from_tag(root:et.Element, tag:str)->et.Element:
    if root == None:
        return None
    tag_list = tag.split(",")
    return get_etElement_callable_from_taglist(root, tag_list)

def output_file_from_etElement(root:et.Element, file:str)->None:
    dom = minidom.parseString(et.tostring(root, encoding='utf-8'))
    pretty_xml = dom.toprettyxml(indent='  ')
    with open(file, 'w', encoding='utf-8') as file_now:
        file_now.write(pretty_xml)

