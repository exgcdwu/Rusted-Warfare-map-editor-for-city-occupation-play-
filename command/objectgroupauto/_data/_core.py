import os
import sys
from collections import OrderedDict
current_file_path = os.path.abspath(__file__)
current_dir_path = os.path.dirname(current_file_path)
auto_dir_path = os.path.dirname(current_dir_path)
package_dir = os.path.dirname(current_dir_path)
sys.path.append(package_dir)
import rwmap as rw

from command.objectgroupauto._core import AUTOKEY
from command.objectgroupauto._data._object import object_info
from command.objectgroupauto._data._teamDetect import teamDetect_info
from command.objectgroupauto._data._multiText import multiText_info
from command.objectgroupauto._data._mtext import mtext_info
from command.objectgroupauto._data._inadd import inadd_info
from command.objectgroupauto._data._building import building_info
from command.objectgroupauto._data._numDetect import numDetect_info
from command.objectgroupauto._data._dictionary import dictionary_info
from command.objectgroupauto._data._multiRemove import multiRemove_info
from command.objectgroupauto._data._tree import tree_info
from command.objectgroupauto._data._multiAdd import multiAdd_info
from command.objectgroupauto._data._flash import flash_info
from command.objectgroupauto._data._idcheck import idcheck_info
from command.objectgroupauto._data._time import time_info
from command.objectgroupauto._data._step import step_info

auto_func_arg = {}
auto_func_arg.update(object_info)
auto_func_arg.update(teamDetect_info)
auto_func_arg.update(numDetect_info)
auto_func_arg.update(multiText_info)
auto_func_arg.update(mtext_info)
auto_func_arg.update(inadd_info)
auto_func_arg.update(building_info)
auto_func_arg.update(dictionary_info)
auto_func_arg.update(multiRemove_info)
auto_func_arg.update(tree_info)
auto_func_arg.update(multiAdd_info)
auto_func_arg.update(flash_info)
auto_func_arg.update(idcheck_info)
auto_func_arg.update(time_info)
auto_func_arg.update(step_info)