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
import hexcity

RWMAP_GROUND_VERSION = "1.0"

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

lukimap = rw.RWmap.init_map(map_size_tile, tile_size = tile_size)
# 反攻大卢基空地图 
lukimap.add_tileset_fromMapFile(f'{example_dir_path}\\template\\v3.tmx')
# 添加V3模板地块集
lukimap.add_tileset_fromMapFile(f'{example_dir_path}\\template\\city occupation(tile property).tmx')
# 添加城夺地块集
lukimap.write_png(f'{current_dir_path}')
# 将地块集图片全部输出，以便使用Tiled观看

comap = rw.RWmap.init_mapfile(f'{example_dir_path}\\template\\city occupation(tile property).tmx')
comap.write_file(f'{example_dir_path}\\template\\公用地图块（带属性，排序）.tmx')

print(lukimap.tileset_name_list())
# 显示地块集名称

lukimap.add_layer(rw.const.NAME.Ground)
lukimap.add_layer(rw.const.NAME.Units)
lukimap.add_layer(rw.const.NAME.Items)
lukimap.add_layer(rw.const.NAME.PathingOverride)
#lukimap.get_layer_s(rw.const.NAME.ItemsExtra).change_opacity(0)
lukimap.add_objectgroup(rw.const.NAME.Triggers)
# 添加图层和地块层

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


export_ground = "export_ground"

city_occu_tile_name_180b = "巴巴罗萨计划（1.80beta版）地块byXs"
city_occu_tile_name_160b = "巴巴罗萨计划（1.60beta版）地块byXs"
city_occu_tile_name_150 = "巴巴罗萨计划（1.50版）地块byXs"
city_occu_tile_name_B3 = "巴巴罗萨计划（B3版）地块byXs"
city_occu_sup_tile_name_12 = '辅助地块（1.2版）byXs'


tilegroup_wood = rw.tile.TileGroup_One.init_tilegroup_addlayer(
    {
        "b": rw.frame.TagCoordinate.init_xy(export_ground, 13, 7), 
        "p": rw.frame.TagCoordinate.init_xy(city_occu_tile_name_160b, 4, 1)
    }, 
    hexcity.tgroup.tile_group_addlayer_ground_hex28_32_fill_barrier_terrain
)
# 树林地块组

tilegroup_swamp = rw.tile.TileGroup_One.init_tilegroup_addlayer(
    {
        "b": rw.frame.TagCoordinate.init_xy(city_occu_tile_name_150, 5, 3), 
        "p": rw.frame.TagCoordinate.init_xy(city_occu_tile_name_150, 4, 3)
    }, 
    hexcity.tgroup.tile_group_addlayer_ground_hex28_32_fill_barrier_terrain
)
# 沼泽地块组

tilegroup_plane = rw.tile.TileGroup_One.init_tilegroup_addlayer(
    {"p": rw.frame.TagCoordinate.init_xy(city_occu_tile_name_180b, 4, 4), 
     "b": rw.frame.TagCoordinate.init_xy(city_occu_tile_name_180b, 5, 5)}, 
    hexcity.tgroup.tile_group_addlayer_ground_hex28_32_fill_light_barrier
)
# 平原地块组

tilegroup_cliff = rw.tile.TileGroup_One.init_tilegroup_addlayer(
    {
        "b": rw.frame.TagCoordinate.init_xy(city_occu_tile_name_B3, 6, 2), 
        "p": rw.frame.TagCoordinate.init_xy(city_occu_tile_name_B3, 4, 1)
    }, 
    hexcity.tgroup.tile_group_addlayer_ground_hex28_32_fill_barrier_terrain
)
# 山脉地块组

core_rect = rw.frame.Rectangle(rw.frame.Coordinate(15, 13), rw.frame.Coordinate(2, 2))
tilegroup_core_item = rw.tile.TileGroup_One.init_tilegroup_matrix(
    rw.const.NAME.Items, 
    {"ic": rw.frame.TagCoordinate.init_xy(city_occu_tile_name_180b, 4, 13)}, 
    hexcity.tgroup.tile_group_hex28_32_fill_acore.part(core_rect).map({"r":"ic", "c":"ic"})
)
tilegroup_core_ground = rw.tile.TileGroup_One.init_tilegroup_matrix(
    rw.const.NAME.Ground, 
    {"gc": rw.frame.TagCoordinate.init_xy(city_occu_tile_name_180b, 4, 7)}, 
    hexcity.tgroup.tile_group_hex28_32_fill_acore.part(core_rect).map({"r":"gc", "c":"gc"})
)
tilegroup_core_itemsextra = rw.tile.TileGroup_One.init_tilegroup_matrix(
    rw.const.NAME.PathingOverride, 
    {"iec": rw.frame.TagCoordinate.init_xy(city_occu_sup_tile_name_12, 9, 4)}, 
    hexcity.tgroup.tile_group_hex28_32_fill_acore.part(core_rect).map({"r":"iec"})
)

