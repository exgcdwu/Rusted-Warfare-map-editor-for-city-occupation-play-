# -*- coding: utf-8 -*-
"""

"""

import xml.etree.ElementTree as et
import os
import importlib

current_dir = os.getcwd()
utility = importlib.import_module(current_dir + '\\_util')

class RWGraph:
    @classmethod
    def init_graphfile(cls, graph_file:str)->None:
        xmlTree:et.ElementTree = et.ElementTree(file=graph_file)
        root:et.Element = xmlTree.getroot()
        cls.map_properties =  utility.ElementProperties.init_etElement(root)
        

