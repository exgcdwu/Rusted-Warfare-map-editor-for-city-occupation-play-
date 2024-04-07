# -*- coding: utf-8 -*-
"""

"""
import xml.etree.ElementTree as et

import rwmap._exceptions as rwexceptions
import rwmap._default_data as rwdata
import rwmap._util as utility
import rwmap._case as case
import rwmap._frame as frame


class RWmap(frame.ElementOri):
    def __init__(self, properties:frame.ElementProperties, tileset_list:list[case.TileSet],
                  layer_list:list[case.Layer], objectGroup_list:list[case.ObjectGroup])->None:
        super().__init__(properties)
        self._tileset_list = tileset_list
        self._layer_list = layer_list
        self._objectGroup_list = objectGroup_list
    @classmethod
    def init_graphfile(cls, map_file:str, rwmaps_dir:str)->None:
        xmlTree:et.ElementTree = et.ElementTree(file=map_file)
        root:et.Element = xmlTree.getroot()
        properties = frame.ElementProperties.init_etElement(root)

        tileset_list = [case.TileSet.init_etElement(tileset, rwmaps_dir) for tileset in root if tileset.tag == "tileset"]
        layer_list = [case.Layer.init_etElement(layer) for layer in root if layer.tag == "layer"]
        objectGroup_list = [case.ObjectGroup.init_etElement(objectGroup) for objectGroup in root if objectGroup.tag == "objectgroup"]  
        
        tileset_list = None if tileset_list == [] else tileset_list
        layer_list = None if layer_list == [] else layer_list
        objectGroup_list = None if objectGroup_list == [] else objectGroup_list
        
        return cls(properties, tileset_list, layer_list, objectGroup_list)

    def output_str(self, pngtextnum:int = -1, tilenum:int = -1, output_rectangle:frame.Rectangle = frame.Rectangle(frame.Coordinate(), frame.Coordinate(-1, -1)), objectnum:int = -1)->str:
        str_ans = ""
        str_ans = str_ans + self._properties.output_str() + "\n"
        str_ans = str_ans + "\n".join([tileset.output_str(pngtextnum, tilenum) for tileset in self._tileset_list]) + "\n"
        str_ans = str_ans + "\n".join([layer.output_str(output_rectangle) for layer in self._layer_list]) + "\n"
        str_ans = str_ans + "\n".join([tobject.output_str(objectnum) for tobject in self._objectGroup_list]) + "\n"
        str_ans = utility.indentstr_Tab(str_ans)
        return str_ans

    def output_etElement(self)->et.Element:
        root = et.Element("map")
        self._properties.output_etElement(root)
        if self._tileset_list != None:
            for tileset in self._tileset_list:
                root.append(tileset.output_etElement())
        if self._layer_list != None:
            for layer in self._layer_list:
                root.append(layer.output_etElement())
        if self._objectGroup_list != None:
            for objectGroup in self._objectGroup_list:
                root.append(objectGroup.output_etElement())
        return root
    
    def write_file(self, map_file:str)->None:
        utility.output_file_from_etElement(self.output_etElement(), map_file)

    def addObject(self, objectGroup_name:str, default_properties:dict[str, str], optional_properties :dict[str, str])->None:
        objectGroup_now:case.ObjectGroup = utility.get_ElementOri_from_list_by_name(self._objectGroup_list, objectGroup_name)
        if objectGroup_now == None:
            raise KeyError("objectGroup name:" + objectGroup_name + " not found")
        objectGroup_now.addObject(default_properties, optional_properties)
        str_nextobjectid = str(max(int(self._properties.returnDefaultProperty("nextobjectid")), int(default_properties["id"]) + 1))
        self._properties.assignDefaultProperty("nextobjectid", str_nextobjectid)
    
    def changeObject_defaultProperty(self, objectGroup_name:str, ID:int, name:str, value:str):
        objectGroup_now:case.ObjectGroup = utility.get_ElementOri_from_list_by_name(self._objectGroup_list, objectGroup_name)
        if objectGroup_now == None:
            raise KeyError("objectGroup name:" + objectGroup_name + " not found")
        for tobject in objectGroup_now._object_list:
            if tobject.returnDefaultProperty("id") == str(ID):
                tobject.assignDefaultProperty(name, value)

    def changeObject_optionalProperty(self, objectGroup_name:str, ID:int, name:str, value:str):
        objectGroup_now:case.ObjectGroup = utility.get_ElementOri_from_list_by_name(self._objectGroup_list, objectGroup_name)
        if objectGroup_now == None:
            raise KeyError("objectGroup name:" + objectGroup_name + " not found")
        for tobject in objectGroup_now._object_list:
            if tobject.returnDefaultProperty("id") == str(ID):
                tobject.assignOptionalProperty(name, value)

    def addTile(self, layer_name:str, place_grid:frame.Coordinate, tileset_name:str, tile_grid:frame.Coordinate)->None:
        layer:case.Layer = utility.get_ElementOri_from_list_by_name(self._layer_list, layer_name)
        tileset_name = tileset_name.strip()
        if layer == None:
            raise KeyError("layer name:" + layer_name + " not found")
        for tileset_now in self._tileset_list:
            if tileset_now.output_name() == tileset_name:
                tileset = tileset_now
        try:
            layer.assigntileid(place_grid, tileset.tileid(tile_grid))
        except UnboundLocalError:
            raise KeyError("tileset name:" + tileset_name + " not found")
        
    def addTile_square(self, layer_name:str, place_rectangle:frame.Rectangle, tileset_name:str, tile_grid:frame.Coordinate)->None:
        for place_grid in place_rectangle.iterator():
            self.addTile(layer_name, place_grid, tileset_name, tile_grid)

        


        
        


