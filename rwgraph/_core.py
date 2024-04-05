# -*- coding: utf-8 -*-
"""

"""

import xml.etree.ElementTree as et

class RWGraph:
    @classmethod
    def init_graphfile(cls, graph_file:str)->None:
        xmlTree:et.ElementTree = et.ElementTree(file=graph_file)
        root:et.Element = xmlTree.getroot()
        cls.map_default_properties = root.attrib()
        cls.map_optional_properties = root.pro

