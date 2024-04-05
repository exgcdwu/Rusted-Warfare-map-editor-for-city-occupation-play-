import xml.etree.ElementTree as et

def _get_etElement_optional_properties(root:et.Element)->dict[str,str]:
    dict_properties = {}
    for properties in root:
        if properties.tag == "properties":
            for nproperty in properties:
                dict_properties[nproperty.attrib['name']] = nproperty.attrib['value']

def _output_etElement_optional_properties(dict_properties:dict[str, str])->et.Element:
    nproperty = []
    for name, value in dict_properties.items():
        nproperty.append(et.Element("property", attrib = {"name":name, "value":value}))
    return et.Element("properties", nproperty)

class ElementProperties:
    def __init__(self, tag:str, default_properties:dict[str, str], optional_properties:dict[str, str])->None:
        self.tag = tag
        self.default_properties = default_properties
        self.optional_properties = optional_properties
        
    @classmethod
    def init_etElement(cls, root:et.Element)->None:
        cls.tag = root.tag
        cls.default_properties = root.attrib
        cls.optional_properties = _get_etElement_optional_properties(root)
        
    def output_etElement(self, root:et.Element)->None:
        root.tag = self.tag
        root.attrib = self.default_properties
        root.append(_output_etElement_optional_properties(self.optional_properties))
        
    def print_str(self)->None:
        str_ans = self.tag + "\n"
        str_ans = "default_properties:" + self.default_properties + "\n"
        str_ans = "optional_properties:" + self.optional_properties + "\n"
        return str_ans