import os
import sys
from collections import OrderedDict
current_file_path = os.path.abspath(__file__)
current_dir_path = os.path.dirname(current_file_path)
auto_dir_path = os.path.dirname(current_dir_path)
package_dir = os.path.dirname(current_dir_path)
sys.path.append(package_dir)
import rwmap as rw

from auto._core import AUTOKEY
from auto._data._const import *

object_info_args_dict = OrderedDict()

object_info_args_dict[INFOKEY.prefix] = str
object_info_args_dict[INFOKEY.isprefixseg] = bool
object_info_args_dict[INFOKEY.objectType] = str
object_info_args_dict[INFOKEY.name] = str
object_info_args_dict[INFOKEY.offset] = (list, int)
object_info_args_dict[INFOKEY.offsetsize] = (list, int)
object_info_args_dict[INFOKEY.args] = (list, list, str)
object_info_args_dict[INFOKEY.opargs] = (list, list, str)
object_info_args_dict[INFOKEY.brace] = (list, str)

object_info_default_args_dict = {
    INFOKEY.offset: "0 0", 
    INFOKEY.offsetsize: "0 0"
}

object_info_optional_set = {INFOKEY.brace}

object_info_optional_set.add(INFOKEY.isprefixseg)
object_info_optional_set.add(INFOKEY.objectType)
object_info_optional_set.add(INFOKEY.name)
object_info_optional_set.add(INFOKEY.args)
object_info_optional_set.add(INFOKEY.opargs)

for key in OBJECT_ARGS_DICT.keys():
    if key.find("__") != -1:
        continue
    object_info_args_dict[key] = bool if OBJECT_ARGS_BOOL_DICT.get(key) != None else str
    object_info_optional_set.add(key)

ARGS_OPARGS_PRE_OPERATION = \
    operation_exist_if("args", "args_opargs_pre_if2") + \
        operation_cycle_start("i", "0", "i < len(args)", "args_opargs_pre_cycle1") + \
            [
                {
                    AUTOKEY.operation_type: AUTOKEY.typeadd_optional, 
                    AUTOKEY.nameadd_optional: "[args[i][0]]"
                }, 
                {
                    AUTOKEY.operation_type: AUTOKEY.typeadd_args, 
                    "{args[i][0]}": "args[i][1]"
                }
            ] + \
        operation_cycle_end("i", "i + 1", "args_opargs_pre_cycle1") + \
    operation_ifend("args_opargs_pre_if2") + \
    operation_exist_if("opargs", "args_opargs_pre_if3") + \
        operation_cycle_start("i", "0", "i < len(opargs)", "args_opargs_pre_cycle2") + \
            operation_if("len(opargs[i]) == 3", "args_opargs_pre_if1") + \
                [
                    {
                        AUTOKEY.operation_type: AUTOKEY.typeadd_opargs, 
                        "{opargs[i][0]}": "(opargs[i][1], opargs[i][2])"
                    }
                ] + \
            operation_else("args_opargs_pre_if1") + \
                [
                    {
                        AUTOKEY.operation_type: AUTOKEY.typeadd_opargs, 
                        "{opargs[i][0]}": "(opargs[i][1] + \'|\' + opargs[i][3], opargs[i][2])"
                    }
                ] + \
            operation_elseend("args_opargs_pre_if1") + \
        operation_cycle_end("i", "i + 1", "args_opargs_pre_cycle2") + \
    operation_ifend("args_opargs_pre_if3")

object_info_operation_pre_list = ARGS_OPARGS_PRE_OPERATION

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
    ] + \
    BRACE_OPERATION_END

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