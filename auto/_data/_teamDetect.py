import os
import sys
from collections import OrderedDict
current_file_path = os.path.abspath(__file__)
current_dir_path = os.path.dirname(current_file_path)
auto_dir_path = os.path.dirname(current_dir_path)
package_dir = os.path.dirname(auto_dir_path)
sys.path.append(package_dir)
import rwmap as rw

from auto._core import AUTOKEY
from auto._data._const import *
from auto._data._object import *

teamDetect_info_args_dict = OrderedDict()

teamDetect_info_args_dict[INFOKEY.prefix] = str
teamDetect_info_args_dict[INFOKEY.isprefixseg] = bool
teamDetect_info_args_dict[INFOKEY.reset] = str
teamDetect_info_args_dict[INFOKEY.setTeam] = (list, list, int)
teamDetect_info_args_dict[INFOKEY.setidTeam] = (list, str)

teamDetect_info_args_dict[INFOKEY.minUnits] = str
teamDetect_info_args_dict[INFOKEY.maxUnits] = str

teamDetect_info_args_dict[INFOKEY.unit] = str
teamDetect_info_args_dict[INFOKEY.name] = (list, str)
teamDetect_info_args_dict[INFOKEY.offset] = (list, list, int)
teamDetect_info_args_dict[INFOKEY.offsetsize] = (list, list, int)

teamDetect_info_args_dict[INFOKEY.cite_name] = str

teamDetect_info_args_dict[INFOKEY.args] = (list, list, str)
teamDetect_info_args_dict[INFOKEY.opargs] = (list, list, str)
teamDetect_info_args_dict[INFOKEY.brace] = (list, str)

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
teamDetect_info_args_dict.update(DETECT_OPTION_DICT)

teamDetect_info_default_args_dict = {
    INFOKEY.minUnits: "1", 
    INFOKEY.name: "" + "[\"{'setid\" + \"Team\" + str(ex) + \"_0'[len(setidTeam[ex]):]}\" for ex in range(lenidTeam)]", # [\"{'setid\" + \"Team\" + str(ex) + \"_0'[len(setidTeam[ex]):]}\"
    INFOKEY.offset: f"[[0, 0] for ex in range({INFOKEY.lenidTeam})]", 
    INFOKEY.offsetsize: f"[[0, 0] for ex in range({INFOKEY.lenidTeam})]"
}

teamDetect_info_optional_set = {INFOKEY.brace}

teamDetect_info_optional_set.add(INFOKEY.isprefixseg)
teamDetect_info_optional_set.add(INFOKEY.maxUnits)
teamDetect_info_optional_set.add(INFOKEY.cite_name)
teamDetect_info_optional_set.add(INFOKEY.args)
teamDetect_info_optional_set.add(INFOKEY.opargs)
DETECT_OPTION_SET = set(DETECT_OPTION_DICT.keys())
teamDetect_info_optional_set.update(DETECT_OPTION_SET)

teamDetect_info_var_dependent_dict = {}

teamDetect_info_initial_brace_dict = {
    f"{INFOKEY.lenidTeam}": f"len({INFOKEY.setidTeam})"
}

teamDetect_info_default_brace_set = {
    f"{INFOKEY.name}", 
    f"{INFOKEY.offset}", 
    f"{INFOKEY.offsetsize}"
}

teamDetect_info_operation_pre_list = \
    operation_cycle_start("i", "0", f"i < {INFOKEY.lenidTeam}", "teamDetect_pre_cycle1") + \
        [
            {
                AUTOKEY.operation_type: AUTOKEY.typeset_id, 
                f"{INFOKEY.setidTeam}" + "{i}_": "1", 
                AUTOKEY.real_idexp: "{" + f"{INFOKEY.setidTeam}" + "[i]}"
            }, 
        ] + \
    operation_cycle_end("i", "i + 1", "teamDetect_pre_cycle1") + \
    ARGS_OPARGS_PRE_OPERATION

DETECT_OPTION_OPERATION_OPTIONAL = {DETECT_KEY:(True, DETECT_KEY, AUTOKEY.brace) if DEFECT_VALUE == bool else ("{" + DETECT_KEY + "}", DETECT_KEY, AUTOKEY.exist) for DETECT_KEY, DEFECT_VALUE in DETECT_OPTION_DICT.items()}

teamDetect_info_operation_optional = {
    rw.const.OBJECTOP.id: "{id_now}", 
    rw.const.OBJECTOP.minUnits: "{" + INFOKEY.minUnits + "}", 
    rw.const.OBJECTOP.maxUnits: ("{" + INFOKEY.maxUnits + "}", INFOKEY.maxUnits, AUTOKEY.exist), 
    rw.const.OBJECTOP.resetActivationAfter: "{" + INFOKEY.reset + "}", 
    rw.const.OBJECTOP.unitType: ("{" + f"{INFOKEY.unit}" + "}", INFOKEY.unit, AUTOKEY.exist), 
    rw.const.OBJECTOP.team: "{" + f"{INFOKEY.setTeam}" + "[i][j]}"
}
teamDetect_info_operation_optional.update(DETECT_OPTION_OPERATION_OPTIONAL)