# 核心地块




terrain = [
    ["s,N", "w"], 
    ["s", "w,N", "w", "p", ",E"], 
    ["w", "w", "w,N", "p", "w,E", "s"], 
    ["p", "w", "p", "p", "p-N,NSE", "s-NE", "s"],  
    ["s,N", "w", "c", "w", "w,E", "p-ES", "p,S"], 
    ["w", "p,NES", "p", "p,E", "w,S", "c", "w-S"], 
    ["s", "p,N", "p,N", "p,E", "w", "w", "w"], 
    ["w-E", "s", "p,E", "p,E", "p-N,S", "p-S,SN", "p"], 
    ["w", "s-NES", "p-NE,N", "p-E,E", "p", "s-ES", "p"], 
    ["w", "p", "p", "p,E", "s-ES", "s", "w-ES"], 
    ["s", "w", "p,E", "p,ES", "p,", "s-NES", "w-E"], 
    ["w", "w,E", "p,S", "p,E", "w", "s", "s"], 
    ["w-ES", "w,E", "c,NS", "p,E", "p", "w", "w"],
    ["s", "p-ES,E", "c", "w,E", "w", "w", "w"],
    ["w", "p,E", "w-ES", "w,E", "c", "w", "w"],
    ["w-NES", "p-E,E", "w", "w-ES,N", "w", "w", "w"],
    ["p", "p,S", "p-S", "p", "w-NES,N", "w-NE", "c"],
    ["e", "w", "w", "w", "w", "w,N", "w"],
    ["e", "e", "e", "w", "w", "w", "w"],
    ["e", "e", "e", "e", "e", "w", "w"],
]
# 地形-河流,铁路



for x, terrain_y_list in enumerate(terrain):
    for y, terrain_now in enumerate(terrain_y_list):
        
        terrain_now_templist = hexcity.sutility.get_str_end_split(terrain_now, ",")
        terrain_railway = terrain_now_templist[1]

        terrain_now_templist = hexcity.sutility.get_str_end_split(terrain_now_templist[0], "-")
        terrain_river = terrain_now_templist[1]

        terrain_tile = terrain_now_templist[0]

        terrain[x][y] = [terrain_tile, terrain_river, terrain_railway]

for x, terrain_y_list in enumerate(terrain):
    for y, terrain_now in enumerate(terrain_y_list):
        terrain_now_tile = terrain_now[0]
        if terrain_now_tile == "e":
            continue
        elif terrain_now_tile == "w":
            tilegroup_now = tilegroup_wood
        elif terrain_now_tile == "s":
            tilegroup_now = tilegroup_swamp
        elif terrain_now_tile == "p":
            tilegroup_now = tilegroup_plane
        elif terrain_now_tile == "c":
            tilegroup_now = tilegroup_cliff
        pos_grid = pos_tile_layer(rw.frame.Coordinate(x, y), hex_topleft_origin_layer_tile)
        lukimap.addTile_group(tilegroup_now, pos_grid, isacce = True)
        # 添加地形




for x, terrain_y_list in enumerate(terrain):
    for y, terrain_now in enumerate(terrain_y_list):
        river_now = hexcity.direction.str_to_NESbool(hexcity.lutility.get_listoflist_s(terrain, [x, y, 1]))
        river_N = hexcity.direction.str_to_NESbool(hexcity.lutility.get_listoflist_s(terrain, [x + 1, y + 1, 1]))
        river_S = hexcity.direction.str_to_NESbool(hexcity.lutility.get_listoflist_s(terrain, [x, y - 1, 1]))
        railway_now = hexcity.direction.str_to_NESbool(hexcity.lutility.get_listoflist_s(terrain, [x, y, 2]))

        river_NEESE = hexcity.direction.NESbool_to_NEESE(river_now)

        river_dict_now_list = hexcity.direction.river_dict(city_occu_tile_name_180b, 0, river_NEESE)

        river_dict_now = river_dict_now_list[0]

        river_dict_now_item = river_dict_now_list[1]

        river_map = hexcity.direction.river_map(river_now, river_N, river_S, railway_now)

        tile_group_hex28_32_border_now = hexcity.tgroup.tile_group_hex28_32_border.map(river_map)

        tilegroup_border_now = rw.tile.TileGroup_One.init_tilegroup_matrix(
            rw.const.NAME.Ground, 
            river_dict_now, 
            tile_group_hex28_32_border_now
        )
        tilegroup_border_now_item = rw.tile.TileGroup_One.init_tilegroup_matrix(
            rw.const.NAME.Items, 
            river_dict_now_item, 
            tile_group_hex28_32_border_now
        )
        
        #河流地块组

        pos_grid = pos_tile_layer(rw.frame.Coordinate(x, y), hex_topleft_origin_layer_tile)
        lukimap.addTile_group(tilegroup_border_now, pos_grid)
        lukimap.addTile_group(tilegroup_border_now_item, pos_grid)
        #添加河流

