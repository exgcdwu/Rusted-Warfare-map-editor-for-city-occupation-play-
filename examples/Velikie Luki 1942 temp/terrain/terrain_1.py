import os
import sys
_current_dir_path = os.path.dirname(os.path.abspath(__file__))
_project_dir_path = os.path.dirname(_current_dir_path)
_example_dir_path = os.path.dirname(_project_dir_path)
_package_dir = os.path.dirname(_example_dir_path)


sys.path.append(_package_dir)
#这两项可以省略，如果pip安装（确定包的位置）

sys.path.append(_current_dir_path)
# 地图数据文件

from copy import deepcopy
import numpy as np

import rwmap as rw

import const
import version_var as var

from importlib import import_module
sys.path.append(const.tile_group_data_path)
tgroup = import_module(const.tile_group_data + "_" + str(var.tile_group_data_version))

VERSION = 1
terrain_offset = rw.frame.Coordinate(-14, -16)

terrain = [
    ["s", "w"], 
    ["s", "w", "w", "p", "s"], 
    ["w", "w", "w", "p", "w", "s"], 
    ["p", "w", "p", "p", "p", "s", "s"],  
    ["s", "w", "c", "w", "w", "p", "p"], 
    ["w", "p", "p", "p", "w", "c", "w"], 
    ["s", "p", "p", "p", "w", "w", "w"], 
    ["w", "s", "p", "p", "p", "p", "p"], 
    ["w", "s", "p", "p", "p", "s", "p"], 
    ["w", "p", "p", "p", "s", "s", "w"], 
    ["s", "w", "p", "p", "p", "s", "w"], 
    ["w", "w", "p", "p", "w", "s", "s"], 
    ["w", "w", "c", "p", "p", "w", "w"], 
    ["s", "p", "c", "w", "w", "w", "w"],
    ["w", "p", "w", "w", "c", "w", "w"],
    ["w", "p", "w", "w", "w", "w", "w"],
    ["p", "p", "p", "p", "w", "w", "c"],
    ["e", "w", "w", "w", "w", "w", "w"],
    ["e", "e", "e", "w", "w", "w", "w"],
    ["e", "e", "e", "e", "e", "w", "w"],
]

# row

template_file_list = [
    "v3.tmx", 
    "city occupation(tile property).tmx"
]

_export_ground = "export_ground"

_city_occu_tile_name_180b = "巴巴罗萨计划（1.80beta版）地块byXs"
_city_occu_tile_name_160b = "巴巴罗萨计划（1.60beta版）地块byXs"
_city_occu_tile_name_150 = "巴巴罗萨计划（1.50版）地块byXs"
_city_occu_tile_name_B3 = "巴巴罗萨计划（B3版）地块byXs"
_city_occu_sup_tile_name_12 = '辅助地块（1.2版）byXs'

_terrain_b = {
    "w": rw.frame.TagCoordinate.init_xy(_export_ground, 13, 7), 
    "s": rw.frame.TagCoordinate.init_xy(_city_occu_tile_name_150, 5, 3), 
    "p": rw.frame.TagCoordinate.init_xy(_city_occu_tile_name_180b, 5, 5), 
    "c": rw.frame.TagCoordinate.init_xy(_city_occu_tile_name_B3, 6, 2)
}
_terrain_p = {
    "w": rw.frame.TagCoordinate.init_xy(_city_occu_tile_name_160b, 4, 1), 
    "s": rw.frame.TagCoordinate.init_xy(_city_occu_tile_name_150, 4, 3), 
    "p": rw.frame.TagCoordinate.init_xy(_city_occu_tile_name_180b, 4, 4), 
    "c": rw.frame.TagCoordinate.init_xy(_city_occu_tile_name_B3, 4, 1)
}

# process

_tilegroup_wood = rw.tile.TileGroup_List.init_tilegroup_list(
    [  
        rw.tile.TileGroup_One.init_tilegroup_addlayer(
            {
                "b": _terrain_b["w"], 
                "p": _terrain_p["w"]
            }, 
            tgroup.tile_group_addlayer_ground_hex28_32_fill_barrier_terrain
        )
    ]
)
# 树林地块组

_tilegroup_swamp = rw.tile.TileGroup_List.init_tilegroup_list(
    [  
        rw.tile.TileGroup_One.init_tilegroup_addlayer(
            {
                "b": _terrain_b["s"], 
                "p": _terrain_p["s"]
            }, 
            tgroup.tile_group_addlayer_ground_hex28_32_fill_barrier_terrain
        )
    ]
)
# 沼泽地块组

_tilegroup_plane = rw.tile.TileGroup_List.init_tilegroup_list(
    [  
        rw.tile.TileGroup_One.init_tilegroup_addlayer(
            {
                "b": _terrain_b["p"], 
                "p": _terrain_p["p"]
            }, 
            tgroup.tile_group_addlayer_ground_hex28_32_fill_light_barrier
        )
    ]
)
# 平原地块组

_tilegroup_cliff = rw.tile.TileGroup_List.init_tilegroup_list(
    [  
        rw.tile.TileGroup_One.init_tilegroup_addlayer(
            {
                "b": _terrain_b["c"], 
                "p": _terrain_p["c"]
            }, 
            tgroup.tile_group_addlayer_ground_hex28_32_fill_barrier_terrain
        )
    ]
)
# 山脉地块组

# process end

for i in range(len(template_file_list)):
    template_file_list[i] = const.template_dir_path + "\\" + template_file_list[i]

terrain_dict = {
    "w": _tilegroup_wood, 
    "c": _tilegroup_cliff, 
    "s": _tilegroup_swamp, 
    "p": _tilegroup_plane, 
}

