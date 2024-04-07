import xml.etree.ElementTree as et
import rwmap._util as utility

class ElementProperties:
    def __init__(self, tag:str, default_properties:dict[str, str], optional_properties:dict[str, str])->None:
        self.tag = tag
        self._default_properties = default_properties
        self._optional_properties = optional_properties
        
    @classmethod
    def init_etElement(cls, root:et.Element):
        if root == None:
            return None
        return cls(root.tag, root.attrib, utility.get_etElement_properties(utility.get_etElement_callable_from_tag(root, "properties")))
        
    def output_etElement(self, root:et.Element)->None:
        root.tag = self.tag
        root.attrib = self._default_properties
        root.append(utility.output_etElement_properties(self._optional_properties))
        
    def output_str(self)->str:
        str_ans = ""
        str_ans = str_ans + self.tag + ":\n"
        str_ans = str_ans + "_default_properties:" + str(self._default_properties) + "\n"
        str_ans = str_ans + "_optional_properties:" + str(self._optional_properties) + "\n"
        str_ans = utility.indentstr_Tab(str_ans)
        return str_ans
    
    def assignDefaultProperty(self, name:str, value:str):
        self._default_properties[name] = value
    
    def assignOptionalProperty(self, name:str, value:str):
        self._optional_properties[name] = value

    def returnDefaultProperty(self, name:str):
        return self._default_properties.get(name)
    
    def returnOptionalProperty(self, name:str):
        return self._optional_properties.get(name)