for x, terrain_y_list in enumerate(terrain):
    for y, terrain_now in enumerate(terrain_y_list):

        railway_now = hexcity.direction.str_to_NESbool(hexcity.lutility.get_listoflist_s(terrain, [x, y, 2]))
        railway_N = hexcity.direction.str_to_NESbool(hexcity.lutility.get_listoflist_s(terrain, [x, y + 1, 2]))
        railway_S = hexcity.direction.str_to_NESbool(hexcity.lutility.get_listoflist_s(terrain, [x - 1, y - 1, 2]))
        railway_W = hexcity.direction.str_to_NESbool(hexcity.lutility.get_listoflist_s(terrain, [x - 1, y, 2]))

        river_now = hexcity.direction.str_to_NESbool(hexcity.lutility.get_listoflist_s(terrain, [x, y, 1]))
        river_NW = hexcity.direction.str_to_NESbool(hexcity.lutility.get_listoflist_s(terrain, [x, y + 1, 1]))
        river_W = hexcity.direction.str_to_NESbool(hexcity.lutility.get_listoflist_s(terrain, [x - 1, y, 1]))
        river_SW = hexcity.direction.str_to_NESbool(hexcity.lutility.get_listoflist_s(terrain, [x - 1, y - 1, 1]))

        railway_N_CW_bool = railway_now + [railway_S[0], railway_W[1], railway_N[2]]

        railway_direc = hexcity.direction.N_CWbool_to_direction_symbol(railway_N_CW_bool)

        railway_map = hexcity.direction.railway_map(railway_N_CW_bool)

        line_map = hexcity.direction.line_map(river_now + [river_SW[0], river_W[1], river_NW[2]])

        tilegroup_railway_now = rw.tile.TileGroup_One.init_tilegroup_addlayer(
            hexcity.direction.railway_dict(city_occu_tile_name_180b, railway_direc), 
            hexcity.tgroup.tile_group_addlayer_item_hex28_32_railway.map(railway_map)
        )

        tilegroup_line = rw.tile.TileGroup_One.init_tilegroup_addlayer(
            hexcity.direction.line_dict(rw.frame.TagCoordinate.init_xy(city_occu_tile_name_180b, 4, 1), railway_direc), 
            hexcity.tgroup.tile_group_addlayer_ground_hex28_32_line.map(line_map)
        )

        pos_grid = pos_tile_layer(rw.frame.Coordinate(x, y), hex_topleft_origin_layer_tile)
        lukimap.addTile_group(tilegroup_railway_now, pos_grid)
        lukimap.addTile_group(tilegroup_line, pos_grid)
        #添加铁路

for x, terrain_y_list in enumerate(terrain):
    for y, terrain_now in enumerate(terrain_y_list):
        pos_grid = pos_tile_layer(rw.frame.Coordinate(x, y), city_origin_tile)
        lukimap.addTile_group(tilegroup_core_ground, pos_grid, isacce = True)
        lukimap.addTile_group(tilegroup_core_item, pos_grid, isacce = True)
        lukimap.addTile_group(tilegroup_core_itemsextra, pos_grid, isacce = True)
        #核心添加

lukimap.write_file(f'{current_dir_path}\\Velikie Luki 1942(basic map and ground)({RWMAP_GROUND_VERSION}).tmx')
# 输出地图到当前文件夹

maps_dir_path = "D:\\Game\\steam\\steamapps\\common\\Rusted Warfare\\mods\\maps"
lukimap.write_file(f'{maps_dir_path}\\Velikie Luki 1942(basic map and ground)({RWMAP_GROUND_VERSION}).tmx')
# 输出地图到游戏地图文件夹

