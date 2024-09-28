import os
import sys
current_dir_path = os.path.dirname(os.path.abspath(__file__))
example_dir_path = os.path.dirname(current_dir_path)

package_dir_path = os.path.dirname(example_dir_path)

work_dir_path = os.path.dirname(package_dir_path)

sys.path.append(work_dir_path)
#这两项可以省略，如果pip安装（确定包的位置）

from copy import deepcopy
import numpy as np
import re
import pdb

import rwmap as rw

bb_map = rw.RWmap.init_mapfile(f'{current_dir_path}\\' + "new_example.tmx")

map_now = rw.RWmap.init_map(rw.frame.Coordinate(400, 400))

map_now.add_tileset_fromMapPath(f'{work_dir_path}\\examples\\template\\v3.tmx')
map_now.add_layer("Ground")
map_now.add_layer(rw.const.NAME.Items)
map_now.add_layer(rw.const.NAME.Units)
for i in range(400):
    for j in range(400):
        map_now.addTile(rw.frame.TagCoordinate.init_xy("Ground", i, j), rw.frame.TagCoordinate.init_xy("export_ground", 7, 4))

red_list = [i for i in range(300) if (i % 100 >= 90)] + [i for i in range(300, 400)]

for i in red_list:
    for j in range(400):
        map_now.addTile(rw.frame.TagCoordinate.init_xy("Ground", i, j), rw.frame.TagCoordinate.init_xy("export_ground", 25, 4))

map_now._objectGroup_list = bb_map._objectGroup_list

map_now.write_file(f'{current_dir_path}\\' + "new_example.tmx")