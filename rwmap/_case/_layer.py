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
from rwmap._case._tileset import TileSet
import rwmap._data.const as const


class Layer(ElementOri):
    pass

class Layer(ElementOri):
    def __init__(self, properties:ElementProperties, tilematrix:np.ndarray, encoding:str, compression:Union[str, None])->None:
        super().__init__(const.TAG.layer, properties)
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
    def init_Layer(cls, property:frame.TagCoordinate, id:int, compression:str = "zlib")->None:
        properties = ElementProperties("layer", {"id": str(id), "name": property.tag(), "width": str(property.x()), "height": str(property.y())})
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
    
    def reset_terraintileid(self, firstgid:int, endgid:int):
        self._isterraintileid = self._tilematrix.copy().astype(np.int32) - np.ones(self._tilematrix.shape, np.int32) * firstgid
        condition = (self._tilematrix < firstgid) | (self._tilematrix >= endgid)
        self._isterraintileid[condition] = -1

    def assign_terraintileid_fromnewmatrix(self, pos:frame.Coordinate, gidmatrix:np.ndarray, firstgid:int, endgid:int, tilerec:frame.Rectangle = None):
        if not isinstance(self._isterraintileid, np.ndarray):
            self._isterraintileid = -np.ones(self._tilematrix.shape, np.int32)
        tileidmatrix_now = gidmatrix.copy().astype(np.int32) - np.ones(gidmatrix.shape, np.int32) * firstgid
        condition = (gidmatrix < firstgid) | (gidmatrix >= endgid)
        tileidmatrix_now[condition] = -1
        utility.save_matrix_exclude0(self._isterraintileid, pos, tileidmatrix_now, tilerec, exclude = -1)


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
                         max(0, square_grid.i().y()):min(size.y(), square_grid.e().y())] = tileid

    def assigntileid_squarematrix_exclude0(self, pos:frame.Coordinate, tileid_matrix:np.ndarray, tilerec:frame.Rectangle = None):
        utility.save_matrix_exclude0(self._tilematrix, pos, tileid_matrix, tilerec)

    def assigntileid_squarematrix(self, pos:frame.Coordinate, tileid_matrix:np.ndarray, tilerec:frame.Rectangle = None):
        utility.save_matrix(self._tilematrix, pos, tileid_matrix, tilerec)

    def assigntileid_terrain(self, place_grid:frame.Coordinate, tileset:TileSet, tileid:int, isinitial = True, depth = 0):
        
        if not (self.size().contain(place_grid) and place_grid.contain(const.COO.SIZE_ZERO)):
            return
    
        if self._isterraintileid[place_grid.x(), place_grid.y()] == -1 or \
           ((not isinitial) and self._isterraintileid[place_grid.x(), place_grid.y()] == tileid):
            return
        
        if depth >= 2:
            return
            import pdb;pdb.set_trace()

        #print(depth, place_grid, self._isterraintileid[place_grid.x(), place_grid.y()], tileid)

        self._isterraintileid[place_grid.x(), place_grid.y()] = tileid
        self.assigntileid(place_grid, tileset.tileid_to_gid(tileid))
        terrain_expand = tileset.tileid_to_terrain_expand(tileid)
        
        #print(terrain_expand)
        
        for i, ter_j in enumerate(terrain_expand):
            for j, ter in enumerate(ter_j):
                place_grid_now = place_grid + frame.Coordinate(i - 1, j - 1)
                try:
                    tileid_now = tileset.gid_to_tileid(self.tileid(place_grid_now))
                except:
                    continue
                tileid_now = tileid_now[1]
                try:
                    tileid_assign = tileset.terrain_trans_to_tileid(tileid_now, ter)
                except:
                    continue
                self.assigntileid_terrain(place_grid_now, tileset, tileid_assign, isinitial = False, depth = depth + 1)


    def assignterrainid_square(self, square_grid:frame.Rectangle, tileset:TileSet, terrainid:Union[str, int], isedgeterrain:bool = True):
        size = self.size()

        xi = max(0, square_grid.i().x())
        xe = min(size.x(), square_grid.e().x())
        yi = max(0, square_grid.i().y())
        ye = min(size.y(), square_grid.e().y())
        
        if isinstance(terrainid, str):
            terrainid = tileset._terrainname_to_terrainid_dict[terrainid]
        tileid = tileset.terrainid_to_tileid(terrainid)
        gid = tileset.tileid_to_gid(tileid)

        self._tilematrix[xi:xe, yi:ye] = gid
        if isedgeterrain:
            for i in range(xi, xe):
                self.assigntileid_terrain(frame.Coordinate(i, yi), tileset, tileid)
                self.assigntileid_terrain(frame.Coordinate(i, ye - 1), tileset, tileid)
            for i in range(yi, ye):
                self.assigntileid_terrain(frame.Coordinate(xi, i), tileset, tileid)
                self.assigntileid_terrain(frame.Coordinate(xe - 1, i), tileset, tileid)
        else:
            self.reset_terraintileid(tileset.firstgid(), tileset.endgid())

    def assignterrainid_squarematrix_exclude__1(self, pos:frame.Coordinate, tileset:TileSet, terrainid_matrix:np.ndarray, tilerec:frame.Rectangle = None):
        terrainid_to_tileid_dict = deepcopy(tileset._terrainid_to_tileid_dict)
        terrainid_to_tileid_dict = {-1:0} | {k:tileset.tileid_to_gid(v) for k, v in terrainid_to_tileid_dict.items()}
        
        vectorize_get = np.vectorize(terrainid_to_tileid_dict.get)

        tilematrix = vectorize_get(terrainid_matrix)

        utility.save_matrix_exclude0(self._tilematrix, pos, tilematrix, tilerec)

        pos_n, in_matrix_n, tilerec_n = utility.change_save_matrix_condition(self._tilematrix, pos, terrainid_matrix, tilerec)
        
        self.assign_terraintileid_fromnewmatrix(pos, tilematrix, tileset.firstgid(), tileset.endgid(), tilerec)
        
        for pos_index in pos_n:
            tilerec_index = pos_index - pos_n.i() + tilerec_n.i()
            if in_matrix_n[tilerec_index.x(), tilerec_index.y()] != -1 and (
                (tilerec_index.x() != pos_n.i().x() and in_matrix_n[tilerec_index.x() - 1, tilerec_index.y()] != in_matrix_n[tilerec_index.x(), tilerec_index.y()]) or
                (tilerec_index.x() != pos_n.e().x() - 1 and in_matrix_n[tilerec_index.x() + 1, tilerec_index.y()] != in_matrix_n[tilerec_index.x(), tilerec_index.y()]) or
                (tilerec_index.y() != pos_n.i().y() and in_matrix_n[tilerec_index.x(), tilerec_index.y() - 1] != in_matrix_n[tilerec_index.x(), tilerec_index.y()]) or
                (tilerec_index.y() != pos_n.e().y() - 1 and in_matrix_n[tilerec_index.x(), tilerec_index.y() + 1] != in_matrix_n[tilerec_index.x(), tilerec_index.y()])):
                
                self.assigntileid_terrain(pos_index, tileset, tileset._terrainid_to_tileid_dict[in_matrix_n[tilerec_index.x(), tilerec_index.y()]])
    

    def resize(self, resize_t:frame.Coordinate)->Layer:
        layer_new = deepcopy(self)
        layer_new._properties.assignDefaultProperty('height', str(int(self._properties.returnDefaultProperty('height')) * resize_t.x()))
        layer_new._properties.assignDefaultProperty('width', str(int(self._properties.returnDefaultProperty('width')) * resize_t.y()))
        layer_new._tilematrix = np.repeat(layer_new._tilematrix, repeats = resize_t.x(), axis = 0)
        layer_new._tilematrix = np.repeat(layer_new._tilematrix, repeats = resize_t.y(), axis = 1)
        return layer_new
