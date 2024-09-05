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
from auto._data._teamDetect import *

multiRemove_info_args_dict = OrderedDict()

multiRemove_info_args_dict[INFOKEY.prefix] = str
multiRemove_info_args_dict[INFOKEY.isprefixseg] = bool

multiRemove_info_args_dict[INFOKEY.acti] = (list, list, str)
multiRemove_info_args_dict[INFOKEY.deacti] = (list, list, str)
multiRemove_info_args_dict[INFOKEY.teamDetect_cite] = str
multiRemove_info_args_dict[INFOKEY.numDetect_cite] = str

multiRemove_info_args_dict[INFOKEY.team] = (list, str)
multiRemove_info_args_dict[INFOKEY.reset] = (list, str)
multiRemove_info_args_dict[INFOKEY.warmup] = (list, str)
multiRemove_info_args_dict[INFOKEY.delay] = (list, str)
multiRemove_info_args_dict[INFOKEY.repeat] = (list, str)

multiRemove_info_args_dict[INFOKEY.name] = (list, str)
multiRemove_info_args_dict[INFOKEY.offset] = (list, list, int)
multiRemove_info_args_dict[INFOKEY.offsetsize] = (list, list, int)

multiRemove_info_args_dict[INFOKEY.args] = (list, list, str)
multiRemove_info_args_dict[INFOKEY.opargs] = (list, list, str)
multiRemove_info_args_dict[INFOKEY.brace] = (list, str)

multiRemove_info_default_args_dict = {
    INFOKEY.name: "", 
    INFOKEY.offset: "0 0", 
    INFOKEY.offsetsize: "0 0"
}

multiRemove_info_optional_set = {INFOKEY.brace}

multiRemove_info_optional_set.add(INFOKEY.isprefixseg)
multiRemove_info_optional_set.add(INFOKEY.teamDetect_cite)
multiRemove_info_optional_set.add(INFOKEY.numDetect_cite)
multiRemove_info_optional_set.add(INFOKEY.acti)
multiRemove_info_optional_set.add(INFOKEY.deacti)
multiRemove_info_optional_set.add(INFOKEY.team)
multiRemove_info_optional_set.add(INFOKEY.reset)
multiRemove_info_optional_set.add(INFOKEY.warmup)
multiRemove_info_optional_set.add(INFOKEY.delay)
multiRemove_info_optional_set.add(INFOKEY.repeat)
multiRemove_info_optional_set.add(INFOKEY.args)
multiRemove_info_optional_set.add(INFOKEY.opargs)

multiRemove_info_var_dependent_dict = {}

multiRemove_info_initial_brace_dict = {}

multiRemove_info_default_brace_set = set()

multiRemove_info_operation_pre_list = ARGS_OPARGS_PRE_OPERATION

multiRemove_info_operation_optional = {
    rw.const.OBJECTOP.activatedBy: ("{acti_now}", "acti_now_exist", AUTOKEY.brace), 
    rw.const.OBJECTOP.deactivatedBy: ("{deacti_now}", "deacti_now_exist", AUTOKEY.brace), 
    rw.const.OBJECTOP.team: ("{team_now}", "team_now_exist", AUTOKEY.brace), 
    rw.const.OBJECTOP.resetActivationAfter: ("{reset_now}", "reset_now_exist", AUTOKEY.brace), 
    rw.const.OBJECTOP.warmup: ("{warmup_now}", "warmup_now_exist", AUTOKEY.brace), 
    rw.const.OBJECTOP.repeatDelay: ("{repeat_now}", "repeat_now_exist", AUTOKEY.brace), 
    rw.const.OBJECTOP.delay: ("{delay_now}", "delay_now_exist", AUTOKEY.brace), 
}

def operation_join_quote(assign_name:str, info_args:str):
    return operation_typeset_expression(assign_name, f"\",\".join({info_args})")

def operation_list_join_quote(assign_name:str, info_args:str):
    return operation_typeset_expression(assign_name, f"[\",\".join(info_args_now) for info_args_now in {info_args}]")

