# -*- coding: utf-8 -*-
"""

"""

import xml.etree.ElementTree as et

import rwgraph._util as utility

class ObjectGroup:
    def __init__(self, objectgroup_properties:utility.ElementProperties, object_list:list[utility.ElementProperties])->None:
        self.objectgroup_properties = objectgroup_properties
        self.object_list = object_list
    @classmethod
    def init_etElement(cls, root:et.Element)->None:
        objectgroup_properties = utility.ElementProperties.init_etElement(root)
        object_list = [utility.ElementProperties.init_etElement(tobject) for tobject in root if tobject.tag == "object"]
        return cls(objectgroup_properties, object_list)
    
    def output_str(self, objectnum:int = -1)->str:
        str_ans = ""
        str_ans = str_ans + "objectgroup" + ":\n"
        str_ans = str_ans + self.objectgroup_properties.output_str() + "\n"
        str_ans = str_ans + "".join([self.object_list[i].output_str() + "\n" for i in range(0, -1)]) + "\n"
        str_ans = utility.indentstr_Tab(str_ans)
        return str_ans

    def output_etElement(self)->et.Element:
        root = et.Element("objectgroup")
        self.objectgroup_properties.output_etElement(root)
        for tobject in self.object_list:
            tobject_element = et.Element("object")
            tobject.output_etElement(tobject_element)
            root.append(tobject_element)
        return root

