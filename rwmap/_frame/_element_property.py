import xml.etree.ElementTree as et
from copy import deepcopy
from typing import Union
import regex as re

import rwmap._util as utility

class ElementProperties:
    pass

class ElementProperties:
    def __init__(self, tag:str, default_properties:dict[str, str] = {}, optional_properties:dict[str, Union[str, dict[str, str]]] = {})->None:
        self._tag = tag
        self._default_properties = deepcopy(default_properties)
        self._optional_properties = deepcopy(optional_properties)
        
    @classmethod
    def init_etElement(cls, root:et.Element):
        if root == None:
            return None
        optional_properties = utility.get_etElement_properties(utility.get_etElement_callable_from_tag_s(root, "properties"))
        return cls(root.tag, root.attrib, optional_properties)
        
    def output_etElement(self, root:et.Element)->et.Element:
        etElement_ans = deepcopy(root)
        etElement_ans.tag = deepcopy(self._tag)
        if self._default_properties != {}:
            etElement_ans.attrib = deepcopy(self._default_properties)
        if self._optional_properties != {}:
            etElement_ans.append(utility.output_etElement_properties(self._optional_properties))
        return etElement_ans
        
    def output_str(self)->str:
        str_ans = ""
        str_ans = str_ans + self._tag + ":\n"
        str_ans = str_ans + "default_properties:" + str(self._default_properties) + "\n"
        str_ans = str_ans + "optional_properties:" + str(self._optional_properties) + "\n"
        str_ans = utility.indentstr_Tab(str_ans)
        return str_ans
    
    def __lt__(self, other:ElementProperties)->bool:
        return int(self.returnDefaultProperty("id")) < int(other.returnDefaultProperty("id"))

    def assignDefaultProperty(self, name:str, value:Union[str, dict[str, str]]):
        self._default_properties[name] = value
    
    def assignOptionalProperty(self, name:str, value:Union[str, dict[str, str]]):
        self._optional_properties[name] = value

    def assignOptionalProperty_text(self, name:str, value:str):
        self.assignOptionalProperty(name, {'text': value})

    def returnDefaultProperty(self, name:str)->Union[str, dict[str, str]]:
        return deepcopy(self._default_properties.get(name))
    
    def returnOptionalProperty(self, name:str)->Union[str, dict[str, str]]:
        return deepcopy(self._optional_properties.get(name))
    
    def deleteDefaultProperty(self, name:str)->None:
        if self._default_properties.get(name) != None:
            self._default_properties.pop(name)
    def deleteOptionalProperty(self, name:str)->None:
        if self._optional_properties.get(name) != None:
            self._optional_properties.pop(name)
    def deleteDefaultPropertySup(self, name_list:list[str])->None:
        dict_now = {}
        for name in name_list:
            if self.returnDefaultProperty(name) != None:
                dict_now[name] = self.returnDefaultProperty(name)
        self._default_properties = dict_now
    def deleteOptionalPropertySup(self, name_list:list[str])->None:
        dict_now = {}
        for name in name_list:
            if self.returnOptionalProperty(name) != None:
                dict_now[name] = self.returnOptionalProperty(name)
        self._optional_properties = dict_now
    
    def isreDefaultProperty(self, name:str, value_re:Union[str, dict[str, str]])->bool:
        value = self.returnDefaultProperty(name)
        value = value if value != None else ''
        return re.match(value_re, value)

    
    def isreOptionalProperty(self, name:str, value_re:Union[str, dict[str, str]])->bool:
        value = self.returnOptionalProperty(name)
        value = value if value != None else ''
        return re.match(value_re, value)