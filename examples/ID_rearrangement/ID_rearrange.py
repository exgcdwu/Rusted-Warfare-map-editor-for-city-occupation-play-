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

dir = "D:\Game\steam\steamapps\common\Rusted Warfare\mods\maps\\"

name = "export.tmx"

output_name = name[:-4] + "-resetID.tmx"

map_now:rw.RWmap = rw.RWmap.init_mapfile(dir + name)

map_now.resetid()

map_now.write_file(dir + output_name)

