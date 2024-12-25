# -*- coding: utf-8 -*-
"""

"""
import xml.etree.ElementTree as et
import numpy as np
from copy import deepcopy
from typing import Union
import os

import rwmap._util as utility
import rwmap._frame as frame
import rwmap._data.const as const
from rwmap._frame._element_ori import ElementOri
from rwmap._frame._element_property import ElementProperties

class ImageLayer(ElementOri):
    def __init__(self, map_path:str, properties:ElementProperties, image_properties:ElementProperties)->None:
        super().__init__(const.TAG.imagelayer, properties)
        self._properties = deepcopy(properties)
        self._image_properties = deepcopy(image_properties)
        self._map_path = deepcopy(map_path)
        self._size = self.size()
    @classmethod
    def init_etElement(cls, root:et.Element, map_path:str)->None:
        properties = ElementProperties.init_etElement(root)
        image_root = utility.get_etElement_callable_from_tag_s(root, "image")
        image_properties = ElementProperties.init_etElement(image_root)
        return cls(map_path, properties, image_properties)
    
    @classmethod
    def init_imageLayer(cls, property:frame.TagCoordinate, id:int, map_path:str)->None:
        properties = ElementProperties("imagelayer", {"id": str(id), "name": os.path.basename(property.tag())})
        image_properties = ElementProperties("image", {"source": property.tag(), "width": str(property.y()), "height": str(property.x())})
        return cls(map_path, properties, image_properties)

    def output_str(self)->str:
        str_ans = ""
        str_ans = str_ans + self._properties.output_str() + "\n"
        str_ans = str_ans + utility.indentstr_Tab(self._image_properties.output_str()) + "\n"
        str_ans = utility.indentstr_Tab(str_ans)
        return str_ans

    def output_etElement(self)->et.Element:
        root = et.Element("imagelayer")
        root = self._properties.output_etElement(root)
        image_root = et.Element("image")
        image_root = self._image_properties.output_etElement(image_root)
        root.append(image_root)
        return root
    
    def name(self)->str:
        return self._properties.returnDefaultProperty("name")
    
    def source(self)->str:
        return self._image_properties.returnDefaultProperty("source")
    
    def size(self)->frame.Coordinate:
        return frame.Coordinate(int(self._image_properties.returnDefaultProperty("height")), 
                                int(self._image_properties.returnDefaultProperty("width")))

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

    def source_path(self)->str:
        return utility.find_file(os.path.dirname(self._map_path), self.source())

    def imageTile(self, place_grid:frame.Coordinate, tile_size:frame.Coordinate)->np.ndarray:
        return utility.image_division_coo(self.source_path(), tile_size, place_grid)