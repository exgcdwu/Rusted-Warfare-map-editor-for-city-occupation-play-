import os
import sys
_current_dir_path = os.path.dirname(os.path.abspath(__file__))
_example_dir_path = os.path.dirname(_current_dir_path)
_package_dir = os.path.dirname(_example_dir_path)

sys.path.append(_package_dir)
#这两项可以省略，如果pip安装（确定包的位置）

sys.path.append(_current_dir_path)
# 地图数据文件

from copy import deepcopy
import numpy as np

import rwmap as rw
import sqrwmap as sqrw

import const
import version_var as var

from importlib import import_module
sys.path.append(const.basic_data_path)
bas = import_module(const.basic_data + "_" + str(var.basic_data_version))
sys.path.append(const.tile_group_data_path)
tgd = import_module(const.tile_group_data + "_" + str(var.tile_group_data_version))
sys.path.append(const.terrain_path)
terr = import_module(const.terrain + "_" + str(var.terrain_version))
sys.path.append(const.terrain_path)
terr = import_module(const.terrain + "_" + str(var.terrain_version))
sys.path.append(const.river_path)
terr = import_module(const.river + "_" + str(var.river_version))

sqmap_now = sqrw.SqRwmap(bas.square_size_tile, bas.map_size_square, bas.origin_square, 
                         const.map_process_dir_path, bas.layer_file, bas.map_file, form_str = bas.form_str, 
                         tile_size = bas.tile_size)

sqmap_now.add_tileset_fromMapPath_list(terr.template_file_list)

sqmap_now.add_terrain(terr.terrain, terr.terrain_dict, terr.terrain_offset)

sqmap_now.write_layer_path()