teamDetect_info_operation_list = \
    operation_typeset_expression("setidTeam_id", "[]") + \
    operation_typeset_expression("setidTeam_id_dep", "[]") + \
    operation_typeset_expression("teamtoi", "dict()") + \
    operation_typeset_expression("teamtoid", "dict()") + \
    operation_typeset_expression("teamtoid_dep", "dict()") + \
    operation_typeset_expression("lenTeam", "0") + \
    operation_cycle_start("i", "0", f"i < {INFOKEY.lenidTeam}", "teamDetect_cycle3") + \
        operation_typeset_expression("setidTeam_id", "setidTeam_id + ['setidTeam{i}_0']") + \
    operation_cycle_end("i", "i + 1", "teamDetect_cycle3") + \
    operation_cycle_start("i", "0", f"i < {INFOKEY.lenidTeam}", "teamDetect_cycle4") + \
        operation_typeset_expression("setidTeam_id_now", "','.join([setidTeam_id[j] for j in range(len(setidTeam_id)) if j != i])") + \
        operation_typeset_expression("setidTeam_id_dep", "setidTeam_id_dep + ['setidTeam_id_now']") + \
    operation_cycle_end("i", "i + 1", "teamDetect_cycle4") + \
    operation_cycle_start("i", "0", f"i < {INFOKEY.lenidTeam}", "teamDetect_cycle1") + \
        operation_typeset_expression("lenTeam", f"lenTeam + len({INFOKEY.setTeam}[i])") + \
        operation_cycle_start("j", "0", f"j < len({INFOKEY.setTeam}[i])", "teamDetect_cycle2") + \
            operation_typeset_expression("teamtoi", "teamtoi | dict([[str(setTeam[i][j]),str(i)]])") + \
            operation_typeset_expression("teamtoid", "teamtoid | dict([[str(setTeam[i][j]),str(setidTeam_id[i])]])") + \
            operation_typeset_expression("teamtoid_dep", "teamtoid_dep | dict([[str(setTeam[i][j]), str(setidTeam_id_dep[i])]])") + \
            [
                {
                    AUTOKEY.operation_type:AUTOKEY.typeset_expression, 
                    "id_now": f"{INFOKEY.setidTeam}" + "{i}_0"
                }, 
            ] + \
            operation_if(f"len({INFOKEY.name}) != 1", "teamDetect_if2") + \
                [
                    {
                        AUTOKEY.operation_type:AUTOKEY.typeset_expression, 
                        "name_now": f"{INFOKEY.name}[i]"
                    }
                ] + \
            operation_else("teamDetect_if2") + \
                [
                    {
                        AUTOKEY.operation_type:AUTOKEY.typeset_expression, 
                        "name_now": f"{INFOKEY.name}[0]"
                    }
                ] + \
            operation_elseend("teamDetect_if2") + \
            operation_if(f"len({INFOKEY.offset}) != 1", "teamDetect_if3") + \
                [
                    {
                        AUTOKEY.operation_type:AUTOKEY.typeset_expression, 
                        "offset_now": f"{INFOKEY.offset}[i]"
                    }
                ] + \
            operation_else("teamDetect_if3") + \
                [
                    {
                        AUTOKEY.operation_type:AUTOKEY.typeset_expression, 
                        "offset_now": f"{INFOKEY.offset}[0]"
                    }
                ] + \
            operation_elseend("teamDetect_if3") + \
            operation_if(f"len({INFOKEY.offsetsize}) != 1", "teamDetect_if4") + \
                [
                    {
                        AUTOKEY.operation_type:AUTOKEY.typeset_expression, 
                        "offsetsize_now": f"{INFOKEY.offsetsize}[i]"
                    }
                ] + \
            operation_else("teamDetect_if4") + \
                [
                    {
                        AUTOKEY.operation_type:AUTOKEY.typeset_expression, 
                        "offsetsize_now": f"{INFOKEY.offsetsize}[0]"
                    }
                ] + \
            operation_elseend("teamDetect_if4") + \
            [
                {
                    AUTOKEY.operation_type: AUTOKEY.object, 
                    AUTOKEY.offset: "offset_now", 
                    AUTOKEY.offsetsize: "offsetsize_now", 
                    AUTOKEY.name: ("{name_now}", "j == 0", AUTOKEY.brace), 
                    AUTOKEY.type: rw.const.OBJECTTYPE.unitDetect, 
                    AUTOKEY.optional: teamDetect_info_operation_optional
                }

            ] + \
        operation_cycle_end("j", "j + 1", "teamDetect_cycle2") + \
    operation_cycle_end("i", "i + 1", "teamDetect_cycle1") + \
    BRACE_OPERATION_END


teamDetect_info = {
    INFOKEY.teamDetect_info:{
        AUTOKEY.info_args:teamDetect_info_args_dict, 
        AUTOKEY.default_args: teamDetect_info_default_args_dict, 
        AUTOKEY.var_dependent: teamDetect_info_var_dependent_dict, 
        AUTOKEY.optional:teamDetect_info_optional_set, 
        AUTOKEY.initial_brace: teamDetect_info_initial_brace_dict, 
        AUTOKEY.default_brace: teamDetect_info_default_brace_set, 

        AUTOKEY.ids: [], 
        AUTOKEY.prefix: AUTOKEY.prefix, 
        AUTOKEY.isprefixseg: AUTOKEY.isprefixseg, 
        AUTOKEY.args: [], 
        AUTOKEY.seg: ".", 
        AUTOKEY.opargs_prefix_len:1, 
        AUTOKEY.opargs: {}, 
        AUTOKEY.opargs_seg: ",", 
        AUTOKEY.operation_pre:teamDetect_info_operation_pre_list, 
        AUTOKEY.operation:teamDetect_info_operation_list, 
        AUTOKEY.no_check: True
    }
}