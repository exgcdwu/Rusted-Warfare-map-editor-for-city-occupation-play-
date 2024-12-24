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

teamDetect_info_args_dict = OrderedDict()

teamDetect_info_args_dict[INFOKEY.prefix] = str
teamDetect_info_args_dict[INFOKEY.isprefixseg] = bool
teamDetect_info_args_dict[INFOKEY.reset] = str
teamDetect_info_args_dict[INFOKEY.setTeam] = (list, list, int)
teamDetect_info_args_dict[INFOKEY.setidTeam] = (list, list, str)
teamDetect_info_args_dict[INFOKEY.neutralindex] = str

teamDetect_info_args_dict[INFOKEY.minUnits] = str
teamDetect_info_args_dict[INFOKEY.maxUnits] = str

teamDetect_info_args_dict[INFOKEY.aunit] = str
teamDetect_info_args_dict[INFOKEY.basicoffset] = (list, int)
teamDetect_info_args_dict[INFOKEY.basicoffsetsize] = (list, int)

teamDetect_info_args_dict[INFOKEY.name] = (list, str)
teamDetect_info_args_dict[INFOKEY.offset] = (list, list, int)
teamDetect_info_args_dict[INFOKEY.offsetsize] = (list, list, int)

teamDetect_info_args_dict[INFOKEY.cite_name] = str

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
    INFOKEY.name: "" + "[\"{'setid\" + \"Team\" + str(ex) + \"_0_0'[len('setid\" + \"Team\" + str(ex) + \"_0_'):]}\" for ex in range(lenidTeam)]", # [\"{'setid\" + \"Team\" + str(ex) + \"_0'[len(setidTeam[ex]):]}\"
    INFOKEY.offset: f"[[0, 0] for ex in range({INFOKEY.lenidTeam})]", 
    INFOKEY.offsetsize: f"[[0, 0] for ex in range({INFOKEY.lenidTeam})]", 
    INFOKEY.neutralindex: "-1", 
    INFOKEY.basicoffset: "-10 10", 
    INFOKEY.basicoffsetsize: "20 0", 
}

teamDetect_info_optional_set = {INFOKEY.brace}

teamDetect_info_optional_set.add(INFOKEY.isprefixseg)
teamDetect_info_optional_set.add(INFOKEY.cite_name)
teamDetect_info_optional_set.add(INFOKEY.minUnits)
teamDetect_info_optional_set.add(INFOKEY.maxUnits)
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
        operation_cycle_start("j", "0", f"j < len({INFOKEY.setidTeam}[i])", "teamDetect_pre_cycle2") + \
        [
            {
                AUTOKEY.operation_type: AUTOKEY.typeset_id, 
                f"{INFOKEY.setidTeam}" + "{i}_{j}_": "1", 
                AUTOKEY.real_idexp: "{" + f"{INFOKEY.setidTeam}" + "[i][j]}"
            }, 
        ] + \
        operation_cycle_end("j", "j + 1", "teamDetect_pre_cycle2") + \
    operation_cycle_end("i", "i + 1", "teamDetect_pre_cycle1")

DETECT_OPTION_OPERATION_OPTIONAL = {DETECT_KEY:(True, DETECT_KEY, AUTOKEY.brace) if DEFECT_VALUE == bool else ("{" + DETECT_KEY + "}", DETECT_KEY, AUTOKEY.exist) for DETECT_KEY, DEFECT_VALUE in DETECT_OPTION_DICT.items()}

teamDetect_info_operation_optional = {
    rw.const.OBJECTOP.id: ("{alsoactivate_now}", "{id_now_exist}", AUTOKEY.brace), 
    rw.const.OBJECTOP.alsoActivate: ("{alsoactivate_now}", "{not id_now_exist}", AUTOKEY.brace), 
    rw.const.OBJECTOP.minUnits: ("{" + INFOKEY.minUnits + "}", INFOKEY.minUnits, AUTOKEY.exist), 
    rw.const.OBJECTOP.maxUnits: ("{" + INFOKEY.maxUnits + "}", INFOKEY.maxUnits, AUTOKEY.exist), 
    rw.const.OBJECTOP.resetActivationAfter: "{" + INFOKEY.reset + "}", 
    rw.const.OBJECTOP.unitType: ("{" + f"{INFOKEY.aunit}" + "}", INFOKEY.aunit, AUTOKEY.exist), 
    rw.const.OBJECTOP.team: "{" + f"{INFOKEY.setTeam}" + "[i][j]}"
}
teamDetect_info_operation_optional.update(DETECT_OPTION_OPERATION_OPTIONAL)

teamDetect_info_operation_optional_z = deepcopy(teamDetect_info_operation_optional)

teamDetect_info_operation_optional_z.pop(rw.const.OBJECTOP.team)
teamDetect_info_operation_optional_z.pop(rw.const.OBJECTOP.minUnits)
teamDetect_info_operation_optional_z[rw.const.OBJECTOP.maxUnits] = "{" + INFOKEY.minUnits + " - 1}"

