import os
import sys
current_dir_path = os.path.dirname(os.path.abspath(__file__))
example_dir_path = os.path.dirname(current_dir_path)

package_dir = os.path.dirname(example_dir_path)
sys.path.append(package_dir)
#这两项可以省略，如果pip安装（确定包的位置）

from copy import deepcopy
import numpy as np

import rwmap as rw

RWMAP_VERSION = "1.0.0.0"
RWMAP_GROUND_VERSION = RWMAP_VERSION[0:3]

project_hex_x_to_cart = np.array([[1, -0.5], [0, 1]], dtype = np.float32)
project_cart_to_tobject_coo = np.array([[1, 0], [0, -1]], dtype = np.float32)
project_cart_to_layer_coo = np.array([[0, -1], [1, 0]], dtype = np.float32)

origin_square = rw.frame.Coordinate(0.5, -0.5, dtype = np.float32)
tile_size = rw.const.COO.SIZE_STANDARD
square_size_tile = rw.frame.Coordinate(28, 24)
map_size_square = rw.frame.Coordinate(17, 5)

hex_topleft_origin_layer_tile = rw.frame.Coordinate(-16, -14)
city_origin_tile = rw.frame.Coordinate(-1, -1)

map_size_tile = map_size_square * square_size_tile

def pos_tile_cart(square_hex_x:rw.frame.Coordinate)->rw.frame.Coordinate:
    square_hex_x_float = rw.frame.Coordinate(square_hex_x.x(), square_hex_x.y(), dtype = np.float32)
    square_ori_cart = square_hex_x_float * project_hex_x_to_cart
    square_ld_cart = square_ori_cart + origin_square
    square_lt_cart = square_ld_cart - rw.frame.Coordinate(0, map_size_square.y(), dtype = np.float32)
    tile_lt_cart = square_lt_cart * square_size_tile
    tile_lt_cart_int = rw.frame.Coordinate(tile_lt_cart.x(), tile_lt_cart.y())
    return tile_lt_cart_int

def pos_tile_object(square_hex_x:rw.frame.Coordinate, offset_grid:rw.frame.Coordinate)->rw.frame.Coordinate:
    tile_lt_cart = pos_tile_cart(square_hex_x)
    tile_lt_tobject_coo = tile_lt_cart * tile_lt_cart
    tile_lt_tobject_coo_offset = tile_lt_tobject_coo + offset_grid
    return tile_lt_tobject_coo_offset

def pos_pixel_object(square_hex_x:rw.frame.Coordinate, offset_grid:rw.frame.Coordinate)->rw.frame.Coordinate:
    pixel_lt_tobject_coo_offset = pos_tile_object(square_hex_x, offset_grid) * tile_size
    return pixel_lt_tobject_coo_offset

def pos_tile_layer(square_hex_x:rw.frame.Coordinate, offset_grid:rw.frame.Coordinate)->rw.frame.Coordinate:
    tile_lt_cart = pos_tile_cart(square_hex_x)
    tile_lt_cart_layer_coo = tile_lt_cart * project_cart_to_layer_coo
    tile_lt_cart_layer_coo_offet = tile_lt_cart_layer_coo + offset_grid
    return tile_lt_cart_layer_coo_offet

def pos_tile_to_pixel(coo_grid:rw.frame.Coordinate)->rw.frame.Coordinate:
    return tile_size * coo_grid

lukimap = rw.RWmap.init_mapfile(f'{current_dir_path}\\Velikie Luki 1942(basic map and ground)({RWMAP_GROUND_VERSION}).tmx')
# 反攻大卢基地块地图输入

origin = rw.frame.Coordinate(0, 0)
lukimap.addObject_one(rw.object_useful.Mapinfo(origin, rw.const.MAPTYPE.skirmish, 
                                                rw.const.FOG.los, rw.const.WIN.commandCenter, 
                                                text = 
                                                "城市争夺玩法2v2包围机制地图。\n\
                                                地图版本:V.{RWMAP_VERSION} \n\
                                                地图官方群及发布点:699981990 \n\
                                                地图作者：咕咕咕   \n\
                                                特别感谢斐比寻常W'213的教程、 Xs的巴巴罗萨计划城夺地图。"))
#添加map_info

credit_pos = rw.frame.Coordinate(0, -20)
lukimap.addObject_one(rw.object_useful.Credit(credit_pos, 0, setCredits = 0, reset = 1))
lukimap.addObject_one(rw.object_useful.Credit(credit_pos, 1, setCredits = 0, reset = 1))
lukimap.addObject_one(rw.object_useful.Credit(credit_pos, 2, setCredits = 0, reset = 1))
lukimap.addObject_one(rw.object_useful.Credit(credit_pos, 3, setCredits = 0, reset = 1))
#添加credit重置

city = [
    
]




lukimap.write_file(f'{current_dir_path}\\Velikie Luki 1942({RWMAP_VERSION}).tmx')
# 输出地图到当前文件夹

maps_dir_path = "D:\\Game\\steam\\steamapps\\common\\Rusted Warfare\\mods\\maps"
lukimap.write_file(f'{maps_dir_path}\\反攻大卢基(1942.11.8-1943.1.9)【4p,包围城夺】(V.{RWMAP_VERSION}).tmx')
# 输出地图到游戏地图文件夹

