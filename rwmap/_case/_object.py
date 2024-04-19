import xml.etree.ElementTree as et

import rwmap._frame as frame
import rwmap._util as utility
class TObject(frame.ElementProperties):
    def __init__(self, tag:str, default_properties:dict[str, str] = {}, optional_properties:dict[str, str] = {}, other_properties:list[et.Element] = [])->None:
        super().__init__(tag, default_properties, optional_properties)
        self._other_properties = other_properties
        
    @classmethod
    def init_etElement(cls, root:et.Element):
        if root == None:
            return None
        optional_properties = utility.get_etElement_properties(utility.get_etElement_callable_from_tag(root, "properties"))
        other_properties = []
        for etEle in root:
            if etEle.tag != "properties":
                other_properties.append(etEle)
        return cls(root.tag, root.attrib, optional_properties, other_properties)
    
    def output_etElement(self, root:et.Element)->None:
        super().output_etElement(root)
        for etEle in self._other_properties:
            root.append(etEle)
        
    def output_str(self)->str:
        str_ans = super().output_str()
        str_add = "other_properties:" + str(self._other_properties) + "\n"
        str_add = utility.indentstr_Tab(str_ans)
        str_ans = str_ans + str_add
        return str_ans
        