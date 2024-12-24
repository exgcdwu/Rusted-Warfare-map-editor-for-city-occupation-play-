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

numDetect_info_args_dict = OrderedDict()

numDetect_info_args_dict[INFOKEY.prefix] = str
numDetect_info_args_dict[INFOKEY.isprefixseg] = bool
numDetect_info_args_dict[INFOKEY.reset] = str
numDetect_info_args_dict[INFOKEY.setNum] = (list, list, int)
numDetect_info_args_dict[INFOKEY.setidNum] = (list, str)

numDetect_info_args_dict[INFOKEY.team] = str
numDetect_info_args_dict[INFOKEY.aunit] = str
numDetect_info_args_dict[INFOKEY.name] = (list, str)
numDetect_info_args_dict[INFOKEY.offset] = (list, list, int)
numDetect_info_args_dict[INFOKEY.offsetsize] = (list, list, int)

numDetect_info_args_dict[INFOKEY.cite_name] = str

DETECT_OPTION_DICT = {
    OBJECT_ARGS.onlyIdle:bool, 
    OBJECT_ARGS.onlyBuildings:bool, 
    OBJECT_ARGS.onlyMainBuildings:bool, 
    OBJECT_ARGS.onlyEmptyQueue:bool, 
    OBJECT_ARGS.onlyBuilders:bool, 
    OBJECT_ARGS.onlyOnResourcePool:bool, 
    OBJECT_ARGS.onlyAttack:bool, 
    OBJECT_ARGS.onlyAttackAir:bool, 
    OBJECT_ARGS.onlyTechLevel:str, 
    OBJECT_ARGS.includeIncomplete:bool, 
    OBJECT_ARGS.onlyWithTag:str
}
numDetect_info_args_dict.update(DETECT_OPTION_DICT)

numDetect_info_default_args_dict = {
    INFOKEY.name: "[\"{'setid\" + \"Num\" + str(ex) + \"_0'[len(setidNum[ex]):]}\" " + f"for ex in range({INFOKEY.lenidNum})]", 
    INFOKEY.offset: f"[[0, 0] for ex in range({INFOKEY.lenidNum})]", 
    INFOKEY.offsetsize: f"[[0, 0] for ex in range({INFOKEY.lenidNum})]"
}

numDetect_info_optional_set = set()

numDetect_info_optional_set.add(INFOKEY.isprefixseg)
numDetect_info_optional_set.add(INFOKEY.aunit)
numDetect_info_optional_set.add(INFOKEY.team)
numDetect_info_optional_set.add(INFOKEY.cite_name)
DETECT_OPTION_SET = set(DETECT_OPTION_DICT.keys())
numDetect_info_optional_set.update(DETECT_OPTION_SET)

numDetect_info_var_dependent_dict = {}

numDetect_info_initial_brace_dict = {
    f"{INFOKEY.lenidNum}": f"len({INFOKEY.setidNum})"
}

numDetect_info_default_brace_set = {
    f"{INFOKEY.name}", 
    f"{INFOKEY.offset}", 
    f"{INFOKEY.offsetsize}"
}

numDetect_info_operation_pre_list = \
    operation_cycle_start("i", "0", f"i < {INFOKEY.lenidNum}", "numDetect_pre_cycle1") + \
        [
            {
                AUTOKEY.operation_type: AUTOKEY.typeset_id, 
                f"{INFOKEY.setidNum}" + "{i}_": "1", 
                AUTOKEY.real_idexp: "{" + f"{INFOKEY.setidNum}" + "[i]}"
            }, 
        ] + \
    operation_cycle_end("i", "i + 1", "numDetect_pre_cycle1")

DETECT_OPTION_OPERATION_OPTIONAL = {DETECT_KEY:(True, DETECT_KEY, AUTOKEY.brace) if DEFECT_VALUE == bool else ("{" + DETECT_KEY + "}", DETECT_KEY, AUTOKEY.exist) for DETECT_KEY, DEFECT_VALUE in DETECT_OPTION_DICT.items()}

numDetect_info_operation_optional = {
    rw.const.OBJECTOP.id: "{id_now}", 
    rw.const.OBJECTOP.alsoActivate: "{id_now}", 
    rw.const.OBJECTOP.minUnits: ("{minUnits_now}", "minUnits_exist", AUTOKEY.brace), 
    rw.const.OBJECTOP.maxUnits: ("{maxUnits_now}", "maxUnits_exist", AUTOKEY.brace), 
    rw.const.OBJECTOP.resetActivationAfter: "{" + INFOKEY.reset + "}", 
    rw.const.OBJECTOP.unitType: ("{" + f"{INFOKEY.aunit}" + "}", INFOKEY.aunit, AUTOKEY.exist), 
    rw.const.OBJECTOP.team: ("{" + f"{INFOKEY.team}" + "}", "team", AUTOKEY.exist)
}
numDetect_info_operation_optional.update(DETECT_OPTION_OPERATION_OPTIONAL)

