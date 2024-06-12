import os
import sys
_current_dir_path = os.path.dirname(os.path.abspath(__file__))
_project_dir_path = os.path.dirname(_current_dir_path)
_example_dir_path = os.path.dirname(_project_dir_path)
_package_dir = os.path.dirname(_example_dir_path)

sys.path.append(_package_dir)
#这两项可以省略，如果pip安装（确定包的位置）

from copy import deepcopy
import numpy as np
import rwmap as rw

import version_var as var

VERSION = 1
form_str = "hex_x"
origin_square = rw.frame.Coordinate(0.5, -0.5, dtype = np.float32)
tile_size = rw.const.COO.SIZE_STANDARD
square_size_tile = rw.frame.Coordinate(28, 24)
map_size_square = rw.frame.Coordinate(17, 5)

#row

_map_name = "反攻大卢基(1942.11.8-1943.1.9)【4p,城夺战役模式】"
_layer_version = f"(V.{var.basic_data_version}.{var.tile_group_data_version}.{var.terrain_version}"
_map_version = _layer_version
_version_n = ")"
_layer_tag = "(仅底图)" 
_prefix_tmx = ".tmx"

# process

layer_file = _map_name + _layer_version + _version_n + _layer_tag + _prefix_tmx
map_file = _map_name + _map_version + _version_n + _prefix_tmx