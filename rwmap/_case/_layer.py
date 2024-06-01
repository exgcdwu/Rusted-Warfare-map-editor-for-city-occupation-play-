# -*- coding: utf-8 -*-
"""

"""
import xml.etree.ElementTree as et
import numpy as np
from copy import deepcopy
from typing import Union

import rwmap._util as utility
import rwmap._frame as frame
from rwmap._frame._element_ori import ElementOri
from rwmap._frame._element_property import ElementProperties


class Layer(ElementOri):
    def __init__(self, properties:ElementProperties, tilematrix:np.ndarray, encoding:str, compression:Union[str, None])->None:
        super().__init__(properties)
        self._tilematrix = deepcopy(tilematrix)
        self._encoding = deepcopy(encoding)
        self._compression = deepcopy(compression)
    @classmethod
    def init_etElement(cls, root:et.Element)->None:
        properties = ElementProperties.init_etElement(root)
        data = utility.get_etElement_callable_from_tag_s(root, "data")
        _tilematrix = utility.get_etElement_ndarray_from_text_packed(data, frame.Coordinate(root.attrib['width'], root.attrib['height']))
        return cls(properties, _tilematrix, data.attrib["encoding"], data.attrib.get("compression"))
    
    @classmethod
    def init_Layer(cls, property:frame.TagCoordinate, compression:str = "zlib")->None:
        properties = ElementProperties("layer", {"name": property.tag(), "width": str(property.x()), "height": str(property.y())})
        return cls(properties, np.zeros((property.y(), property.x()), dtype = np.uint32), "base64", compression)

    def output_str(self, output_rectangle:frame.Rectangle = frame.Rectangle(frame.Coordinate(), frame.Coordinate(-1, -1)))->str:
        str_ans = ""
        str_ans = str_ans + self._properties.output_str() + "\n"
        str_ans = str_ans + "".join([" ".join([str(self._tilematrix[i][j]) for j in range(max(output_rectangle.i().y(), 0), min(output_rectangle.e().y(), self._tilematrix.shape[1]))]) + "\n"
                                 for i in range(max(output_rectangle.i().x(), 0), min(output_rectangle.e().x(), self._tilematrix.shape[0]))]) + "\n"
        str_ans = utility.indentstr_Tab(str_ans)
        return str_ans

    def output_etElement(self)->et.Element:
        root = et.Element("layer")
        root = self._properties.output_etElement(root)
        root.append(utility.get_etElement_from_text_packed(self._tilematrix, self._encoding, self._compression))
        return root
    
    def name(self)->str:
        return self._properties.returnDefaultProperty("name")
    
    def size(self)->frame.Coordinate:
        return frame.Coordinate(int(self._properties.returnDefaultProperty("height")), 
                                int(self._properties.returnDefaultProperty("width")))

    def __repr__(self)->str:
        return self.output_str()

    def id(self)->int:
        return int(self._properties.returnDefaultProperty("id"))
    
    def changeid(self, id:int)->None:
        self._properties.assignDefaultProperty("id", id)

    def opacity(self)->float:
        return float(self._properties.returnDefaultProperty("opacity"))
    
    def change_opacity(self, num:float)->None:
        self._properties.assignDefaultProperty("opacity", f"{num:.2f}")

    def tileid(self, place_grid:frame.Coordinate)->int:
        return int(self._tilematrix[place_grid.x()][place_grid.y()])
    
    def assigntileid(self, place_grid:frame.Coordinate, tileid:int):
        size = self.size()
        if place_grid.x() < 0 or place_grid.y() < 0 or place_grid.x() >= size.x() or place_grid.y() >= size.y():
            return
        self._tilematrix[place_grid.x()][place_grid.y()] = tileid

    def assigntileid_square(self, square_grid:frame.Rectangle, tileid:int):
        size = self.size()
        self._tilematrix[max(0, square_grid.i().x()):min(size.x(), square_grid.e().x()), 
        max(0, square_grid.i().y()):min(size.y(), square_grid.e().y())]\
        = tileid

    def assigntileid_squarematrix_exclude0(self, pos:frame.Coordinate, tileid_matrix:np.ndarray, tilerec:frame.Rectangle = None):
        utility.save_matrix_exclude0(self._tilematrix, pos, tileid_matrix, tilerec)

    def assigntileid_squarematrix(self, pos:frame.Coordinate, tileid_matrix:np.ndarray, tilerec:frame.Coordinate = None):
        utility.save_matrix(self._tilematrix, pos, tileid_matrix, tilerec)
        

    
    
    
        
