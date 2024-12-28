import os
import sys
current_dir_path = os.path.dirname(os.path.abspath(__file__))
example_dir_path = os.path.dirname(current_dir_path)

package_dir = os.path.dirname(example_dir_path)
sys.path.append(package_dir)
#这两项可以省略，如果pip安装（确定包的位置）

import rwmap as rw

rwmap_output_path = "./examples/sixsquare/sixsq2p.tmx"
rwmap_input_path = "D:\Game\steam\steamapps\common\Rusted Warfare\mods\maps\六边包围战【2p,包围机制城市争夺玩法】(V.1.1)_by咕咕咕.tmx"

rwmap_now = rw.RWmap.init_mapfile(rwmap_input_path)
rwmap_now.write_file(rwmap_output_path)

rwmap_now = rw.RWmap.init_mapfile(rwmap_output_path)