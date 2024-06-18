# -*- coding: utf-8 -*-
"""

"""
import xml.etree.ElementTree as et
import re
import os
from copy import deepcopy
from typing import Generator, Union
from numbers import Integral
import numpy as np

import rwmap._exceptions as rwexceptions
import rwmap._util as utility
import rwmap._case as case
import rwmap._frame as frame
from rwmap._frame._element_ori import ElementOri
from rwmap._frame._element_property import ElementProperties
import rwmap._tile as tile
import rwmap._object as object
import rwmap._otgroup as otgroup
import rwmap._data.const as const


RWMAP_DIR = os.path.dirname(__file__)
RWMAP_MAPS = RWMAP_DIR + "/other_data/maps/"

class RWmap(ElementOri):
    pass

class RWmap(ElementOri):
    def __init__(self, properties:ElementProperties, tileset_list:list[case.TileSet],
                  layer_list:list[case.Layer], objectGroup_list:list[case.ObjectGroup])->None:
        super().__init__(properties)
        self._tileset_list = deepcopy(tileset_list)
        self._layer_list = deepcopy(layer_list)
        self._objectGroup_list = deepcopy(objectGroup_list)
    @classmethod
    def init_mapfile(cls, map_file:str, rwmaps_dir = RWMAP_MAPS):
        xmlTree:et.ElementTree = et.ElementTree(file=map_file)
        root:et.Element = xmlTree.getroot()
        properties = ElementProperties.init_etElement(root)

        tileset_list = [case.TileSet(ElementProperties("tileset", {"firstgid": const.KEY.empty_tile, "name": "empty"}), frame.Coordinate(1, 1))]
        tileset_list = tileset_list + [case.TileSet.init_etElement(tileset, rwmaps_dir) for tileset in root if tileset.tag == "tileset"]
        layer_list = [case.Layer.init_etElement(layer) for layer in root if layer.tag == "layer"]
        objectGroup_list = [case.ObjectGroup.init_etElement(objectGroup) for objectGroup in root if objectGroup.tag == "objectgroup"]  
        
        return cls(properties, tileset_list, layer_list, objectGroup_list)

    @classmethod
    def init_map(cls, size:frame.Coordinate, tile_size:frame.Coordinate = const.COO.SIZE_STANDARD):
        properties = ElementProperties("map", \
                                       {
                                           "version": "1.10", 
                                           "tiledversion": "1.10.2", 
                                           "orientation": "orthogonal", 
                                           "renderorder": "right-down", 
                                           "width": str(size.x()), 
                                           "height": str(size.y()), 
                                           "tilewidth": str(tile_size.x()), 
                                           "tileheight": str(tile_size.y()), 
                                           "infinite": "0"
                                       })
        properties.assignDefaultProperty("nextlayerid", "1")
        properties.assignDefaultProperty("nextobjectid", "1")
        tileset_list = [case.TileSet(ElementProperties("tileset", {"firstgid": const.KEY.empty_tile, "name": "empty"}), frame.Coordinate(1, 1))]
        layer_list = []
        objectGroup_list = []
        return cls(properties, tileset_list, layer_list, objectGroup_list)

    def size(self)->frame.Coordinate:
        return frame.Coordinate(int(self._properties.returnDefaultProperty("width")), 
                                int(self._properties.returnDefaultProperty("height")))
    
    def tile_size(self)->frame.Coordinate:
        return frame.Coordinate(int(self._properties.returnDefaultProperty("tilewidth")), 
                                int(self._properties.returnDefaultProperty("tileheight")))
    
    def end_point_layer(self)->frame.Coordinate:
        return frame.Coordinate(int(self._properties.returnDefaultProperty("height")), 
                                int(self._properties.returnDefaultProperty("width")))
    
    def end_point_object(self)->frame.Coordinate:
        return self.size() * self.tile_size()
    
    def nextlayerid(self)->int:
        return int(self._properties.returnDefaultProperty("nextlayerid"))
    
    def changenextlayerid(self, layerid:int)->None:
        self._properties.assignDefaultProperty("nextlayerid", str(layerid))

    def nextobjectid(self)->int:
        return int(self._properties.returnDefaultProperty("nextobjectid"))
    
    def changenextobjectid(self, layerid:int)->None:
        self._properties.assignDefaultProperty("nextobjectid", str(layerid))

    def resetnextobjectid(self, isaboutnextobjectid = True)->None:
        maxid_now = self.nextobjectid() if isaboutnextobjectid else 1
        for objectGroup in self._objectGroup_list:
            maxid_now = max(maxid_now, objectGroup.max_id() + 1)
        self.changenextobjectid(maxid_now)

    def tileset_name_list(self)->list[str]:
        return [tileset.name() for tileset in self._tileset_list if tileset.isexist()]
    
    def layer_name_list(self)->list[str]:
        return [layer.name() for layer in self._layer_list]
    
    def objectgroup_name_list(self)->list[str]:
        return [objectgroup.name() for objectgroup in self._objectGroup_list]

    def get_layer_s(self, name:str)->case.Layer:
        layer = utility.get_ElementOri_from_list_by_name_s(self._layer_list, name)
        if layer == None:
            raise KeyError("layer name:" + name + " not found")
        return layer
        
    def get_tileset_s(self, name:str)->case.TileSet:
        tileset = utility.get_ElementOri_from_list_by_name_s(self._tileset_list, name)
        if tileset == None:
            raise KeyError("tileset name:" + name + " not found")
        return tileset
        
    def get_objectgroup_s(self, name:str)->case.ObjectGroup:
        objectgroup = utility.get_ElementOri_from_list_by_name_s(self._objectGroup_list, name)
        if objectgroup == None:
            raise KeyError("objectgroup name:" + name + " not found")
        return objectgroup
    
    def add_tileset_fromTileSet(self, tileset:case.TileSet)->None:
        tileset_n = deepcopy(tileset)
        firstgid = self._tileset_list[-1].endgid()
        tileset_n.changefirstgid(firstgid)
        self._tileset_list.append(tileset_n)

    def add_tileset_fromMap(self, rwmap:RWmap)->None:
        for tileset in rwmap._tileset_list:
            if tileset.isexist():
                self.add_tileset_fromTileSet(tileset)

    def add_tileset_fromMapPath(self, map_path:str)->None:
        rwmap = RWmap.init_mapfile(map_path)
        self.add_tileset_fromMap(rwmap)

    def add_layer(self, layername:str, compression:str = "default")->None:
        if compression == "default":
            if self._layer_list == []:
                compression = "zlib"
            else:
                compression = self._layer_list[0]._compression
        layer = case.Layer.init_Layer(frame.TagCoordinate(layername, self.size()), compression = compression)
        self._layer_list.append(layer)

    def add_Layer_fromLayer(self, layer:case.Layer)->None:
        layer_n = deepcopy(layer)
        layerid = self.nextlayerid()
        self.changenextlayerid(layerid)
        layer_n.changeid(layerid)
        self._layer_list.append(layer_n)

    def add_objectgroup(self, objectgroupname:str)->None:
        objectgroup = case.ObjectGroup.init_ObjectGroup(objectgroupname)
        self._objectGroup_list.append(objectgroup)

    def add_objectgroup_fromObjectGroup(self, objectgroup:case.ObjectGroup)->None:
        objectgroup_n = deepcopy(objectgroup)
        layerid = int(self._properties.returnDefaultProperty("nextlayerid"))
        self._properties.assignDefaultProperty("nextlayerid", str(layerid + 1))
        objectgroup_n.changeid(layerid)
        self._objectGroup_list.append(objectgroup_n)

    def write_png(self, dir:str)->None:
        for tileset in self._tileset_list:
            tileset.write_png(dir)

    def output_str(self, pngtextnum:int = -1, tilenum:int = -1, output_rectangle:frame.Rectangle = frame.Rectangle(frame.Coordinate(), frame.Coordinate(-1, -1)), objectnum:int = -1)->str:
        str_ans = ""
        str_ans = str_ans + self._properties.output_str() + "\n"
        str_ans = str_ans + "\n".join([tileset.output_str(pngtextnum, tilenum) for tileset in self._tileset_list if tileset.isexist()]) + "\n"
        str_ans = str_ans + "\n".join([layer.output_str(output_rectangle) for layer in self._layer_list]) + "\n"
        str_ans = str_ans + "\n".join([tobject.output_str(objectnum) for tobject in self._objectGroup_list]) + "\n"
        str_ans = utility.indentstr_Tab(str_ans)
        return str_ans

    def __repr__(self)->str:
        return self.output_str()

    def output_etElement(self)->et.Element:
        root = et.Element("map")
        root = self._properties.output_etElement(root)
        if self._tileset_list != None:
            for tileset in self._tileset_list:
                if tileset.isexist():
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


    def addObject_type(self, tobject:case.TObject, objectGroup_name:str = const.NAME.Triggers, isresetid = True):
        objectGroup_now = self.get_objectgroup_s(objectGroup_name)
        if isresetid:
            tobject.assignDefaultProperty("id", self._properties.returnDefaultProperty("nextobjectid"))
            str_nextobjectid = str(max(int(self._properties.returnDefaultProperty("nextobjectid")), int(tobject.returnDefaultProperty("id")) + 1))
            self._properties.assignDefaultProperty("nextobjectid", str_nextobjectid)
        objectGroup_now.addObject_type(tobject)
        

    def addObject_dict(self, objectGroup_name:str = const.NAME.Triggers, default_properties:dict[str, str] = {}, optional_properties :dict[str, Union[str, dict[str, str]]] = {}, other_properties:list[et.Element] = [])->None:
        objectGroup_now = self.get_objectgroup_s(objectGroup_name)
        default_properties_n = deepcopy(default_properties)
        if default_properties_n.get("id") == None:
            default_properties_n["id"] = self._properties.returnDefaultProperty("nextobjectid")
        objectGroup_now.addObject_dict(default_properties_n, optional_properties, other_properties)
        str_nextobjectid = str(max(int(self._properties.returnDefaultProperty("nextobjectid")), int(default_properties_n["id"]) + 1))
        self._properties.assignDefaultProperty("nextobjectid", str_nextobjectid)
    
    def addObject_one(self, tobject_one:object.TObject_One, offset:frame.Coordinate = frame.Coordinate()):
        ntobject = tobject_one.offset(offset)
        self.addObject_dict("Triggers", ntobject.default_properties(), ntobject.optional_properties(), ntobject.other_properties())

    def addObject_group(self, tobject_group:object.TObject_Group, offset:frame.Coordinate = frame.Coordinate()):
        for tobject in tobject_group._TObject_One_list:
            self.addObject_one(tobject, offset)
        for tobject_group in tobject_group._TObject_Group_list:
            self.addObject_group(tobject_group, offset)

    def addObject(self, tobject:Union[object.TObject_One, object.TObject_Group], offset:frame.Coordinate = frame.Coordinate()):
        if isinstance(tobject, object.TObject_One):
            self.addObject_one(tobject, offset)
        elif isinstance(tobject, object.TObject_Group):
            self.addObject_group(tobject, offset)
        else:
            raise TypeError("The type of RWmap.addObject(tobject, ...) is wrong.")

    def iterator_object_s(self, objectGroup_name:str = const.NAME.Triggers, default_re:dict[str, str] = {}, optional_re:dict[str, str] = {})->Generator[case.TObject, None, None]:
        objectGroup_now = self.get_objectgroup_s(objectGroup_name)
        for tobject in objectGroup_now._object_list:
            tobject_sas:bool = True
            for dname, dvalue in default_re.items():
                tname = tobject.returnDefaultProperty(dname) if tobject.returnDefaultProperty(dname) != None else ""
                if re.match(dvalue, tname) == None:
                    tobject_sas = False
                    break
            if tobject_sas == False:
                continue
            for dname, dvalue in optional_re.items():
                tname = tobject.returnOptionalProperty(dname) if tobject.returnOptionalProperty(dname) != None else ""
                if re.match(dvalue, tname) == None:
                    tobject_sas = False
                    break
            if tobject_sas == False:
                continue
            yield tobject
    
    def delete_object_s(self, tobject:case.TObject, objectGroup_name:str = const.NAME.Triggers):
        objectGroup_now = self.get_objectgroup_s(objectGroup_name)
        objectGroup_now.deleteObject(tobject)

    def index_object_s(self, tobject:case.TObject, objectGroup_name:str = const.NAME.Triggers)->int:
        objectGroup_now = self.get_objectgroup_s(objectGroup_name)
        return objectGroup_now.index_object_s(tobject)

    def _tileplace_to_gid(self, tileplace:Union[int, tuple[str, int], frame.TagCoordinate])->int:
        if isinstance(tileplace, int):
            tileplace_now = tileplace
        elif isinstance(tileplace, tuple) and isinstance(tileplace[0], str) and isinstance(tileplace[1], int):
            tileplace_now = self.get_tileset_s(tileplace[0]).tileid_to_gid(tileplace[1])
        elif isinstance(tileplace, frame.TagCoordinate):
            if tileplace.tag()[-1] == const.KEY.tag_for_tile_notre:
                tileset = self.get_tileset_s(tileplace.tag()[:-1])
                isre = False
            else:
                tileset = self.get_tileset_s(tileplace.tag())
                isre = True
            tileplace_now = tileset.coo_to_gid(tileplace.place(), isre = isre)
        else:
            raise TypeError("The type of RWmap.addTile(..., tileplace) is wrong.")
        return tileplace_now

    def addTile_gid(self, layerplace:frame.TagCoordinate, gid:int):
        if gid >= 0 and isinstance(gid, Integral):
            layer:case.Layer = self.get_layer_s(layerplace.tag())
        else:
            raise TypeError("gid is less than 0 or not integer.")
        layer.assigntileid(layerplace.place(), gid)

    def addTile(self, layerplace:frame.TagCoordinate, tileplace:Union[int, tuple[str, int], frame.TagCoordinate]):
        tileplace_now = self._tileplace_to_gid(tileplace)
        self.addTile_gid(layerplace, tileplace_now)

    def addTile_square(self, layerRectangle:frame.TagRectangle, tileplace:Union[int, tuple[str, int], frame.TagCoordinate])->None:
        tileplace_now = self._tileplace_to_gid(tileplace)
        layer:case.Layer = self.get_layer_s(layerRectangle.tag())
        layer.assigntileid_square(layerRectangle.rectangle(), tileplace_now)

    def addTile_group(self, tilegroup:tile.TileGroup_One, original_grid:frame.Coordinate, rect_execute:frame.Rectangle = None, isacce = False):
        if rect_execute == None:
            range_excute = frame.Rectangle(frame.Coordinate(0, 0), tilegroup.size())
        else:
            range_excute = rect_execute
        
        selfid = str(id(self))

        gidmatrix = tilegroup.get_acce_s(selfid)
        if type(gidmatrix) != np.ndarray:
            gidmatrix = np.ndarray([tilegroup.size().x(), tilegroup.size().y()], dtype = np.uint32)
            for place_grid in tilegroup.size():
                gidmatrix[place_grid.x(), place_grid.y()] = self._tileplace_to_gid(tilegroup[place_grid])
        
        layer_s = self.get_layer_s(tilegroup.layername())
        
        layer_s.assigntileid_squarematrix_exclude0(original_grid, gidmatrix, range_excute)
        if isacce:
            if type(tilegroup.get_acce_s(selfid)) != np.ndarray:
                tilegroup.save_acce_s(selfid, gidmatrix)

    def addTile_group_list(self, tilegroup_list:tile.TileGroup_List, original_grid:frame.Coordinate, rect_execute:frame.Rectangle = None):
        for tilegroup in tilegroup_list:
            self.addTile_group(tilegroup, original_grid, rect_execute)

    def addOTGroup(self, otgroup:otgroup.OTGroup, offset_grid:frame.Coordinate = frame.Coordinate()):
        self.addTile_group_list(otgroup._tilegroup_list, offset_grid)
        self.addObject_group(otgroup._tobject_group, offset_grid * self.tile_size())
        


        
        


