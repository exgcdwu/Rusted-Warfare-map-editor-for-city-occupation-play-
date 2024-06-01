import os
import sys

current_dir_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir_path)

from copy import deepcopy
import numpy as np
import rwmap as rw



origin_square = rw.frame.Coordinate(0.5, -0.5, dtype = np.float32)
tile_size = rw.const.COO.SIZE_STANDARD
square_size_tile = rw.frame.Coordinate(28, 24)
hex_size_tile = rw.frame.Coordinate(28, 32)
map_size_square = rw.frame.Coordinate(17, 5)

square_size_pixel = square_size_tile * tile_size
hex_size_pixel = hex_size_tile * tile_size
map_size_tile = map_size_square * square_size_tile

class Hexrwmap:
    def __init__(self, square_size_tile, map_size_square, origin_square, 
                 layer_file:str, object_file:str, 
                 form_str = "hex_x", tile_size = rw.const.COO.SIZE_STANDARD)->None:
        self._square_size_tile = square_size_tile
        self._map_size_square = map_size_square
        self._origin_square = origin_square
        self._form_str = form_str
        self._tile_size = tile_size
        self._layer_file = layer_file
        self._object_file = object_file

    def _square_size_pixel(self)-> rw.frame.Coordinate:
        return self._square_size_tile * self._tile_size
    
    def _map_size_tile(self)-> rw.frame.Coordinate:
        return self._map_size_square * self._square_size_tile