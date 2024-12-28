# -*- coding: utf-8 -*-
"""

"""
import xml.etree.ElementTree as et
import re
import os
from copy import deepcopy
from typing import Generator, Union, Callable
from numbers import Integral
import numpy as np
import sys
import math
from PIL import Image
import networkx as nx
from sortedcontainers import SortedDict

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

def exenparr_deal_expand(rwnparr:np.ndarray, exe_to_exe:dict[int, list[list[int]]] = {}):
    exe_to_exe_nparr = {e:np.ndarray(v) for e, v in exe_to_exe.items()}
    exe_set = set(exe_to_exe_nparr.keys())
    exe_dict = SortedDict({i:[] for i in exe_set})
    exe_to_exe_dict = SortedDict(exe_to_exe_nparr)
    exe_num = 0
    min_exe = sorted(exe_dict.keys())
    for i in range(rwnparr.shape[0]):
        for j in range(rwnparr.shape[1]):
            if exe_dict.get(rwnparr[i, j]) == None:
                continue
            else:
                exe_dict[rwnparr[i, j]].append((i, j))
                exe_num = exe_num + 1

    men = 0
    while exe_num > 0:
        ml = exe_dict.get(min_exe[men])
        nl = ml[-1]
        fm = exe_to_exe_dict.get(min_exe)
        for i in range(-1, 2):
            for j in range(-1, 2):
                if rwnparr[nl[0] + i, nl[1] + j] == 0 and fm[i + 1, j + 1] != -1:
                    rwnparr[nl[0] + i, nl[1] + j] = fm[i + 1, j + 1]
                    el = exe_dict.get(fm[i, j])
                    if el != None:
                        el.append((nl[0] + i, nl[1] + j))
                        exe_num = exe_num + 1
        ml.pop(-1)
        exe_num = exe_num - 1

        if len(ml) == 0:
            men = men + 1

def exenparr_deal_shrink_one(exe_tree:nx.DiGraph, rwnparr:np.ndarray, i:int, j:int, sx:int, sy:int)->int:
    pid = 0
    while True:
        plfd = exe_tree[pid].get('lfd')
        if plfd != None:
            return plfd
        for ee in exe_tree.edges(pid):
            plx = i + exe_tree[ee]['pla'][0]
            ply = j + exe_tree[ee]['pla'][1]
            if plx >= 0 or plx < sx or ply >= 0 or ply < sy:
                return rwnparr[i, j]
            if rwnparr[plx, ply] == exe_tree[ee]['exe']:
                pid = ee
                break
        

def exenparr_deal_shrink(rwnparr:np.ndarray, exe_to_exe:dict[int, list[list[int]]] = {}):
    
    exe_tree = nx.DiGraph()
    p_ind = 0
    exe_tree.add_node(p_ind, exe = -1)
    p_ind = p_ind + 1
    for k, vll in exe_to_exe.items():
        node_now = 0
        vllt = deepcopy(vll)
        ke = vllt[1][1]
        vllt[1][1] = k
        for i, vl in enumerate(vllt):
            for j, v in enumerate(vl):
                if v == -1:
                    continue
                else:
                    ised = False
                    for edge in exe_tree.edges(node_now):
                        if exe_tree[edge[1]]['exe'] == v and exe_tree[edge[1]]['pla'] == (i, j):
                            node_now = edge[1]
                            ised = True
                            break
                    if ised:
                        continue
                    
                    exe_tree.add_node(p_ind, pla = (i, j), exe = v)

                    exe_tree.add_edge(node_now, p_ind)
                    node_now = p_ind
                    p_ind = p_ind + 1
        exe_tree[node_now]['lfd'] = ke

    rwnparr_new = deepcopy(rwnparr)
    for i in range(rwnparr.shape[0]):
        for j in range(rwnparr.shape[1]):
            rwnparr_new[i, j] = exenparr_deal_shrink_one(exe_tree, rwnparr, i, j, rwnparr.shape[0], rwnparr.shape[1])
    return rwnparr_new

class RWmap(ElementOri):
    pass