def operation_list_assign(info_args:str, index:str, assign_name:str, info_tag:str, default_assign:str = None):
    return operation_exist_if(f"{info_args}", info_tag + "_exist_if_" + assign_name) + \
        operation_if(f"len({info_args}) == 1", info_tag + "_if_" + assign_name, 1) + \
            [
                {
                    AUTOKEY.operation_type:AUTOKEY.typeset_expression, 
                    "{" + f"\"{assign_name}_\" + " + f"\"{index}\"" + "}": f"{info_args}[0]"
                }
            ] + \
            operation_typeset_expression(f"{assign_name}_exist", "True") + \
            operation_typeset_expression(f"{assign_name}", f"{assign_name}_" + "{" + f"{index}" + "}") + \
        operation_elseif(f"{index} < len({info_args})", info_tag + "_if_" + assign_name, 2) + \
            [
                {
                    AUTOKEY.operation_type:AUTOKEY.typeset_expression, 
                    "{" + f"\"{assign_name}_\" + " + f"\"{index}\"" + "}": f"{info_args}[{index}]"
                }
            ] + \
            operation_typeset_expression(f"{assign_name}_exist", "True") + \
            operation_typeset_expression(f"{assign_name}", f"{assign_name}_" + "{" + f"{index}" + "}") + \
        operation_else(info_tag + "_if_" + assign_name, 3) + \
            (operation_typeset_expression("{" + f"\"{assign_name}_\" + " + f"\"{index}\"" + "}", default_assign) + \
            operation_typeset_expression(f"{assign_name}_exist", "True")
            if default_assign != None else 
            operation_typeset_expression(f"{assign_name}_exist", "False")) + \
        operation_elseend(info_tag + "_if_" + assign_name) + \
    operation_else(info_tag + "_exist_if_" + assign_name) + \
        operation_typeset_expression(f"{assign_name}_exist", "False") + \
    operation_elseend(info_tag + "_exist_if_" + assign_name)

def operation_ids_assign(args_exist:str, args:str, add_args:str, info_tag:str, assign_tag:str):
    return operation_typeset_expression("temp", args) + \
    operation_if(args_exist, info_tag + f"_exist_if_temp_assign{assign_tag}") + \
        operation_if(f"temp != \"\"", info_tag + f"_if_temp_assign{assign_tag}") + \
            [
                {
                    AUTOKEY.operation_type:AUTOKEY.typeset_expression, 
                    args: f"\"temp\" + \",\" + \"{add_args}\""
                }
            ] + \
        operation_else(info_tag + f"_if_temp_assign{assign_tag}") + \
            [
                {
                    AUTOKEY.operation_type:AUTOKEY.typeset_expression, 
                    args: f"{add_args}"
                }
            ] + \
        operation_elseend(info_tag + f"_if_temp_assign{assign_tag}") + \
    operation_else(info_tag + f"_exist_if_temp_assign{assign_tag}") + \
        [
            {
                AUTOKEY.operation_type:AUTOKEY.typeset_expression, 
                args: f"{add_args}"
            }
        ] + \
    operation_elseend(info_tag + f"_exist_if_temp_assign{assign_tag}")

