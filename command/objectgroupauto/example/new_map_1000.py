import os
import sys
example_dir_path = os.path.dirname(os.path.abspath(__file__))

package_dir_path = os.path.dirname(example_dir_path)

work_dir_path = os.path.dirname(package_dir_path)

sys.path.append(work_dir_path)
#这两项可以省略，如果pip安装（确定包的位置）

from copy import deepcopy
import numpy as np
import re
import pdb

import rwmap as rw

bb_map = rw.RWmap.init_mapfile(os.path.join(example_dir_path, "auto_example.tmx"))
map_x = 500
map_y = 800
map_now = rw.RWmap.init_map(rw.frame.Coordinate(map_y, map_x))

map_now.add_tileset_fromMapPath(f'{work_dir_path}\\examples\\template\\v3.tmx')
map_now.add_layer("Ground")
map_now.add_layer(rw.const.NAME.Items)
map_now.add_layer(rw.const.NAME.Units)

map_now.addTile_square(rw.frame.TagRectangle.init_ae("Ground", rw.frame.Coordinate(0, 0), rw.frame.Coordinate(map_x, map_y)), 
                       rw.frame.TagCoordinate.init_xy("export_ground", 7, 4))

red_x_list = [i for i in range(90, 100)] + [i for i in range(130, 140)] + [i for i in range(170, 180)] + [i for i in range(210, 220)]

for i in red_x_list:
    for j in range(map_y):
        map_now.addTile(rw.frame.TagCoordinate.init_xy("Ground", i, j), rw.frame.TagCoordinate.init_xy("export_ground", 25, 4))

red_y_list = [i for i in range(230, 240)] + [i for i in range(290, 300)] + [i for i in range(350, 360)]

for i in range(map_x):
    for j in red_y_list:
        map_now.addTile(rw.frame.TagCoordinate.init_xy("Ground", i, j), rw.frame.TagCoordinate.init_xy("export_ground", 25, 4))

map_now.addTile_square(rw.frame.TagRectangle.init_ae("Ground", rw.frame.Coordinate(140, 460), rw.frame.Coordinate(170, map_y)), 
                       rw.frame.TagCoordinate.init_xy("export_ground", 25, 4))

map_now._objectGroup_list = bb_map._objectGroup_list

map_now.write_file(os.path.join(example_dir_path, "auto_example.tmx"))


