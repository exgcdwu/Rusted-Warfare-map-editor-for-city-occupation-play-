import os
import sys
current_dir_path = os.path.dirname(os.path.abspath(__file__))
great_war_dir_path = os.path.dirname(current_dir_path)
example_dir_path = os.path.dirname(great_war_dir_path)

package_dir = os.path.dirname(example_dir_path)
sys.path.append(package_dir)
#这两项可以省略，如果pip安装（确定包的位置）

sys.path.append(great_war_dir_path)
#hexcity 包位置

sys.path.append(current_dir_path)
# 地图数据文件

from copy import deepcopy
import numpy as np

import rwmap as rw
import hexcity
from Velikie_Luki_1942_data_1_0_1_0 import *

lukimap = rw.RWmap.init_map(map_size_tile, tile_size = tile_size)
# 反攻大卢基空地图 
lukimap.add_tileset_fromMapPath(f'{example_dir_path}\\template\\v3.tmx')
# 添加V3模板地块集
lukimap.add_tileset_fromMapPath(f'{example_dir_path}\\template\\city occupation(tile property).tmx')
# 添加城夺地块集
lukimap.write_png(f'{current_dir_path}')
# 将地块集图片全部输出，以便使用Tiled观看

print(lukimap.tileset_name_list())
# 显示地块集名称

lukimap.add_layer(rw.const.NAME.Ground)
lukimap.add_layer(rw.const.NAME.Units)
lukimap.add_layer(rw.const.NAME.Items)
lukimap.add_layer(rw.const.NAME.PathingOverride)
#lukimap.get_layer_s(rw.const.NAME.ItemsExtra).change_opacity(0)
lukimap.add_objectgroup(rw.const.NAME.Triggers)
# 添加图层和地块层


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
        pos_grid = pos_tile_layer(rw.frame.Coordinate(x, y))
        lukimap.addTile_group(tilegroup_now, pos_grid + hex_topleft_origin_layer_tile, isacce = True)
        lukimap.addTile_group(rw.tile.TileGroup_One.init_tilegroup_addlayer(
            {"p": terrain_p[terrain[x][y][0]]}, tilegroup_core_expand0[0]), 
            pos_grid + tilegroup_core_expand0[1])
        # 添加地形

for name, value in city.items():
    city_name = value[0]
    city_level = value[1]
    city_fort_level = value[2]
    city_victory = value[3]
    x = name[0]
    y = name[1]
    pos_grid = pos_tile_layer(rw.frame.Coordinate(x, y))
    tilegroup_now =  tilegroup_core_expand(1)
    if city_name != '':
        lukimap.addTile_group(rw.tile.TileGroup_One.init_tilegroup_addlayer(
            {"p": terrain_p[terrain[x][y][0]]}, tilegroup_core_expand1[0]), 
            pos_grid + tilegroup_core_expand1[1])
    #地形中央扩展（城市）



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
            hexcity.direction.line_dict(line_tile, railway_direc), 
            hexcity.tgroup.tile_group_addlayer_ground_hex28_32_line.map(line_map)
        )

        pos_grid = pos_tile_layer(rw.frame.Coordinate(x, y))
        lukimap.addTile_group(tilegroup_railway_now, pos_grid + hex_topleft_origin_layer_tile)
        lukimap.addTile_group(tilegroup_line, pos_grid + hex_topleft_origin_layer_tile)
        if sum(railway_N_CW_bool) != 0:
            lukimap.addTile_group(tilegroup_core_ground2, pos_grid + city_origin_layer_tile)

        #添加铁路

lukimap.write_file(f'{current_dir_path}\\Velikie Luki 1942(basic map and ground)({RWMAP_GROUND_VERSION}).tmx')
# 输出地图到当前文件夹

maps_dir_path = "D:\\Game\\steam\\steamapps\\common\\Rusted Warfare\\mods\\maps"
lukimap.write_file(f'{maps_dir_path}\\Velikie Luki 1942(basic map and ground)({RWMAP_GROUND_VERSION}).tmx')
# 输出地图到游戏地图文件夹

