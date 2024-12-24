import os
import sys
from collections import OrderedDict
current_file_path = os.path.abspath(__file__)
current_dir_path = os.path.dirname(current_file_path)
auto_dir_path = os.path.dirname(current_dir_path)
package_dir = os.path.dirname(auto_dir_path)
sys.path.append(package_dir)
import rwmap as rw

from command.objectgroupauto._core import AUTOKEY
from command.objectgroupauto._data._const import *
from command.objectgroupauto._data._object import *
from command.objectgroupauto._data._multiText import *

tree_info_args_dict = OrderedDict()

tree_info_args_dict[INFOKEY.prefix] = str
tree_info_args_dict[INFOKEY.cite_name] = str
tree_info_args_dict[INFOKEY.name] = (list, list, str)
tree_info_args_dict[INFOKEY.exist] = (list, str)
tree_info_args_dict[INFOKEY.offset] = (list, list, int)
tree_info_args_dict[INFOKEY.offsetsize] = (list, list, int)
tree_info_args_dict[INFOKEY.idprefix] = (list, list, str)
tree_info_args_dict[INFOKEY.isprefixseg] = bool

tree_info_default_args_dict = {
    INFOKEY.offset: "0 0", 
    INFOKEY.offsetsize: "0 0", 
    INFOKEY.exist: "true"
}

tree_info_optional_set = {
    INFOKEY.cite_name, INFOKEY.idprefix, 
    INFOKEY.isprefixseg
}

IDPREFIX_PRE_OPERATION = \
    operation_exist_if(INFOKEY.idprefix, "idprefix_pre_if_1") + \
        operation_cycle_start("i", "0", "i < len(idprefix)", "idprefix_pre_cycle_1") + \
        [
            {
                AUTOKEY.operation_type: AUTOKEY.typeset_id, 
                f"{INFOKEY.idprefix}" + "{i}_": "{" + f"{INFOKEY.idprefix}" + "[i][1]}",  
                AUTOKEY.real_idexp: "{" + f"{INFOKEY.idprefix}" + "[i][0]}"
            }, 
        ] + \
        operation_cycle_end("i", "i + 1", "idprefix_pre_cycle_1") + \
    operation_ifend("idprefix_pre_if_1")

tree_info_operation_pre_list = IDPREFIX_PRE_OPERATION

def bool_list_operation_list(key:str):
    return operation_typeset_expression(f"{key}", f"[True if operation_key == 'true' else operation_key for operation_key in {key}]")

tree_info_operation_list = \
    bool_list_operation_list("exist") + \
    operation_exist_if("name", "tree_operation_if_1") + \
        operation_cycle_start("i", "0", "i < len(name)", "tree_operation_cycle_1") + \
            operation_list_assign(f"{INFOKEY.offset}", "i", "offset_now", "tree", "[0, 0]") + \
            operation_list_assign(f"{INFOKEY.offsetsize}", "i", "offsetsize_now", "tree", "[0, 0]") + \
            operation_list_assign(f"{INFOKEY.exist}", "i", "exist_now", "tree", "True") + \
            operation_if("exist_now_{i}", "tree_operation_if_exist_now") + \
                [
                    {
                        AUTOKEY.operation_type: AUTOKEY.object, 
                        AUTOKEY.offset: "offset_now_{i}", 
                        AUTOKEY.offsetsize: "offsetsize_now_{i}", 
                        AUTOKEY.name: "{','.join(name[i])}&12"
                    }
                ] + \
            operation_ifend("tree_operation_if_exist_now") + \
        operation_cycle_end("i", "i + 1", "tree_operation_cycle_1") + \
    operation_ifend("tree_operation_if_1")

tree_info = {
    INFOKEY.tree_info:{
        AUTOKEY.info_args:tree_info_args_dict, 
        AUTOKEY.default_args: tree_info_default_args_dict, 
        AUTOKEY.optional:tree_info_optional_set, 
        AUTOKEY.ids: [], 
        AUTOKEY.args: [], 
        AUTOKEY.seg: ".", 
        AUTOKEY.opargs_prefix_len:1, 
        AUTOKEY.opargs: {}, 
        AUTOKEY.opargs_seg: ",", 
        AUTOKEY.prefix: AUTOKEY.prefix, 
        AUTOKEY.isprefixseg: AUTOKEY.isprefixseg, 
        AUTOKEY.operation_pre: tree_info_operation_pre_list, 
        AUTOKEY.operation:tree_info_operation_list, 
        AUTOKEY.no_check: True
    }
}

tree_info = brace_add_info(tree_info)
tree_info = args_opargs_add_info(tree_info)