multiRemove_info_operation_list = \
    [
        {
            AUTOKEY.operation_type:AUTOKEY.typeset_expression, 
            "lenRemove": "0"
        }
    ] + \
    operation_exist_if(INFOKEY.numDetect_cite, "multiRemove_exist_if_numDetect_cite") + \
        [
            {
                AUTOKEY.operation_type:AUTOKEY.typeset_expression, 
                "lenRemove": f"max(lenRemove, " + "{" + f"{INFOKEY.numDetect_cite}" + "}" + f".{INFOKEY.lenidNum})"
            }
        ] + \
    operation_ifend("multiRemove_exist_if_numDetect_cite") + \
    operation_exist_if(INFOKEY.acti,  "multiRemove_exist_if_acti") + \
        [
            {
                AUTOKEY.operation_type:AUTOKEY.typeset_expression, 
                "lenRemove": f"max(lenRemove, len({INFOKEY.acti}))"
            }
        ] + \
        operation_list_join_quote(f"{INFOKEY.acti}", f"{INFOKEY.acti}") + \
    operation_ifend("multiRemove_exist_if_acti") + \
    operation_exist_if(INFOKEY.deacti,  "multiRemove_exist_if_deacti") + \
        [
            {
                AUTOKEY.operation_type:AUTOKEY.typeset_expression, 
                "lenRemove": f"max(lenRemove, len({INFOKEY.deacti}))"
            }
        ] + \
        operation_list_join_quote(f"{INFOKEY.deacti}", f"{INFOKEY.deacti}") + \
    operation_ifend("multiRemove_exist_if_deacti") + \
    operation_exist_if(INFOKEY.team,  "multiRemove_exist_if_team") + \
        [
            {
                AUTOKEY.operation_type:AUTOKEY.typeset_expression, 
                "lenRemove": f"max(lenRemove, len({INFOKEY.team}))"
            }
        ] + \
        operation_list_join_quote(f"{INFOKEY.team}", f"{INFOKEY.team}") + \
    operation_ifend("multiRemove_exist_if_team") + \
    operation_cycle_start("i", "0", "i < lenRemove", "multiRemove_cycle_lenRemove") + \
        operation_list_assign(f"{INFOKEY.name}", "i", "name_now", "multiRemove") + \
        operation_list_assign(f"{INFOKEY.offset}", "i", "offset_now", "multiRemove", "[0, 0]") + \
        operation_list_assign(f"{INFOKEY.offsetsize}", "i", "offsetsize_now", "multiRemove", "[0, 0]") + \
        operation_list_assign(f"{INFOKEY.acti}", "i", "acti_now", "multiRemove") + \
        operation_list_assign(f"{INFOKEY.deacti}", "i", "deacti_now", "multiRemove") + \
        operation_list_assign(f"{INFOKEY.team}", "i", "team_now", "multiRemove") + \
        operation_list_assign(f"{INFOKEY.reset}", "i", "reset_now", "multiRemove") + \
        operation_list_assign(f"{INFOKEY.warmup}", "i", "warmup_now", "multiRemove") + \
        operation_list_assign(f"{INFOKEY.repeat}", "i", "repeat_now", "multiRemove") + \
        operation_list_assign(f"{INFOKEY.delay}", "i", "delay_now", "multiRemove") + \
        operation_exist_if(f"{INFOKEY.teamDetect_cite}", "multiRemove_exist_if_teamDetect_cite_assign") + \
            operation_if("team_now_exist == True", "multiRemove_exist_if_teamDetect_cite_assign_team_exist") + \
                operation_if("{" + f"{INFOKEY.teamDetect_cite}" + "}" + ".teamtoi.get(team_now) != None", "multiRemove_if_teamDetect_cite_assign_acti") + \
                    operation_ids_assign(f"{INFOKEY.acti}_now_exist", f"{INFOKEY.acti}_now_" + "{i}", "{" + f"{INFOKEY.teamDetect_cite}" + "}" + f".{INFOKEY.setidTeam}" + "{{" + f"{INFOKEY.teamDetect_cite}" + "}" + ".teamtoi[team_now]}_0", "multiRemove", "actiids_addteamDetect") + \
                    operation_typeset_expression(f"{INFOKEY.acti}_now_exist", "True") + \
                    operation_typeset_expression(f"{INFOKEY.acti}_now", f"{INFOKEY.acti}_now_" + "{i}") + \
                operation_ifend("multiRemove_if_teamDetect_cite_assign_acti") + \
            operation_ifend("multiRemove_exist_if_teamDetect_cite_assign_team_exist") + \
        operation_ifend("multiRemove_exist_if_teamDetect_cite_assign") + \
        operation_exist_if(f"{INFOKEY.numDetect_cite}", "multiRemove_exist_if_numDetect_cite_assign") + \
            operation_if(f"i < " + "{" + f"{INFOKEY.numDetect_cite}" + "}" + f".{INFOKEY.lenidNum}", "multiRemove_if_numDetect_cite_assign_acti") + \
                operation_ids_assign(f"{INFOKEY.acti}_now_exist", f"{INFOKEY.acti}_now_" + "{i}", "{" + f"{INFOKEY.numDetect_cite}" + "}" + f".{INFOKEY.setidNum}" + "{i}_0", "multiRemove", "actiids_addnumDetect") + \
                operation_typeset_expression(f"{INFOKEY.acti}_now_exist", "True") + \
                operation_typeset_expression(f"{INFOKEY.acti}_now", f"{INFOKEY.acti}_now_" + "{i}") + \
            operation_ifend("multiRemove_if_numDetect_cite_assign_acti") + \
        operation_ifend("multiRemove_exist_if_numDetect_cite_assign") + \
        [
            {
                AUTOKEY.operation_type: AUTOKEY.object, 
                AUTOKEY.offset: "offset_now_{i}", 
                AUTOKEY.offsetsize: "offsetsize_now_{i}", 
                AUTOKEY.name: ("{name_now}", "name_now_exist", AUTOKEY.brace), 
                AUTOKEY.type: rw.const.OBJECTTYPE.unitRemove, 
                AUTOKEY.optional: multiRemove_info_operation_optional
            }
        ] + \
    operation_cycle_end("i", "i + 1", "multiRemove_cycle_lenRemove") + \
    BRACE_OPERATION_END



multiRemove_info = {
    INFOKEY.multiRemove_info:{
        AUTOKEY.info_args:multiRemove_info_args_dict, 
        AUTOKEY.default_args: multiRemove_info_default_args_dict, 
        AUTOKEY.var_dependent: multiRemove_info_var_dependent_dict, 
        AUTOKEY.optional:multiRemove_info_optional_set, 
        AUTOKEY.default_brace: multiRemove_info_default_brace_set, 
        AUTOKEY.initial_brace: multiRemove_info_initial_brace_dict, 
    
        AUTOKEY.ids: [], 
        AUTOKEY.prefix: AUTOKEY.prefix, 
        AUTOKEY.isprefixseg: AUTOKEY.isprefixseg, 
        AUTOKEY.args: [], 
        AUTOKEY.seg: ".", 
        AUTOKEY.opargs_prefix_len:1, 
        AUTOKEY.opargs: {}, 
        AUTOKEY.opargs_seg: ",", 

        AUTOKEY.operation_pre: multiRemove_info_operation_pre_list, 
        AUTOKEY.operation: multiRemove_info_operation_list, 
        AUTOKEY.no_check: True
    }
}

