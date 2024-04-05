import xml.etree.ElementTree as et
import rwgraph._util._etElement_find as etfind
import rwgraph._util._str_util as strutil

class ElementProperties:
    def __init__(self, tag:str, default_properties:dict[str, str], optional_properties:dict[str, str])->None:
        self.tag = tag
        self.default_properties = default_properties
        self.optional_properties = optional_properties
        
    @classmethod
    def init_etElement(cls, root:et.Element):
        if root == None:
            return None
        return cls(root.tag, root.attrib, etfind._get_etElement_properties(etfind._get_etElement_callable_from_tag(root, "properties")))
        
    def output_etElement(self, root:et.Element)->None:
        root.tag = self.tag
        root.attrib = self.default_properties
        root.append(etfind._output_etElement_properties(self.optional_properties))
        
    def output_str(self)->str:
        str_ans = ""
        str_ans = str_ans + self.tag + ":\n"
        str_ans = str_ans + "default_properties:" + str(self.default_properties) + "\n"
        str_ans = str_ans + "optional_properties:" + str(self.optional_properties) + "\n"
        str_ans = strutil.indentstr_Tab(str_ans)
        return str_ans