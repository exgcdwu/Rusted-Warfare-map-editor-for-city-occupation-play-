import xml.etree.ElementTree as et
import numpy as np
import zlib
import base64

import rwgraph._util._coordinate as coo


def _get_etElement_properties(root:et.Element)->dict[str,str]:
    if root == None:
        return None
    dict_properties = {}
    for nproperty in root:
        if nproperty.attrib.get('value') == None:
            nproperty.attrib['value'] = ""
        dict_properties[nproperty.attrib['name']] = nproperty.attrib['value']
    return dict_properties

def _output_etElement_properties(dict_properties:dict[str, str])->et.Element:
    root = et.Element("properties")
    if dict_properties != None:
        for name, value in dict_properties.items():
            root.append(et.Element("property", attrib = {"name":name, "value":value}))
    return root

def _get_etElement_name_to_text_rm(root:et.Element, name:str)->str:
    if root == None:
        return None
    for nproperty in root:
        if nproperty.attrib['name'] == name:
            text = nproperty.text
            root.remove(nproperty)
            return text

def _ndarray_from_text_packed(text:str)->np.ndarray:
    nmatrix = np.frombuffer(zlib.decompress(base64.b64decode(text)), dtype=np.uint32)
    return nmatrix

def _text_packed_from_ndarray(ndarray_now:np.ndarray):
    text_packed = base64.b64encode(zlib.compress(ndarray_now.flatten().tobytes())).decode(encoding="utf-8")
    return text_packed

def _get_etElement_ndarray_from_text_packed(root:et.Element, reshape_Coordinate:coo.Coordinate)->np.ndarray:
    if root == None:
        return None
    nmatrix = _ndarray_from_text_packed(root.text)
    nmatrix = np.reshape(nmatrix, [reshape_Coordinate.x(), reshape_Coordinate.y()])
    return nmatrix

def _get_etElement_from_text_packed(tilematrix:np.ndarray)->et.Element:
    root = et.Element("data", {"encoding": "base64", "compression": "zlib"})
    root.text = _text_packed_from_ndarray(tilematrix)
    return root

def _get_etElement_callable_from_tagone(root:et.Element, tag:str)->et.Element:
    if root == None:
        return None
    for etchild in root:
        if etchild.tag == tag:
            return etchild
        
def _get_etElement_callable_from_taglist(root:et.Element, tag_list:list[str])->et.Element:
    if root == None:
        return None
    for tagnow in tag_list:
        root = _get_etElement_callable_from_tagone(root, tagnow)
    return root

def _get_etElement_callable_from_tag(root:et.Element, tag:str)->et.Element:
    if root == None:
        return None
    tag_list = tag.split(",")
    return _get_etElement_callable_from_taglist(root, tag_list)