class RWmap(ElementOri):
    def __init__(self, properties:ElementProperties, tileset_list:list[case.TileSet],
                  layer_list:list[case.Layer], objectGroup_list:list[case.ObjectGroup], 
                  imageLayer_list:list[case.ImageLayer], oli_order_list:list[int], other_elements:list[et.Element] = [])->None:
        super().__init__(const.TAG.map, properties)
        self._tileset_list = deepcopy(tileset_list)
        self._layer_list = deepcopy(layer_list)
        self._objectGroup_list = deepcopy(objectGroup_list)
        self._imageLayer_list = deepcopy(imageLayer_list)
        self._oli_order_list = deepcopy(oli_order_list)
        self._other_elements = deepcopy(other_elements)
        self._tileset_now = None
        self._layer_now = None
        self._imageLayer_now = None
        self._objectgroup_now = None
    @classmethod
    def init_mapfile(cls, map_file:str, rwmaps_dir = RWMAP_MAPS):
        xmlTree:et.ElementTree = et.ElementTree(file=map_file)
        root:et.Element = xmlTree.getroot()
        properties = ElementProperties.init_etElement(root)


        tileset_list = [case.TileSet(ElementProperties("tileset", {"firstgid": const.KEY.empty_tile, "name": "empty"}), frame.Coordinate(1, 1), frame.Coordinate(), None)]
        tileset_list = tileset_list + [case.TileSet.init_etElement(map_file, tileset, rwmaps_dir) for tileset in root if tileset.tag == "tileset"]
        layer_list = [case.Layer.init_etElement(layer) for layer in root if layer.tag == "layer"]
        objectGroup_list = [case.ObjectGroup.init_etElement(objectGroup) for objectGroup in root if objectGroup.tag == "objectgroup"]  
        imageLayer_list = [case.ImageLayer.init_etElement(imageLayer, map_file) for imageLayer in root if imageLayer.tag == "imagelayer"]  
        oli_order_list = [const.OLI_TAG_DICT[td.tag] for td in root if td.tag in const.OLI_TAG_SET]

        other_elements = [other_element for other_element in root if not other_element.tag in const.KNOWN_MAP_TAG_SET]  

        return cls(properties, tileset_list, layer_list, objectGroup_list, imageLayer_list, oli_order_list, other_elements)

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
        tileset_list = [case.TileSet(ElementProperties("tileset", {"firstgid": const.KEY.empty_tile, "name": "empty"}), frame.Coordinate(1, 1), tile_size, None)]
        layer_list = []
        objectGroup_list = []
        imageLayer_list = []
        oli_order_list = []
        return cls(properties, tileset_list, layer_list, imageLayer_list, objectGroup_list, oli_order_list)

    def size(self)->frame.Coordinate:
        return frame.Coordinate(int(self._properties.returnDefaultProperty("width")), 
                                int(self._properties.returnDefaultProperty("height")))

    def size_t(self)->frame.Coordinate:
        return self.size().transpose()
    
    def size_o(self)->frame.Coordinate:
        return self.size()

    def tilecount(self)->int:
        return self.size().mul()

    def tile_size(self)->frame.Coordinate:
        return frame.Coordinate(int(self._properties.returnDefaultProperty("tilewidth")), 
                                int(self._properties.returnDefaultProperty("tileheight")))
    
    def tile_size_t(self)->frame.Coordinate:
        return self.tile_size().transpose()
    
    def tile_size_o(self)->frame.Coordinate:
        return self.tile_size()

    def end_point_layer(self)->frame.Coordinate:
        return frame.Coordinate(int(self._properties.returnDefaultProperty("height")), 
                                int(self._properties.returnDefaultProperty("width")))
    
    def end_point_object(self)->frame.Coordinate:
        return self.size() * self.tile_size()
    
    def nextlayerid(self)->int:
        return int(self._properties.returnDefaultProperty("nextlayerid"))

    def changenextlayerid(self, layerid:int)->None:
        self._properties.assignDefaultProperty("nextlayerid", str(layerid))

    def nextlayerid_pp(self)->None:
        self.changenextlayerid(self.nextlayerid() + 1)

    def nextobjectid(self)->int:
        return int(self._properties.returnDefaultProperty("nextobjectid"))
    
    def changenextobjectid(self, layerid:int)->None:
        self._properties.assignDefaultProperty("nextobjectid", str(layerid))

    def nextlayerid_pp(self)->None:
        self.changenextobjectid(self.nextobjectid() + 1)

    def resetlayer_terrain(self, layername:str, tilesetname:str)->None:
        layer_s = self.get_layer_s(layername)
        tileset_s = self.get_tileset_s(tilesetname)
        layer_s.reset_terraintileid(tileset_s.firstgid(), tileset_s.endgid())

    def resetnextobjectid(self, isaboutnextobjectid = True)->None:
        maxid_now = self.nextobjectid() if isaboutnextobjectid else 1
        for objectGroup in self._objectGroup_list:
            maxid_now = max(maxid_now, objectGroup.max_id() + 1)
        self.changenextobjectid(maxid_now)

    def resetid(self)->None:
        id_to_tobject = {}
        id_now = 1
        for objectGroup in self._objectGroup_list:
            for tobject in objectGroup._object_list:
                if id_to_tobject.get(tobject.returnDefaultProperty("id")) != None:
                    print("coincide ID|重合 ID:" + tobject.returnDefaultProperty("id"))
                id_to_tobject[tobject.returnDefaultProperty("id")] = tobject
                tobject.assignDefaultProperty("id", str(id_now))
                id_now = id_now + 1
        self.resetnextobjectid(isaboutnextobjectid = False)

    def tileset_name_list(self)->list[str]:
        return [tileset.name() for tileset in self._tileset_list if tileset.isexist()]
    
    def layer_name_list(self)->list[str]:
        return [layer.name() for layer in self._layer_list]
    
    def objectgroup_name_list(self)->list[str]:
        return [objectgroup.name() for objectgroup in self._objectGroup_list]

    def get_layer_s(self, name:str)->case.Layer:
        if self._layer_now != None and self._layer_now.name() == name:
            return self._layer_now
        layer = utility.get_ElementOri_from_list_by_name_s(self._layer_list, name)
        self._layer_now = layer
        return layer
    
    def layer_s_ahead(self, name:str, to_index:int = 0):
        layer_s = self.get_layer_s(name)
        self._layer_list.remove(layer_s)
        self._layer_list.insert(to_index, layer_s)
    
    def get_imageLayer_s(self, name:str)->case.ImageLayer:
        if self._imageLayer_now != None and self._imageLayer_now.name() == name:
            return self._imageLayer_now
        imageLayer = utility.get_ElementOri_from_list_by_name_s(self._imageLayer_list, name)
        self._imageLayer_now = imageLayer
        return imageLayer
    
    def get_ndarray_fromImageLayer(self, imagelayer_name:str, resize_coo:frame.Coordinate = None)->np.ndarray:
        image_path = self.get_imageLayer_s(imagelayer_name).source_path()
        if image_path == None:
            raise FileNotFoundError(f"Image source {self.get_imageLayer_s(imagelayer_name).source()} not found")
        image_now = utility.get_image(image_path)
        image_now = image_now.copy()
        if image_now.mode != 'RGB':
            image_now = image_now.convert('RGB')

        if resize_coo != None:
            resize_x = int(image_now.size[0] / resize_coo.x())
            resize_y = int(image_now.size[1] / resize_coo.y())
            image_now = image_now.resize((resize_x, resize_y), Image.Resampling.NEAREST)

        image_now = np.array(image_now)
        image_now = image_now.astype(np.uint8)
        image_now = image_now[:,:,:3]

        return image_now

    def imageLayer_s_ahead(self, name:str, to_index:int = 0):
        imagelayer_s = self.get_imageLayer_s(name)
        self._imageLayer_list.remove(imagelayer_s)
        self._imageLayer_list.insert(to_index, imagelayer_s)

    def get_tileset_fromgid_s(self, gid:int)->case.TileSet:
        for tileset in self._tileset_list:
            if tileset.exist_gid_to_tileid(gid):
                return tileset
        raise ValueError("gid is illegal.")

    def get_tileset_s(self, name:str)->case.TileSet:
        if self._tileset_now != None and self._tileset_now.name() == name:
            return self._tileset_now
        tileset = utility.get_ElementOri_from_list_by_name_s(self._tileset_list, name)
        self._tileset_now = tileset
        return tileset
    
    def tileset_s_ahead(self, name:str, to_index:int = 0):
        tileset_s = self.get_imageLayer_s(name)
        self._tileset_list.remove(tileset_s)
        self._tileset_list.insert(to_index, tileset_s)

    def get_objectgroup_s(self, name:str)->case.ObjectGroup:
        if self._objectgroup_now != None and self._objectgroup_now.name() == name:
            return self._objectgroup_now
        objectgroup = utility.get_ElementOri_from_list_by_name_s(self._objectGroup_list, name)
        self._objectgroup_now = objectgroup
        return objectgroup
    
    def get_objectgroup_s_ex(self, name:str)->case.ObjectGroup:
        objectgroup = self.get_objectgroup_s(name)
        if objectgroup == None:
            raise KeyError(f"get_objectgroup_s: {name} not found.")
        return objectgroup
    
    def objectGroup_s_ahead(self, name:str, to_index:int = 0):
        objectgroup_s = self.get_objectgroup_s(name)
        self._objectGroup_list.remove(objectgroup_s)
        self._objectGroup_list.insert(to_index, objectgroup_s)

    def add_tileset_purecolor(self, map_path:str, color_nparr:np.ndarray, tile_properties:list[list[str]], png_path:str, tsx_path:str, rwmaps_dir:str = RWMAP_MAPS, noise:list[int] = [0, 0, 0], randseed:int = -1)->None:
        tileset = case.TileSet.init_pure_color(rwmaps_dir, map_path, color_nparr, tile_properties, self.tile_size(), png_path, tsx_path, noise = noise, randseed = randseed)
        self.add_tileset_fromTileSet(tileset)

    def add_tileset_purecolor_terrain(self, map_path:str, name_list:list[str], color_list:list[np.ndarray], color_pair:list[tuple], tile_properties:list[str], delta_lxc:list[list[float]], png_path:str, tsx_path:str, rwmaps_dir:str = RWMAP_MAPS, tiy:int = -1, noise:list[list[float]] = [], randseed:int = -1, terrain_index_dict:dict = {})->None:
        tileset = case.TileSet.init_terrain_nt_t(name_list, color_list, color_pair, delta_lxc, rwmaps_dir, map_path, tile_properties, self.tile_size(), png_path, tsx_path, tiy = tiy, noise = noise, randseed = randseed, terrain_index_dict = terrain_index_dict)
        self.add_tileset_fromTileSet(tileset)

    def add_tileset_kmean(self, tileset_size:frame.Coordinate, imageLayer_name:str, map_path:str, png_path:str, tsx_path:str, resize_coo:frame.Coordinate = frame.Coordinate(), tile_properties_args = None, rwmaps_dir:str = RWMAP_MAPS, stopnum:int = 0, rand_seed:int = -1, limit_cycle:int = -1, isverbose:bool = True, isdebug:bool = False, noise:list[int] = [0, 0, 0], randseed:int = -1)->None:
        image_now = self.get_ndarray_fromImageLayer(imageLayer_name, resize_coo)

        tileset = case.TileSet.init_kmean(tileset_size, image_now, rwmaps_dir, map_path, self.tile_size(), png_path, tsx_path, tile_properties_args = tile_properties_args, mode_code = 0, stopnum = stopnum, limit_cycle = limit_cycle, isverbose = isverbose, isdebug = isdebug, noise = noise, randseed = randseed)
        self.add_tileset_fromTileSet(tileset)


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

    def delete_tileset_s(self, tileset_s:case.TileSet)->None:
        self._tileset_list.remove(tileset_s)
        self._tileset_now = None

    def delete_imageLayer_s(self, imageLayer_s:case.ImageLayer)->None:
        index_now = self._imageLayer_list.index(imageLayer_s)
        utility.remove_nth_occurrence(self._oli_order_list, const.OLI_TAG_DICT[imageLayer_s.tag()], index_now)
        self._imageLayer_list.remove(imageLayer_s)
        self._imageLayer_now = None

    def delete_layer_s(self, layer_s:case.Layer)->None:
        index_now = self._layer_list.index(layer_s)
        utility.remove_nth_occurrence(self._oli_order_list, const.OLI_TAG_DICT[layer_s.tag()], index_now)
        self._layer_list.remove(layer_s)
        self._layer_now = None

    def delete_objectGroup_s(self, objectGroup_s:case.ObjectGroup)->None:
        index_now = self._objectGroup_list.index(objectGroup_s)
        utility.remove_nth_occurrence(self._oli_order_list, const.OLI_TAG_DICT[objectGroup_s.tag()], index_now)
        self._objectGroup_list.remove(objectGroup_s)
        self._objectGroup_now = None

    def delete_tileset(self, tileset_name:str)->None:
        tilset_s = self.get_tileset_s(tileset_name)
        self.delete_tileset_s(tilset_s)

    def delete_imageLayer(self, imageLayer_name:str)->None:
        imageLayer_s = self.get_imageLayer_s(imageLayer_name)
        self.delete_imageLayer_s(imageLayer_s)

    def delete_layer(self, layer_name:str)->None:
        layer_s = self.get_layer_s(layer_name)
        self.delete_layer_s(layer_s)

    def delete_objectGroup(self, objectGroup_name:str)->None:
        objectGroup_s = self.get_objectGroup_s(objectGroup_name)
        self.delete_objectGroup_s(objectGroup_s)


    def append_objectGroup_s(self, objectGroup_s:case.ObjectGroup)->None:
        self._objectGroup_list.append(objectGroup_s)
        self._oli_order_list.append(0)

    def append_layer_s(self, layer_s:case.Layer)->None:
        self._layer_list.append(layer_s)
        self._oli_order_list.append(1)

    def append_imageLayer_s(self, imageLayer_s:case.ImageLayer)->None:
        self._imageLayer_list.append(imageLayer_s)
        self._oli_order_list.append(2)

    def add_layer(self, layername:str, compression:str = "default")->None:
        if compression == "default":
            if self._layer_list == []:
                compression = "zlib"
            else:
                compression = self._layer_list[0]._compression
        layer = case.Layer.init_Layer(frame.TagCoordinate(layername, self.size()), self.nextlayerid(), compression = compression)
        self.nextlayerid_pp()
        self.append_layer_s(layer)

    def add_imageLayer(self, imageLayer_properties:frame.TagCoordinate)->None:
        imageLayer = case.ImageLayer.init_imageLayer(imageLayer_properties, self.nextlayerid())
        self.nextlayerid_pp()
        self.append_imageLayer_s(imageLayer)

    def add_Layer_fromLayer(self, layer:case.Layer)->None:
        layer_n = deepcopy(layer)
        layer_n.changeid(self.nextlayerid())
        self.nextlayerid_pp()
        self.append_layer_s(layer_n)

    def add_objectgroup(self, objectgroup_name:str = const.NAME.Triggers)->None:
        objectgroup = case.ObjectGroup.init_ObjectGroup(objectgroup_name)
        self.append_objectGroup_s(objectgroup)

    def add_objectgroup_fromObjectGroup(self, objectgroup:case.ObjectGroup)->None:
        objectgroup_n = deepcopy(objectgroup)
        layerid = int(self._properties.returnDefaultProperty("nextlayerid"))
        self._properties.assignDefaultProperty("nextlayerid", str(layerid + 1))
        objectgroup_n.changeid(layerid)
        self.append_objectGroup_s(objectgroup_n)

    def write_png(self, dir:str)->None:
        for tileset in self._tileset_list:
            tileset.write_png(dir)

    def output_str(self, pngtextnum:int = -1, tilenum:int = -1, output_rectangle:frame.Rectangle = frame.Rectangle(frame.Coordinate(), frame.Coordinate(-1, -1)), objectnum:int = -1)->str:
        str_ans = ""
        str_ans = str_ans + self._properties.output_str() + "\n"
        str_ans = str_ans + "\n".join([tileset.output_str(pngtextnum, tilenum) for tileset in self._tileset_list if tileset.isexist()]) + "\n"
        str_ans = str_ans + "\n".join([layer.output_str(output_rectangle) for layer in self._layer_list]) + "\n"
        str_ans = str_ans + "\n".join([tobject.output_str(objectnum) for tobject in self._objectGroup_list]) + "\n"
        str_ans = str_ans + "\n".join([imageLayer.output_str() for imageLayer in self._imageLayer_list]) + "\n"
        str_ans = utility.indentstr_Tab(str_ans)
        return str_ans

    def __repr__(self)->str:
        return self.output_str()

    def output_etElement(self, isdeletetsxsource:bool = False, isdeleteimgsource:bool = False)->et.Element:
        root = et.Element("map")
        root = self._properties.output_etElement(root)
        if self._tileset_list != None:
            for tileset in self._tileset_list:
                if tileset.isexist():
                    root.append(tileset.output_etElement(isdeletetsxsource, isdeleteimgsource))
        oi = 0
        li = 0
        ii = 0
        for ni in self._oli_order_list:
            if ni == 0:
                node = self._objectGroup_list[oi]
                oi = oi + 1
            if ni == 1:
                node = self._layer_list[li]
                li = li + 1
            if ni == 2:
                node = self._imageLayer_list[ii]
                ii = ii + 1
            root.append(node.output_etElement())

        if self._other_elements != None:
            for other_element in self._other_elements:
                root.append(other_element)
        return root
    
    def change_map_path(self, map_path:str)->None:
        if self._tileset_list != None:
            for tileset in self._tileset_list:
                if tileset.isexist():
                    tileset.change_map_path(map_path)

    def write_file(self, map_file:str, ischangemappath:bool = True, isdeletetsxsource:bool = False, isdeleteimgsource:bool = False)->None:
        temp_map = deepcopy(self)
        if ischangemappath:
            temp_map.change_map_path(map_file)
        utility.output_file_from_etElement(temp_map.output_etElement(isdeletetsxsource, isdeleteimgsource), map_file)

    def tileset_dependent(self, rwmaps_dir = RWMAP_MAPS)->None:
        if self._tileset_list != None:
            for index, tileset in enumerate(self._tileset_list):
                if tileset.isexist():
                    self._tileset_list[index] = tileset.dependent(rwmaps_dir)

    def addObject_type(self, tobject:case.TObject, objectGroup_name:str = const.NAME.Triggers, isresetid = True):
        objectGroup_now = self.get_objectgroup_s_ex(objectGroup_name)
        
        if isresetid:
            tobject.assignDefaultProperty("id", self._properties.returnDefaultProperty("nextobjectid"))
            str_nextobjectid = str(max(int(self._properties.returnDefaultProperty("nextobjectid")), int(tobject.returnDefaultProperty("id")) + 1))
            self._properties.assignDefaultProperty("nextobjectid", str_nextobjectid)
        objectGroup_now.addObject_type(tobject)
        

    def addObject_dict(self, objectGroup_name:str = const.NAME.Triggers, default_properties:dict[str, str] = {}, optional_properties :dict[str, Union[str, dict[str, str]]] = {}, other_properties:list[et.Element] = [])->None:
        objectGroup_now = self.get_objectgroup_s_ex(objectGroup_name)
        default_properties_n = deepcopy(default_properties)
        if default_properties_n.get("id") == None:
            default_properties_n["id"] = self._properties.returnDefaultProperty("nextobjectid")
        objectGroup_now.addObject_dict(default_properties_n, optional_properties, other_properties)
        str_nextobjectid = str(max(int(self._properties.returnDefaultProperty("nextobjectid")), int(default_properties_n["id"]) + 1))
        self._properties.assignDefaultProperty("nextobjectid", str_nextobjectid)
    
    def addObject_one(self, tobject_one:object.TObject_One, offset:frame.Coordinate = frame.Coordinate(), objectGroup_name:str = const.NAME.Triggers):
        ntobject = tobject_one.offset(offset)
        self.addObject_dict(objectGroup_name, ntobject.default_properties(), ntobject.optional_properties(), ntobject.other_properties())

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

    def iterator_object_s(self, objectGroup_re:str = const.NAME.Triggers, default_re:dict[str, str] = {}, optional_re:dict[str, str] = {})->Generator[case.TObject, None, None]:
        for objectGroup_now in self._objectGroup_list:
            if re.match(objectGroup_re, objectGroup_now.name()):
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
        objectGroup_now = self.get_objectgroup_s_ex(objectGroup_name)
        objectGroup_now.deleteObject(tobject)

    def index_object_s(self, tobject:case.TObject, objectGroup_name:str = const.NAME.Triggers)->int:
        objectGroup_now = self.get_objectgroup_s_ex(objectGroup_name)
        return objectGroup_now.index_object_s(tobject)

    def _tileplace_to_gid(self, tileplace:Union[int, tuple[str, int], frame.TagCoordinate, frame.TagRectangle])->Union[set[int], int]:
        if isinstance(tileplace, int):
            tileplace_now = tileplace
        elif isinstance(tileplace, tuple) and isinstance(tileplace[0], str) and isinstance(tileplace[1], int):
            tileplace_now = self.get_tileset_s(tileplace[0]).tileid_to_gid(tileplace[1])
        elif isinstance(tileplace, frame.TagCoordinate) or isinstance(tileplace, frame.TagRectangle):

            if tileplace.tag()[-1] == const.KEY.tag_for_tile_notre:
                tileset_name = tileplace.tag()[:-1]
                isre = False
            else:
                tileset_name = tileplace.tag()
                isre = True
            tileset = self.get_tileset_s(tileset_name)
            if isinstance(tileplace, frame.TagCoordinate):
                tileplace_now = tileset.coo_to_gid(tileplace.place(), isre = isre)
            elif isinstance(tileplace, frame.TagRectangle):
                tileplace_now = tileset.rec_to_gid(tileplace.rectangle(), isre = isre)
        else:
            raise TypeError("The type of RWmap._tileplace_to_gid(..., tileplace) is wrong.")
        return tileplace_now

    def _tileplace_to_tileid(self, tileplace:Union[int, tuple[str, int], frame.TagCoordinate, frame.TagRectangle])->tuple[str, Union[int, set[int]]]:
        if isinstance(tileplace, int):
            tileset_now = self.get_tileset_fromgid_s(tileplace)
            tileplace_now = (tileset_now.name(), tileset_now.gid_to_tileid(tileplace))
        elif isinstance(tileplace, tuple) and isinstance(tileplace[0], str) and isinstance(tileplace[1], int):
            tileplace_now = tileplace
        elif isinstance(tileplace, frame.TagCoordinate) or isinstance(tileplace, frame.TagRectangle):

            if tileplace.tag()[-1] == const.KEY.tag_for_tile_notre:
                tileset_name = tileplace.tag()[:-1]
                isre = False
            else:
                tileset_name = tileplace.tag()
                isre = True
            tileset = self.get_tileset_s(tileset_name)

            if isinstance(tileplace, frame.TagCoordinate):
                tileplace_now = (tileset_name, tileset.coo_to_tileid(tileplace.place(), isre = isre))
            elif isinstance(tileplace, frame.TagRectangle):
                tileplace_now = (tileset_name, tileset.rec_to_tileid(tileplace.rectangle(), isre = isre))
        else:
            raise TypeError("The type of RWmap._tileplace_to_tileid(..., tileplace) is wrong.")
        return tileplace_now

    def addTile_gid(self, layerplace:frame.TagCoordinate, gid:int):
        if gid >= 0 and isinstance(gid, Integral):
            layer:case.Layer = self.get_layer_s(layerplace.tag())
        else:
            raise TypeError("gid is less than 0 or not integer.")
        layer.assigntileid(layerplace.place(), gid)

    def imageTile_fromTileSet(self, tileplace:Union[int, tuple[str, int], frame.TagCoordinate])->np.ndarray:
        tileid_now = self._tileplace_to_tileid(tileplace)
        return self.get_tileset_s(tileid_now[0]).imageTile_fromTileid(tileid_now[1])
    
    def imageTile_fromImageLayer(self, tileplace:frame.TagCoordinate)->np.ndarray:
        return self.get_imageLayer_s(tileplace.tag()).imageTile(tileplace.place(), self.tile_size())

    def addTile_auto(self, layer_name:str, imageLayer_name:str, func_fit_compare:str, isverbose:bool = True, tileSet_whiteSet:set = None):
        
        image_path = self.get_imageLayer_s(imageLayer_name).source_path()
        layer_now = self.get_layer_s(layer_name)

        nparr_imaLayer_list, ima_columns = utility.image_division_path(image_path, self.tile_size())
        ima_count = len(nparr_imaLayer_list)
        
        nparr_tileset_dict = {}
        for tileset in self._tileset_list:
            if tileset.isexist() and tileset.name() in tileSet_whiteSet:
                for ts_gid in range(tileset.totalgid()):
                    nparr_tileset_dict[tileset.tileid_to_gid(ts_gid)] = tileset.imageTile_fromTileid(ts_gid)
        size_now_w = self.size().x()
        size_now_h = self.size().y()
        
        for imlid in range(ima_count):
            if isverbose:
                print(f"{imlid} has been processed.")
            iml_coo_x = math.floor(imlid / ima_columns)
            iml_coo_y = imlid % ima_columns
            if iml_coo_x >= size_now_h or iml_coo_y >= size_now_w:
                continue

            nparr_imgLayer = nparr_imaLayer_list[imlid]
            fit_compare_max = -sys.float_info.max
            add_tileplace = 0
            for gid, nparr in nparr_tileset_dict.items():
                fit_compare = func_fit_compare(nparr_imgLayer, nparr)
                if fit_compare > fit_compare_max:
                    fit_compare_max = fit_compare
                    add_tileplace = gid
            layer_now._tilematrix[iml_coo_x, iml_coo_y] = add_tileplace



    def addTile_auto_quick(self, layer_name:str, imageLayer_name:str, isverbose:bool = True, isdebug = False, tileSet_whiteSet:set = None, layer_start:frame.Coordinate = frame.Coordinate(), image_start:frame.Coordinate = frame.Coordinate()):
        
        size_now = self.size() - layer_start
        tile_size_now = self.tile_size()

        image_now = self.get_ndarray_fromImageLayer(imageLayer_name)
        image_now = image_now[image_start.x():, image_start.y():]

        image_now_shape = image_now.shape
        image_size = frame.Coordinate(image_now_shape[1], image_now_shape[0]) // tile_size_now
        deal_size = frame.Coordinate(min(size_now.x(), image_size.x()), min(size_now.y(), image_size.y()))
        image_now = image_now[:deal_size.y() * tile_size_now.y(), :deal_size.x() * tile_size_now.x()]


        tilenum = 0
        for tileset in self._tileset_list:
            if tileset.isexist() and tileset.name() in tileSet_whiteSet:
                tilenum = tilenum + tileset.totalgid()

        gid_now = np.ndarray([tilenum], np.uint32)
        tileset_now = np.ndarray([tilenum, self.tile_size().y(), self.tile_size().x(), 3], np.uint8)
        tileset_now_dict = {}
        tileset_index = 0
        for tileset in self._tileset_list:
            if tileset.isexist() and tileset.name() in tileSet_whiteSet:
                for ts_gid in range(tileset.totalgid()):
                    gid_now[tileset_index] = tileset.tileid_to_gid(ts_gid)
                    tileset_now[tileset_index] = tileset.imageTile_fromTileid(ts_gid)[:, :, :3]
                    tileset_now_dict[tileset_index] = tileset.firstgid() + ts_gid
                    tileset_index = tileset_index + 1

        image_now = utility.memory_continuous_nparr(image_now)
        tileset_now = utility.memory_continuous_nparr(tileset_now)
        gid_now = utility.memory_continuous_nparr(gid_now)

        import rwmapautoc
        layer_n = rwmapautoc.layerauto(image_now, tileset_now, gid_now, 0, isverbose, isdebug)

        self.get_layer_s(layer_name)._tilematrix[layer_start.y():(layer_start.y() + deal_size.y()), layer_start.x():(layer_start.x() + deal_size.x())] = layer_n
        
    def addTile_terrain(self, layerplace:frame.TagCoordinate, tileplace:Union[int, tuple[str, int], frame.TagCoordinate]):
        layer_now = self.get_layer_s(layerplace.tag())
        tile = self._tileplace_to_tileid(tileplace)
        tileset_now = self.get_tileset_s(tile[0])
        tileid = tile[1]
        layer_now.assigntileid_terrain(layerplace.place(), tileset_now, tileid)


    def addTerrainid_square(self, layerRectangle:frame.TagRectangle, tileset_name:str, tileset_terrainid:Union[str, int], isedgeterrain = True):
        layer_now = self.get_layer_s(layerRectangle.tag())
        tileset_now = self.get_tileset_s(tileset_name)
        layer_now.assignterrainid_square(layerRectangle.rectangle(), tileset_now, tileset_terrainid, isedgeterrain = isedgeterrain)

    def addTerrainid_group(self, layername:str, tileset_name:str, terrainid_matrix:np.ndarray, original_grid:frame.Coordinate, rect_execute:frame.Rectangle = None):
        tileset_now = self.get_tileset_s(tileset_name)
        layer_now = self.get_layer_s(layername)
        layer_now.assignterrainid_squarematrix_exclude__1(original_grid, tileset_now, terrainid_matrix, rect_execute)

    def addTile(self, layerplace:frame.TagCoordinate, tileplace:Union[int, tuple[str, int], frame.TagCoordinate]):
        tileplace_now = self._tileplace_to_gid(tileplace)
        self.addTile_gid(layerplace, tileplace_now)

    def addTile_square(self, layerRectangle:frame.TagRectangle, tileplace:Union[int, tuple[str, int], frame.TagCoordinate])->None:
        tileplace_now = self._tileplace_to_gid(tileplace)
        layer:case.Layer = self.get_layer_s(layerRectangle.tag())
        layer.assigntileid_square(layerRectangle.rectangle(), tileplace_now)

    def addTile_group(self, tilegroup:tile.TileGroup_One, original_grid:frame.Coordinate, rect_execute:frame.Rectangle = None, isacce = False):
        selfid = str(id(self))
        gidmatrix = tilegroup.get_acce_s(selfid)
        if type(gidmatrix) != np.ndarray:
            gidmatrix = np.ndarray([tilegroup.size().x(), tilegroup.size().y()], dtype = np.uint32)
            for place_grid in tilegroup.size():
                gidmatrix[place_grid.x(), place_grid.y()] = self._tileplace_to_gid(tilegroup[place_grid])
        
        layer_s = self.get_layer_s(tilegroup.layername())
        
        layer_s.assigntileid_squarematrix_exclude0(original_grid, gidmatrix, rect_execute)
        if isacce:
            if type(tilegroup.get_acce_s(selfid)) != np.ndarray:
                tilegroup.save_acce_s(selfid, gidmatrix)

    def addTile_group_list(self, tilegroup_list:tile.TileGroup_List, original_grid:frame.Coordinate, rect_execute:frame.Rectangle = None):
        for tilegroup in tilegroup_list:
            self.addTile_group(tilegroup, original_grid, rect_execute)

    def addOTGroup(self, otgroup:otgroup.OTGroup, offset_grid:frame.Coordinate = frame.Coordinate()):
        self.addTile_group_list(otgroup._tilegroup_list, offset_grid)
        self.addObject_group(otgroup._tobject_group, offset_grid * self.tile_size())
        
    def resize(self, resize_t:frame.Coordinate)->RWmap:
        new_rwmap = deepcopy(self)
        new_rwmap._properties.assignDefaultProperty('height', str(int(self._properties.returnDefaultProperty('height')) * resize_t.x()))
        new_rwmap._properties.assignDefaultProperty('width', str(int(self._properties.returnDefaultProperty('width')) * resize_t.y()))
        for i, layer_n in enumerate(new_rwmap._layer_list):
            new_rwmap._layer_list[i] = layer_n.resize(resize_t)
        for i, objectgroup_n in enumerate(new_rwmap._objectGroup_list):
            new_rwmap._objectGroup_list[i] = objectgroup_n.resize(resize_t.transpose())
        return new_rwmap
        
    def _layerobjectgroup_to_dictnparr(self, obg_re_to_int_list:list[str, dict[str, int]])->dict[str, np.ndarray]:
        lobg_dict = {}
        tile_size_t = self.tile_size_t().changetype(np.uint32)
        for obg_re_to_int in obg_re_to_int_list:
            layer_tile = np.zeros(self.size_t().output_tuple(), np.uint32)
            ob_re_orall = "(" + ")|(".join(obg_re_to_int[1].keys()) + ")"
            for tobject in self.iterator_object_s(obg_re_to_int[0], {const.OBJECTDE.name, ob_re_orall}):
                size_tb = (int(tobject.returnDefaultProperty(const.OBJECTDE.y)) // tile_size_t.x(), int(tobject.returnDefaultProperty(const.OBJECTDE.x)) // tile_size_t.y())
                for ob_re, intn in obg_re_to_int[1].items():
                    if tobject.isreDefaultProperty(const.OBJECTDE.name, ob_re):
                        layer_tile[size_tb] = intn
            lobg_dict[obg_re_to_int[0]] = layer_tile
        for layer_s in self._layer_list:
            lobg_dict[layer_s.name()] = layer_s._tilematrix
        return lobg_dict

    def _tileplace_to_setofgid(self, tileplace:const.LAOBG_TILE)->set[int]:
        set_n = self._tileplace_to_gid(tileplace)
        if isinstance(set_n, int):
            set_n = set([set_n])
        return set_n

    def _tileplacedict_to_dictofsetofgid(self, tileplace_dict:dict[str, const.LAOBG_TILE])->dict[str, set[int]]:
        gidset_dict = {}
        for key, tileplace in tileplace_dict.items():
            gidset_dict[key] = self._tileplace_to_setofgid(tileplace)
        return gidset_dict

    def _layerobjectgroup_to_exenparr(self, lobg_dict:dict[str, np.ndarray], 
                                     tileplace_to_exe:list[dict[str, const.LAOBG_TILE], int])->np.ndarray:
        exe_nparr = np.zeros(self.size_t().output_tuple(), np.uint32)
        for tileplace_exe in tileplace_to_exe:
            tileplace_and = self._tileplacedict_to_dictofsetofgid(tileplace_exe[0])
            exe = tileplace_exe[1]
            mask = np.ones(self.size_t().output_tuple(), np.bool_)
            for lobg_name, gidset in tileplace_and.items():
                mask = mask & (np.in1d(lobg_dict[lobg_name], gidset))
            exe_nparr[mask] = exe
        return exe_nparr

    def _exe_to_tileplace_change_lobg(self, lobg_dict:dict[str, np.ndarray], exe_nparr:np.ndarray, exe_to_laygid:dict[int, list[tuple[str, int]]]):
        for i in range(exe_nparr.shape[0]):
            for j in range(exe_nparr.shape[1]):
                lsn = exe_to_laygid[exe_nparr[i, j]]
                for la, tc in lsn:
                    lobg_dict[la][i, j] = tc

    def layerobjectgroup_map_auto(self, obg_re_to_int_list:list[str, dict[str, int]], 
                                  tileplace_to_exe:list[list[frame.TagRectangle, tuple[str, set[int]], tuple[str, int]], int], 
                                  exe_to_tileplace:dict[int, list[tuple[str, frame.TagCoordinate]]], 
                                  exe_to_exe:dict[int, list[list[int]]] = {}, exe_mode:str = 'map')->RWmap:
        map_temp = deepcopy(self)
        lobg_dict = map_temp._layerobjectgroup_to_dictnparr(obg_re_to_int_list)
        exe_nparr = map_temp._layerobjectgroup_to_exenparr(lobg_dict, tileplace_to_exe)
        if exe_mode == 'expansion':
            exenparr_deal_expand(exe_nparr, exe_to_exe)
        elif exe_mode == 'terrain':
            exenparr_deal_shrink(exe_nparr, exe_to_exe)
        elif exe_mode == 'map':
            pass
        exe_to_laygid = {k:[(vi[0], self._tileplace_to_gid(vi[1])) for vi in v] for k, v in exe_to_tileplace.items()}
        map_temp._exe_to_tileplace_change_lobg(lobg_dict, exe_nparr, exe_to_laygid)



        
