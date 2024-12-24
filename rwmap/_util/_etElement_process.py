import xml.etree.ElementTree as et
import numpy as np
from typing import Union
from copy import deepcopy

from xml.dom import minidom


import rwmap._frame as frame
import rwmap._util._str_util as str_utility
import rwmap._util._dict_util as dict_utility

def get_etElement_properties(root:et.Element)->dict[str,Union[str, dict[str, str]]]:
    rootn = deepcopy(root)
    if rootn == None:
        return {}
    dict_properties = {}
    for nproperty in rootn:
        if nproperty.text != None and nproperty.text != "":
            nproperty.attrib['text'] = nproperty.text

        if nproperty.attrib.get('value') == None:
            nproperty.attrib['value'] = ""
        if len(nproperty.attrib) == 2:
            dict_properties[nproperty.attrib['name']] = nproperty.attrib['value']
        else:
            name_now = nproperty.attrib["name"]
            nproperty.attrib.pop('name')
            if nproperty.attrib.get('value') != None and nproperty.attrib.get('value') == "":
                nproperty.attrib.pop('value')
            dict_properties[name_now] = nproperty.attrib
    return dict_properties

def output_etElement_properties(dict_properties:dict[str, Union[dict[str, str], str]])->et.Element:
    root = et.Element("properties")
    if dict_properties != None:
        for name, value in dict_properties.items():
            dict_n = {"name":name}
            value_n = dict_utility.udictstr_to_dict(value)
            if isinstance(value_n, list):
                dict_n.update(value_n[0])
                nproperty = et.Element("property", dict_n)
                nproperty.text = value_n[1]
            else:
                dict_n.update(value_n)
                nproperty = et.Element("property", dict_n)
            root.append(nproperty)
    return root

def get_etElement_name_to_text_s(root:et.Element, name:str)->Union[str, None]:
    if root == None:
        return None
    for nproperty in root:
        if nproperty.attrib['name'] == name:
            text = nproperty.text
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

def get_etElement_callable_from_tagone_s(root:et.Element, tag:str)->et.Element:
    if root == None:
        return None
    for etchild in root:
        if etchild.tag == tag:
            return etchild
        
def get_etElement_callable_from_taglist_s(root:et.Element, tag_list:list[str])->et.Element:
    if root == None:
        return None
    for tagnow in tag_list:
        root = get_etElement_callable_from_tagone_s(root, tagnow)
    return root

def get_etElement_callable_from_tag_s(root:et.Element, tag:str)->et.Element:
    if root == None:
        return None
    tag_list = tag.split(",")
    return get_etElement_callable_from_taglist_s(root, tag_list)
        
def get_etElement_callable_from_taglist_sup_s(root:et.Element, tag_set:set[str])->list[et.Element]:
    if root == None:
        return []
    et_list = []
    for etchild in root:
        if not etchild.tag in tag_set:
            et_list.append(etchild)
    return et_list

def get_etElement_callable_from_tag_sup_s(root:et.Element, tag:str)->list[et.Element]:
    if root == None:
        return []
    tag_set = set(tag.split(","))
    return get_etElement_callable_from_taglist_sup_s(root, tag_set)

def output_file_from_etElement(root:et.Element, file:str)->None:
    dom = minidom.parseString(et.tostring(root, encoding='utf-8'))
    pretty_xml = dom.toprettyxml(indent='  ')
    with open(file, 'w', encoding='utf-8') as file_now:
        file_now.write(pretty_xml)

