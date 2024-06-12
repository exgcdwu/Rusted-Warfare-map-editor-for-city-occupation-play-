import os
import sys

current_dir_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir_path)

from copy import deepcopy
import numpy as np
import rwmap as rw

import _const as const

class SqRwmap:
    def __init__(self, square_size_tile, map_size_square, origin_square, 
                 map_dir_path:str, layer_file:str, map_file:str, 
                 form_str = "hex_x", tile_size = rw.const.COO.SIZE_STANDARD, 
                 map_path_list:list[str] = [], 
                 layer_need_list:list[str] = 
                 [rw.const.NAME.Ground, rw.const.NAME.Items, rw.const.NAME.Units], 
                 objectgroup_need_list:list[str] = [rw.const.NAME.Triggers])->None:
        self._square_size_tile = deepcopy(square_size_tile)
        self._map_size_square = deepcopy(map_size_square)
        self._origin_square = deepcopy(origin_square)
        self._project_to_cart = deepcopy(const.PROJECT_TO_CART[form_str])
        self._tile_size = deepcopy(tile_size)
        self._map_dir_path = deepcopy(map_dir_path)
        self._layer_file = deepcopy(layer_file)
        self._map_file = deepcopy(map_file)
        self._map_path_list = deepcopy(map_path_list)
        self._layer_need_list = layer_need_list
        self._objectgroup_need_list = objectgroup_need_list
        self._isterrain = False

    def _layer_path(self)->str:
        return self._map_dir_path + "\\" + self._layer_file

    def _object_path(self)->str:
        return self._map_dir_path + "\\" + self._object_file

    def _square_size_pixel(self)-> rw.frame.Coordinate:
        return self._square_size_tile * self._tile_size
    
    def _map_size_tile(self)-> rw.frame.Coordinate:
        return self._map_size_square * self._square_size_tile
    
    def _pos_tile_cart(self, square:rw.frame.Coordinate)->rw.frame.Coordinate:
        square_float = rw.frame.Coordinate(square.x(), square.y(), dtype = np.float32)
        square_ori_cart = square_float * self._project_to_cart
        square_ld_cart = square_ori_cart + self._origin_square
        square_lt_cart = square_ld_cart - rw.frame.Coordinate(0, self._map_size_square.y(), dtype = np.float32)
        tile_lt_cart = square_lt_cart * self._square_size_tile
        tile_lt_cart_int = rw.frame.Coordinate(tile_lt_cart.x(), tile_lt_cart.y())
        return tile_lt_cart_int

    def _pos_tile_object(self, square:rw.frame.Coordinate, offset_grid:rw.frame.Coordinate = rw.frame.Coordinate(0, 0))->rw.frame.Coordinate:
        tile_lt_cart = self._pos_tile_cart(square)
        tile_lt_tobject_coo = tile_lt_cart * const.PROJECT_CART_TO_TOBJECT_COO
        tile_lt_tobject_coo_offset = tile_lt_tobject_coo + offset_grid
        return tile_lt_tobject_coo_offset
    
    def _pos_pixel_object(self, square:rw.frame.Coordinate, offset_grid:rw.frame.Coordinate = rw.frame.Coordinate(0, 0), offset_pixel:rw.frame.Coordinate  = rw.frame.Coordinate(0, 0))->rw.frame.Coordinate:
        pixel_lt_tobject_coo_offset = self._pos_tile_object(square, offset_grid) * self._tile_size
        return pixel_lt_tobject_coo_offset + offset_pixel

    def _pos_tile_layer(self, square:rw.frame.Coordinate, offset_grid:rw.frame.Coordinate = rw.frame.Coordinate(0, 0))->rw.frame.Coordinate:
        tile_lt_cart = self._pos_tile_cart(square)
        tile_lt_cart_layer_coo = tile_lt_cart * const.PROJECT_CART_TO_LAYER_COO
        tile_lt_cart_layer_coo_offset = tile_lt_cart_layer_coo + offset_grid
        return tile_lt_cart_layer_coo_offset

    def pos_tile_to_pixel(self, coo_grid:rw.frame.Coordinate, offset_pixel:rw.frame.Coordinate  = rw.frame.Coordinate(0, 0))->rw.frame.Coordinate:
        return (self._tile_size * coo_grid) + offset_pixel   

    def add_tileset_fromMapPath_list(self, map_path_list:list[str])->None:
        self._map_path_list = self._map_path_list + deepcopy(map_path_list)

    def add_terrain(self, terrain_matrix:list[list[str]], 
                    terrain_dict:dict[str, rw.tile.TileGroup_List], 
                    terrain_offset_tile:rw.frame.Coordinate, 
                    layer_need_list:list[str] = []):
        '''
            terrain_matrix:shape:[self._map_size_square * np.array([[1, 0.5], [0, 1]], dtype = np.float32)]+(0, 2)
            Empty terrain is "e"
        '''
        self._terrain_matrix = deepcopy(terrain_matrix)
        self._terrain_dict = deepcopy(terrain_dict)
        self._terrain_offset = deepcopy(terrain_offset_tile)
        self._layer_need_list = self._layer_need_list + deepcopy(layer_need_list)
        self._isterrain = True

    def _add_terrain_to_map(self, map_s:rw.RWmap):
        for x, terrain_y_list in enumerate(self._terrain_matrix):
            for y, terrain_str in enumerate(terrain_y_list):
                if terrain_str == const.KEY.empty_square:
                    continue
                pos_terrain_lt = self._pos_tile_layer(rw.frame.Coordinate(x, y), self._terrain_offset)
                terrain = self._terrain_dict[terrain_str]
                map_s.addTile_group_list(terrain, pos_terrain_lt)

    def write_layer_path(self):
        rwmap_now = rw.RWmap.init_map(self._map_size_tile(), self._tile_size)

        for map_path in self._map_path_list:
            rwmap_now.add_tileset_fromMapPath(map_path)

        for layer_str in self._layer_need_list:
            rwmap_now.add_layer(layer_str)

        if self._isterrain:
            self._add_terrain_to_map(rwmap_now)

        rwmap_now.write_file(self._layer_path())

        rwmap_now.write_png(self._map_dir_path)
        


