# -*- coding: utf-8 -*-
"""

"""
import xml.etree.ElementTree as et
import numpy as np

import rwgraph._util as utility

class Layer:
    def __init__(self, layer_properties:utility.ElementProperties, tilematrix:np.ndarray)->None:
        self.layer_properties = layer_properties
        self.tilematrix = tilematrix
    @classmethod
    def init_etElement(cls, root:et.Element)->None:
        layer_properties = utility.ElementProperties.init_etElement(root)
        tilematrix = utility._get_etElement_ndarray_from_text_packed(utility._get_etElement_callable_from_tag(root, "data"), utility.Coordinate(root.attrib['width'], root.attrib['height']))
        return cls(layer_properties, tilematrix)

    def output_str(self, output_rectangle:utility.Rectangle = utility.Rectangle(utility.Coordinate(), utility.Coordinate(-1, -1)))->str:
        str_ans = ""
        str_ans = str_ans + self.layer_properties.output_str() + "\n"
        str_ans = str_ans + "".join([" ".join([self.tilematrix[i][j] for j in range(output_rectangle.i().y(), output_rectangle.e().y())]) + "\n"
                                 for i in range(output_rectangle.i().x(), output_rectangle.e().x())]) + "\n"
        str_ans = utility.indentstr_Tab(str_ans)
        return str_ans

    def output_etElement(self)->et.Element:
        root = et.Element("layer")
        self.layer_properties.output_etElement(root)
        root.append(utility._get_etElement_from_text_packed(self.tilematrix))
        return root
        
