# -*- coding: utf-8 -*-
"""

"""

import xml.etree.ElementTree as et

import rwgraph._exceptions as rwexceptions
import rwgraph._default_data as rwdata
import rwgraph._util as utility
import rwgraph._case as case


class RWGraph:
    def __init__(self, map_properties:utility.ElementProperties, tileset_list:list[case.TileSet],
                  layer_list:list[case.Layer], objectGroup_list:list[case.ObjectGroup])->None:
        self._map_properties = map_properties
        self._tileset_list = tileset_list
        self._layer_list = layer_list
        self._objectGroup_list = objectGroup_list
    @classmethod
    def init_graphfile(cls, graph_file:str)->None:
        xmlTree:et.ElementTree = et.ElementTree(file=graph_file)
        root:et.Element = xmlTree.getroot()
        map_properties = utility.ElementProperties.init_etElement(root)

        tileset_list = [case.TileSet.init_etElement(tileset) for tileset in root if tileset.tag == "tileset"]
        layer_list = [case.Layer.init_etElement(layer) for layer in root if layer.tag == "layer"]
        objectGroup_list = [case.ObjectGroup.init_etElement(objectGroup) for objectGroup in root if objectGroup.tag == "objectgroup"]  
        
        tileset_list = None if tileset_list == [] else tileset_list
        layer_list = None if layer_list == [] else layer_list
        objectGroup_list = None if objectGroup_list == [] else objectGroup_list
        
        return cls(map_properties, tileset_list, layer_list, objectGroup_list)
    
    def output_str(self, pngtextnum:int = -1, tilenum:int = -1, output_rectangle:utility.Rectangle = utility.Rectangle(utility.Coordinate(), utility.Coordinate(-1, -1)), objectnum:int = -1)->str:
        str_ans = ""
        str_ans = str_ans + self._map_properties.output_str() + "\n"
        str_ans = str_ans + "\n".join([tileset.output_str(pngtextnum, tilenum) for tileset in self._tileset_list]) + "\n"
        str_ans = str_ans + "\n".join([layer.output_str(output_rectangle) for layer in self._layer_list]) + "\n"
        str_ans = str_ans + "\n".join([tobject.output_str(objectnum) for tobject in self._objectGroup_list]) + "\n"
        str_ans = utility.indentstr_Tab(str_ans)
        return str_ans
        

