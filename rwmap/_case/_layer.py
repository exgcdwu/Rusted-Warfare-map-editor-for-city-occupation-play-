# -*- coding: utf-8 -*-
"""

"""
import xml.etree.ElementTree as et
import numpy as np

import rwmap._util as utility
import rwmap._frame as frame

class Layer(frame.ElementOri):
    def __init__(self, properties:frame.ElementProperties, tilematrix:np.ndarray, encoding:str, compression:str)->None:
        super().__init__(properties)
        self._tilematrix = tilematrix
        self._encoding = encoding
        self._compression = compression
    @classmethod
    def init_etElement(cls, root:et.Element)->None:
        properties = frame.ElementProperties.init_etElement(root)
        data = utility.get_etElement_callable_from_tag(root, "data")
        _tilematrix = utility.get_etElement_ndarray_from_text_packed(data, frame.Coordinate(root.attrib['width'], root.attrib['height']))
        return cls(properties, _tilematrix, data.attrib["encoding"], data.attrib["compression"])

    def output_str(self, output_rectangle:frame.Rectangle = frame.Rectangle(frame.Coordinate(), frame.Coordinate(-1, -1)))->str:
        str_ans = ""
        str_ans = str_ans + self._properties.output_str() + "\n"
        str_ans = str_ans + "".join([" ".join([self._tilematrix[i][j] for j in range(output_rectangle.i().y(), output_rectangle.e().y())]) + "\n"
                                 for i in range(output_rectangle.i().x(), output_rectangle.e().x())]) + "\n"
        str_ans = utility.indentstr_Tab(str_ans)
        return str_ans

    def output_etElement(self)->et.Element:
        root = et.Element("layer")
        self._properties.output_etElement(root)
        root.append(utility.get_etElement_from_text_packed(self._tilematrix, self._encoding, self._compression))
        return root
    
    def id(self)->int:
        return int(self._properties.default_properties["id"])
    
    def tileid(self, place_grid:frame.Coordinate)->int:
        return int(self._tilematrix[place_grid.x()][place_grid.y()])
    
    def assigntileid(self, place_grid:frame.Coordinate, tileid:int):
        self._tilematrix[place_grid.x()][place_grid.y()] = tileid
    
    
    
        
