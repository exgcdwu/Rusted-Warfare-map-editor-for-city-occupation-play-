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
from command.objectgroupauto._data._const import *
from command.objectgroupauto._data._time import time_info_sub

object_info_args_dict = OrderedDict()

object_info_args_dict[INFOKEY.prefix] = str
object_info_args_dict[INFOKEY.isprefixseg] = bool
object_info_args_dict[INFOKEY.objectType] = str
object_info_args_dict[INFOKEY.name] = str
object_info_args_dict[INFOKEY.offset] = (list, int)
object_info_args_dict[INFOKEY.offsetsize] = (list, int)

object_info_default_args_dict = {
    INFOKEY.offset: "0 0", 
    INFOKEY.offsetsize: "0 0"
}

object_info_optional_set = set()

object_info_optional_set.add(INFOKEY.isprefixseg)
object_info_optional_set.add(INFOKEY.objectType)
object_info_optional_set.add(INFOKEY.name)

for key in OBJECT_ARGS_DICT.keys():
    if key.find("__") != -1:
        continue
    object_info_args_dict[key] = bool if OBJECT_ARGS_BOOL_DICT.get(key) != None else str
    object_info_optional_set.add(key)

object_info_operation_pre_list = []

object_info_operation_list_optional = {}

for key in OBJECT_ARGS_DICT.keys():
    if key.find("__") != -1:
        continue
    if OBJECT_ARGS_BOOL_DICT.get(key) != None:
        object_info_operation_list_optional[key] = ("{" + f"{key}" + "}", key, AUTOKEY.brace)
    else:
        object_info_operation_list_optional[key] = ("{" + f"{key}" + "}", key, AUTOKEY.exist)


object_info_operation_list = \
    [
        {
            AUTOKEY.operation_type: AUTOKEY.object, 
            AUTOKEY.offset: INFOKEY.offset, 
            AUTOKEY.offsetsize: INFOKEY.offsetsize,                 
            AUTOKEY.name: ("{" + f"{INFOKEY.name}" + "}", AUTOKEY.name, AUTOKEY.exist), 
            AUTOKEY.type: ("{" + f"{INFOKEY.objectType}" + "}", INFOKEY.objectType, AUTOKEY.exist), 
            AUTOKEY.optional: object_info_operation_list_optional
        }, 
    ]

object_info = {
    INFOKEY.object_info:{
        AUTOKEY.info_args:object_info_args_dict, 
        AUTOKEY.default_args: object_info_default_args_dict, 
        AUTOKEY.prefix: AUTOKEY.prefix, 
        AUTOKEY.isprefixseg: AUTOKEY.isprefixseg, 
        AUTOKEY.args: [], 
        AUTOKEY.seg: ".", 
        AUTOKEY.opargs_prefix_len:1, 
        AUTOKEY.opargs: {}, 
        AUTOKEY.opargs_seg: ",", 
        AUTOKEY.optional:object_info_optional_set, 
        AUTOKEY.operation_pre:object_info_operation_pre_list, 
        AUTOKEY.operation:object_info_operation_list, 
        AUTOKEY.no_check: True
    }
}

object_info = time_info_sub(object_info, [rw.const.OBJECTOP.warmup, rw.const.OBJECTOP.delay], [], 
                            [rw.const.OBJECTOP.repeatDelay, rw.const.OBJECTOP.resetActivationAfter], [])
object_info = brace_add_info(object_info)
object_info = args_opargs_add_info(object_info)