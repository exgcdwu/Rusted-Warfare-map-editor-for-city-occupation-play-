import xml.etree.ElementTree as et
from copy import deepcopy
from typing import Union

import rwmap._frame as frame
import rwmap._util as utility
from rwmap._frame._element_property import ElementProperties
class TObject(ElementProperties):
    pass
class TObject(ElementProperties):
    def __init__(self, tag:str, default_properties:dict[str, str] = {}, optional_properties:dict[str, Union[str, dict[str, str]]] = {}, other_properties:list[et.Element] = [])->None:
        super().__init__(tag, default_properties, optional_properties)
        self._other_properties = deepcopy(other_properties)

    def copy(self, tobject:TObject):
        self.__init__(tobject._tag, tobject._default_properties, tobject._optional_properties, tobject._other_properties)
    @classmethod
    def init_etElement(cls, root:et.Element):
        if root == None:
            return None
        optional_properties = utility.get_etElement_properties(utility.get_etElement_callable_from_tag_s(root, "properties"))
        other_properties = []
        for etEle in root:
            if etEle.tag != "properties":
                other_properties.append(deepcopy(etEle))
        return cls(root.tag, root.attrib, optional_properties, other_properties)
    
    def output_etElement(self, root:et.Element)->et.Element:
        etElement_ans = super().output_etElement(root)
        for etEle in self._other_properties:
            etElement_ans.append(deepcopy(etEle))
        return etElement_ans
        
    def output_str(self)->str:
        str_ans = super().output_str()
        str_add = "other_properties:" + str(self._other_properties) + "\n"
        str_ans = utility.indentstr_Tab(str_ans) + str_add
        return str_ans
    
    def __repr__(self)->str:
        return self.output_str()
        