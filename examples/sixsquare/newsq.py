import os
import sys
current_dir_path = os.path.dirname(os.path.abspath(__file__))
example_dir_path = os.path.dirname(current_dir_path)

package_dir = os.path.dirname(example_dir_path)
sys.path.append(package_dir)
#这两项可以省略，如果pip安装（确定包的位置）

import rwmap as rw

rwmap_input_path = "D:\Game\steam\steamapps\common\Rusted Warfare\mods\maps\六边包围战【2p,包围城夺】(V.1.3)_by咕咕咕.tmx"
rwmap_output_path = "D:\Game\steam\steamapps\common\Rusted Warfare\mods\maps\六边包围战【2p,包围城夺】(V.1.12)_by咕咕咕.tmx"

rwmap_input = rw.RWmap.init_mapfile(rwmap_input_path)
rwmap_output = rw.RWmap.init_mapfile(rwmap_output_path)
rwmap_output.add_Layer_fromLayer_replace(rwmap_input.get_layer_s("Ground"))
rwmap_output.write_file(rwmap_output_path)