teamDetect_info_operation_optional_zm = deepcopy(teamDetect_info_operation_optional)

teamDetect_info_operation_optional_zm.pop(rw.const.OBJECTOP.team)
teamDetect_info_operation_optional_zm.pop(rw.const.OBJECTOP.maxUnits)
teamDetect_info_operation_optional_zm.pop(rw.const.OBJECTOP.id)
teamDetect_info_operation_optional_zm[rw.const.OBJECTOP.minUnits] = "{" + INFOKEY.maxUnits + " + 1}"

teamDetect_info_operation_list = \
    error_brace(
        check_minmaxUnits_operation("teamDetect_info") + \
        operation_cycle_start("i", "0", f"i < {INFOKEY.lenidTeam}", "teamDetect_cycle_check1") + \
            operation_cycle_start("j", "0", f"j < len({INFOKEY.setTeam}[i])", "teamDetect_cycle_check2") + \
                error_brace(
                    operation_if(f"{INFOKEY.setTeam}[i][j] < -3", "teamDetect_if_setTeam_error") + \
                        operation_error("setTeam[{i}][{j}]({setTeam[i][j]}) <= -4, please check your info or tagged object." + \
                                        "|setTeam[{i}][{j}]({setTeam[i][j]}) <= -4, 请查看对应teamDetect_info和标记宾语是否出错") + \
                    operation_ifend("teamDetect_if_setTeam_error")
                ) + \
            operation_cycle_end("j", "j + 1", "teamDetect_cycle_check2") + \
        operation_cycle_end("i", "i + 1", "teamDetect_cycle_check1")
    ) + \
    operation_typeset_expression("setTeam_len", "[len(setTeam[ti]) for ti in range(lenidTeam)]") + \
    operation_typeset_expression("setidTeam_len", "[len(setidTeam[ti]) for ti in range(lenidTeam)]") + \
    operation_typeset_expression("setidTeam_id", "[]") + \
    operation_typeset_expression("setidTeam_id_all_basic", "[]") + \
    operation_typeset_expression("iti", "[]") + \
    operation_typeset_expression("itj", "[]") + \
    operation_cycle_start("i", "0", f"i < {INFOKEY.lenidTeam}", "teamDetect_cycle3") + \
        operation_typeset_expression("setidTeam_id", "setidTeam_id + ['setidTeam{i}_0_0']") + \
        operation_typeset_expression("setidTeam_len_now", "setidTeam_len[i]") + \
        operation_typeset_expression("setTeam_len_now", "setTeam_len[i]") + \
        operation_typeset_expression("iti", "iti + [i] * setTeam_len_now") + \
        operation_typeset_expression("itj", "itj + [tj for tj in range(setTeam_len_now)]") + \
        operation_if("setidTeam_len_now != 1", "teamDetect_if_isdoid") + \
            operation_cycle_start("j", "0", f"j < setidTeam_len_now", "teamDetect_cycle2_setidall") + \
                operation_typeset_expression("setidTeam_id_all_basic", "setidTeam_id_all_basic + ['setidTeam{i}_{j}_0']") + \
            operation_cycle_end("j", "j + 1", "teamDetect_cycle2_setidall") + \
        operation_ifend("teamDetect_if_isdoid") + \
    operation_cycle_end("i", "i + 1", "teamDetect_cycle3") + \
    operation_typeset_expression("lenTeam", f"sum(setTeam_len)") + \
    operation_typeset_expression("setidTeam_set", "set(setidTeam_id)") + \
    operation_typeset_expression("setidTeam_id_all_basic_set", "set(setidTeam_id_all_basic)") + \
    operation_typeset_expression("setidTeam_id_all_basic_set_list", "list(setidTeam_id_all_basic_set)") + \
    operation_typeset_expression("setidTeam_id_depn", "[','.join([myid for myid in setidTeam_set if myid != setidTeam_id[ti]]) for ti in range(lenidTeam)]") + \
    operation_typeset_expression("setidTeam_id_dep", "[','.join([myid for myid in setidTeam_set if myid != setidTeam_id[ti] and myid != setidTeam_id[neutralindex]]) for ti in range(lenidTeam)]") + \
    operation_typeset_expression("teamtoi", "dict([[str(setTeam[iti[ind]][itj[ind]]),str(iti[ind])] for ind in range(lenTeam)])") + \
    operation_typeset_expression("teamtoid", "dict([[str(setTeam[iti[ind]][itj[ind]]),str(setidTeam_id[iti[ind]])] for ind in range(lenTeam)])") + \
    operation_typeset_expression("teamtoid_depn", "dict([[str(setTeam[iti[ind]][itj[ind]]),str(setidTeam_id_depn[iti[ind]])] for ind in range(lenTeam)])") + \
    operation_typeset_expression("teamtoid_dep", "dict([[str(setTeam[iti[ind]][itj[ind]]),str(setidTeam_id_dep[iti[ind]])] for ind in range(lenTeam)])") + \
    operation_cycle_start("i", "0", f"i < {INFOKEY.lenidTeam}", "teamDetect_cycle1") + \
        operation_typeset_expression("setidTeam_len_now", "setidTeam_len[i]") + \
        operation_typeset_expression("setTeam_len_now", "setTeam_len[i]") + \
        operation_typeset_expression("id_now_exist", "setidTeam_len_now == 1 and 'setidTeam{i}_0_0' not in setidTeam_id_all_basic_set") + \
        [
            {
                AUTOKEY.operation_type:AUTOKEY.typeset_expression, 
                "alsoactivate_now": f"'{INFOKEY.setidTeam}" + "{i}_0_0'"
            }, 
        ] + \
        operation_cycle_start("j", "1", f"j < setidTeam_len_now", "teamDetect_cycle2_alsoacti") + \
            [
                {
                    AUTOKEY.operation_type:AUTOKEY.typeset_expression, 
                    "alsoactivate_now": f"'alsoactivate_now' + ',' + '{INFOKEY.setidTeam}" + "{i}_{j}_0'"
                }, 
            ] + \
        operation_cycle_end("j", "j + 1", "teamDetect_cycle2_alsoacti") + \
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
        operation_cycle_start("j", "0", f"j < setTeam_len_now", "teamDetect_cycle2") + \
            operation_if("j == 1", "teamDetect_closeaddid") + \
                operation_typeset_expression("id_now_exist", "False") + \
            operation_ifend("teamDetect_closeaddid") + \
            operation_if(f"{INFOKEY.setTeam}[i][j] != -3", "teamDetect_ifteam-3_object") + \
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
            operation_else("teamDetect_ifteam-3_object") + \
                operation_exist_if(f"{INFOKEY.minUnits}", "teamDetect_ifminUnits0") + \
                    [
                        {
                            AUTOKEY.operation_type: AUTOKEY.object, 
                            AUTOKEY.offset: "offset_now", 
                            AUTOKEY.offsetsize: "offsetsize_now", 
                            AUTOKEY.name: ("{name_now}", "j == 0", AUTOKEY.brace), 
                            AUTOKEY.type: rw.const.OBJECTTYPE.unitDetect, 
                            AUTOKEY.optional: teamDetect_info_operation_optional_z
                        }
                    ] + \
                operation_ifend("teamDetect_ifminUnits0") + \
                operation_exist_if(f"{INFOKEY.maxUnits}", "teamDetect_existifmaxUnits") + \
                    [
                        {
                            AUTOKEY.operation_type: AUTOKEY.object, 
                            AUTOKEY.offset: "offset_now", 
                            AUTOKEY.offsetsize: "offsetsize_now", 
                            AUTOKEY.type: rw.const.OBJECTTYPE.unitDetect, 
                            AUTOKEY.optional: teamDetect_info_operation_optional_zm
                        }
                    ] + \
                operation_ifend("teamDetect_existifmaxUnits") + \
            operation_elseend("teamDetect_ifteam-3_object") + \
        operation_cycle_end("j", "j + 1", "teamDetect_cycle2") + \
    operation_cycle_end("i", "i + 1", "teamDetect_cycle1") + \
    operation_typeset_expression("setidTeam_id_all_basic_set_list_len", "len(setidTeam_id_all_basic_set_list)") + \
    operation_cycle_start("i", "0", f"i < setidTeam_id_all_basic_set_list_len", "teamDetect_cycle2_basic") + \
        [
            {
                AUTOKEY.operation_type: AUTOKEY.object, 
                AUTOKEY.type: rw.const.OBJECTTYPE.basic, 
                AUTOKEY.offset: f"{INFOKEY.basicoffset}", 
                AUTOKEY.offsetsize: f"{INFOKEY.basicoffsetsize}", 
                AUTOKEY.name: "{setidTeam_id_all_basic_set_list[i]}", 
                AUTOKEY.optional: {
                    rw.const.OBJECTOP.resetActivationAfter: "{" + INFOKEY.reset + "}"
                }
            }
        ] + \
    operation_cycle_end("i", "i + 1", "teamDetect_cycle2_basic")

teamDetect_info_is_cite_white_list = [
    "setidTeam_id", 
    "setidTeam_id_depn", 
    "setidTeam_id_dep", 
    "teamtoi", 
    "teamtoid", 
    "teamtoid_depn", 
    "teamtoid_dep", 
    "lenTeam"
]

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
        AUTOKEY.no_check: True, 
        AUTOKEY.is_cite_white_list: teamDetect_info_is_cite_white_list
    }
}

teamDetect_info = brace_add_info(teamDetect_info)
teamDetect_info = args_opargs_add_info(teamDetect_info)