numDetect_info_operation_list = \
    operation_cycle_start("i", "0", f"i < {INFOKEY.lenidNum}", "numDetect_cycle1") + \
        operation_cycle_start("j", "0", f"(2 * j + 1) < len({INFOKEY.setNum}[i])", "numDetect_cycle2") + \
            [
                {
                    AUTOKEY.operation_type:AUTOKEY.typeset_expression, 
                    "id_now": f"{INFOKEY.setidNum}" + "{i}_0"
                }, 
            ] + \
            [
                {
                    AUTOKEY.operation_type:AUTOKEY.typeset_expression, 
                    "minUnits_now": f"{INFOKEY.setNum}" + "[i][2 * j]"
                }, 
            ] + \
            operation_if("minUnits_now <= 0", "numDetect_if_minUnits_remove") + \
                operation_typeset_expression("minUnits_exist", "False") + \
            operation_else("numDetect_if_minUnits_remove") + \
                operation_typeset_expression("minUnits_exist", "True") + \
            operation_elseend("numDetect_if_minUnits_remove") + \
            [
                {
                    AUTOKEY.operation_type:AUTOKEY.typeset_expression, 
                    "maxUnits_now": f"{INFOKEY.setNum}" + "[i][2 * j + 1]"
                }, 
            ] + \
            operation_if("maxUnits_now >= 65536", "numDetect_if_maxUnits_remove") + \
                operation_typeset_expression("maxUnits_exist", "False") + \
            operation_else("numDetect_if_maxUnits_remove") + \
                operation_typeset_expression("maxUnits_exist", "True") + \
            operation_elseend("numDetect_if_maxUnits_remove") + \
            [
                {
                    AUTOKEY.operation_type:AUTOKEY.typeset_expression, 
                    "id_now": f"{INFOKEY.setidNum}" + "{i}_0"
                }, 
            ] + \
            operation_if(f"len({INFOKEY.name}) != 1", "numDetect_if2") + \
                [
                    {
                        AUTOKEY.operation_type:AUTOKEY.typeset_expression, 
                        "name_now": f"{INFOKEY.name}[i]"
                    }
                ] + \
            operation_else("numDetect_if2") + \
                [
                    {
                        AUTOKEY.operation_type:AUTOKEY.typeset_expression, 
                        "name_now": f"{INFOKEY.name}[0]"
                    }
                ] + \
            operation_elseend("numDetect_if2") + \
            operation_if(f"len({INFOKEY.offset}) != 1", "numDetect_if3") + \
                [
                    {
                        AUTOKEY.operation_type:AUTOKEY.typeset_expression, 
                        "offset_now": f"{INFOKEY.offset}[i]"
                    }
                ] + \
            operation_else("numDetect_if3") + \
                [
                    {
                        AUTOKEY.operation_type:AUTOKEY.typeset_expression, 
                        "offset_now": f"{INFOKEY.offset}[0]"
                    }
                ] + \
            operation_elseend("numDetect_if3") + \
            operation_if(f"len({INFOKEY.offsetsize}) != 1", "numDetect_if4") + \
                [
                    {
                        AUTOKEY.operation_type:AUTOKEY.typeset_expression, 
                        "offsetsize_now": f"{INFOKEY.offsetsize}[i]"
                    }
                ] + \
            operation_else("numDetect_if4") + \
                [
                    {
                        AUTOKEY.operation_type:AUTOKEY.typeset_expression, 
                        "offsetsize_now": f"{INFOKEY.offsetsize}[0]"
                    }
                ] + \
            operation_elseend("numDetect_if4") + \
            [
                {
                    AUTOKEY.operation_type: AUTOKEY.object, 
                    AUTOKEY.offset: "offset_now", 
                    AUTOKEY.offsetsize: "offsetsize_now", 
                    AUTOKEY.name: ("{name_now}", "j == 0", AUTOKEY.brace), 
                    AUTOKEY.type: rw.const.OBJECTTYPE.unitDetect, 
                    AUTOKEY.optional: numDetect_info_operation_optional
                }

            ] + \
        operation_cycle_end("j", "j + 1", "numDetect_cycle2") + \
    operation_cycle_end("i", "i + 1", "numDetect_cycle1")


numDetect_info = {
    INFOKEY.numDetect_info:{
        AUTOKEY.info_args:numDetect_info_args_dict, 
        AUTOKEY.default_args: numDetect_info_default_args_dict, 
        AUTOKEY.var_dependent: numDetect_info_var_dependent_dict, 
        AUTOKEY.optional:numDetect_info_optional_set, 
        AUTOKEY.initial_brace: numDetect_info_initial_brace_dict, 
        AUTOKEY.default_brace: numDetect_info_default_brace_set, 

        AUTOKEY.ids: [], 
        AUTOKEY.prefix: AUTOKEY.prefix, 
        AUTOKEY.isprefixseg: AUTOKEY.isprefixseg, 
        AUTOKEY.args: [], 
        AUTOKEY.seg: ".", 
        AUTOKEY.opargs_prefix_len:1, 
        AUTOKEY.opargs: {}, 
        AUTOKEY.opargs_seg: ",", 
        AUTOKEY.operation_pre:numDetect_info_operation_pre_list, 
        AUTOKEY.operation:numDetect_info_operation_list, 
        AUTOKEY.no_check: True
    }
}

numDetect_info = brace_add_info(numDetect_info)
numDetect_info = args_opargs_add_info(numDetect_info)