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
from command.objectgroupauto._data._teamDetect import *
from command.objectgroupauto._data._time import *

multiText_info_args_dict = OrderedDict()

multiText_info_args_dict[INFOKEY.prefix] = str
multiText_info_args_dict[INFOKEY.isprefixseg] = bool
multiText_info_args_dict[INFOKEY.reset] = str

multiText_info_args_dict[INFOKEY.acti] = (list, list, str)
multiText_info_args_dict[INFOKEY.deacti] = (list, list, str)
multiText_info_args_dict[INFOKEY.teamDetect_cite] = str
multiText_info_args_dict[INFOKEY.numDetect_cite] = str
multiText_info_args_dict[INFOKEY.isdefaultText] = bool

multiText_info_args_dict[INFOKEY.textsize] = (list, str)
multiText_info_args_dict[INFOKEY.color] = (list, str)
multiText_info_args_dict[INFOKEY.name] = (list, str)
multiText_info_args_dict[INFOKEY.text] = (list, str)
multiText_info_args_dict[INFOKEY.offset] = (list, list, int)
multiText_info_args_dict[INFOKEY.offsetsize] = (list, list, int)

multiText_info_default_args_dict = {
    INFOKEY.name: "", 
    INFOKEY.offset: "0 0", 
    INFOKEY.offsetsize: "0 0", 
    INFOKEY.reset: "1s"
}

multiText_info_optional_set = set()

multiText_info_optional_set.add(INFOKEY.isprefixseg)
multiText_info_optional_set.add(INFOKEY.teamDetect_cite)
multiText_info_optional_set.add(INFOKEY.numDetect_cite)
multiText_info_optional_set.add(INFOKEY.acti)
multiText_info_optional_set.add(INFOKEY.deacti)
multiText_info_optional_set.add(INFOKEY.isdefaultText)
multiText_info_optional_set.add(INFOKEY.textsize)
multiText_info_optional_set.add(INFOKEY.color)
multiText_info_optional_set.add(INFOKEY.name)

multiText_info_var_dependent_dict = {INFOKEY.isdefaultText:INFOKEY.teamDetect_cite}

multiText_info_initial_brace_dict = {}

multiText_info_default_brace_set = set()

multiText_info_operation_pre_list = []

multiText_info_operation_optional = {
    rw.const.OBJECTOP.activatedBy: ("{acti_now}", "acti_now_exist", AUTOKEY.brace), 
    rw.const.OBJECTOP.deactivatedBy: ("{deacti_now}", "deacti_now_exist", AUTOKEY.brace), 
    rw.const.OBJECTOP.resetActivationAfter: "{" + f"{INFOKEY.reset}" + "}", 
    rw.const.OBJECTOP.textColor: ("{color_now}", "color_now_exist", AUTOKEY.brace), 
    rw.const.OBJECTOP.textSize: ("{textsize_now}", "textsize_now_exist", AUTOKEY.brace), 
    rw.const.OBJECTOP.text: ("{text_now}", "text_now_exist", AUTOKEY.brace), 
}

def operation_join_quote(assign_name:str, info_args:str):
    return operation_typeset_expression(assign_name, f"\",\".join({info_args})")

def operation_list_join_quote(assign_name:str, info_args:str, depth:int = MAXTRANSDEPTH):
    return operation_typeset_expression(assign_name, f"[\",\".join(info_args_now) for info_args_now in {info_args}]", depth = depth)

def operation_list_assign(info_args:str, index:str, assign_name:str, info_tag:str, default_assign:str = None):
    return \
    operation_exist_if(f"{info_args}", info_tag + "_exist_if_" + assign_name) + \
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
    operation_elseend(info_tag + "_exist_if_" + assign_name) + \
[]

def operation_ids_assign(args_exist:str, args:str, add_args:str, info_tag:str, assign_tag:str):
    return \
    operation_if(args_exist, info_tag + f"_exist_if_temp_assign{assign_tag}") + \
        operation_if(f"'{args}' != ''", info_tag + f"_if_temp_assign{assign_tag}") + \
            [
                {
                    AUTOKEY.operation_type:AUTOKEY.typeset_expression, 
                    args: f"\"{args}\" + \",\" + \"{add_args}\""
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

multiText_info_operation_list = \
    [
        {
            AUTOKEY.operation_type:AUTOKEY.typeset_expression, 
            "lenText": "0"
        }
    ] + \
    operation_exist_if(INFOKEY.teamDetect_cite, "multiText_exist_if_teamDetect_cite") + \
        operation_if(INFOKEY.isdefaultText, "multiText_if_isdefaultText") + \
            [
                {
                    AUTOKEY.operation_type:AUTOKEY.typeset_expression, 
                    "lenText": "max(lenText,{" +  f"{INFOKEY.teamDetect_cite}" + "}." + f"{INFOKEY.lenidTeam}" + " + 1)"
                }
            ] + \
        operation_else("multiText_if_isdefaultText") + \
            [
                {
                    AUTOKEY.operation_type:AUTOKEY.typeset_expression, 
                    "lenText": "max(lenText,{" +  f"{INFOKEY.teamDetect_cite}" + "}." + f"{INFOKEY.lenidTeam}" + ")"
                }
            ] + \
        operation_elseend("multiText_if_isdefaultText") + \
    operation_ifend("multiText_exist_if_teamDetect_cite") + \
    operation_exist_if(INFOKEY.numDetect_cite, "multiText_exist_if_numDetect_cite") + \
        [
            {
                AUTOKEY.operation_type:AUTOKEY.typeset_expression, 
                    "lenText": "max(lenText,{" +  f"{INFOKEY.numDetect_cite}" + "}." + f"{INFOKEY.lenidNum}" + ")"
            }
        ] + \
    operation_ifend("multiText_exist_if_numDetect_cite") + \
    operation_exist_if(INFOKEY.acti,  "multiText_exist_if_acti") + \
        [
            {
                AUTOKEY.operation_type:AUTOKEY.typeset_expression, 
                "lenText": f"max(lenText, len({INFOKEY.acti}))"
            }
        ] + \
        operation_list_join_quote(f"{INFOKEY.acti}", f"{INFOKEY.acti}") + \
    operation_ifend("multiText_exist_if_acti") + \
    operation_exist_if(INFOKEY.deacti,  "multiText_exist_if_deacti") + \
        [
            {
                AUTOKEY.operation_type:AUTOKEY.typeset_expression, 
                "lenText": f"max(lenText, len({INFOKEY.deacti}))"
            }
        ] + \
        operation_list_join_quote(f"{INFOKEY.deacti}", f"{INFOKEY.deacti}") + \
    operation_ifend("multiText_exist_if_deacti") + \
    operation_cycle_start("i", "0", "i < lenText", "multiText_cycle_lenText") + \
        operation_list_assign(f"{INFOKEY.name}", "i", "name_now", "multiText") + \
        operation_list_assign(f"{INFOKEY.offset}", "i", "offset_now", "multiText", "[0, 0]") + \
        operation_list_assign(f"{INFOKEY.offsetsize}", "i", "offsetsize_now", "multiText", "[0, 0]") + \
        operation_list_assign(f"{INFOKEY.acti}", "i", "acti_now", "multiText") + \
        operation_list_assign(f"{INFOKEY.deacti}", "i", "deacti_now", "multiText") + \
        operation_list_assign(f"{INFOKEY.color}", "i", "color_now", "multiText") + \
        operation_list_assign(f"{INFOKEY.text}", "i", "text_now", "multiText") + \
        operation_list_assign(f"{INFOKEY.textsize}", "i", "textsize_now", "multiText") + \
        operation_exist_if(f"{INFOKEY.teamDetect_cite}", "multiText_exist_if_teamDetect_cite_assign") + \
            operation_if("i < {" + f"{INFOKEY.teamDetect_cite}" + "}." + f"{INFOKEY.lenidTeam}", "multiText_if_teamDetect_cite_assign_acti", 1) + \
                operation_ids_assign(f"{INFOKEY.acti}_now_exist", f"{INFOKEY.acti}_now_" + "{i}", "{" + f"{INFOKEY.teamDetect_cite}" + "}" + f".{INFOKEY.setidTeam}" + "{i}_0_0", "multiText", "actiids_addteamDetect") + \
                operation_typeset_expression(f"{INFOKEY.acti}_now_exist", "True") + \
                operation_typeset_expression(f"{INFOKEY.acti}_now", f"{INFOKEY.acti}_now_" + "{i}") + \
            operation_elseif("i == {" + f"{INFOKEY.teamDetect_cite}" + "}.{" + f"{INFOKEY.lenidTeam}" + "} and isdefaultText", "multiText_if_teamDetect_cite_assign_acti", 2) + \
                operation_cycle_start("j", "0", "j < {" + f"{INFOKEY.teamDetect_cite}" + "}." + f"{INFOKEY.lenidTeam}", "multiText_cycle_teamDetect_cite_assign_deacti") + \
                    operation_ids_assign(f"{INFOKEY.deacti}_now_exist", f"{INFOKEY.deacti}_now_" + "{i}", "{" + f"{INFOKEY.teamDetect_cite}" + "}" + f".{INFOKEY.setidTeam}" + "{j}_0_0", "multiText", "deactiids_addteamDetect") + \
                    operation_typeset_expression(f"{INFOKEY.deacti}_now_exist", "True") + \
                    operation_typeset_expression(f"{INFOKEY.deacti}_now", f"{INFOKEY.deacti}_now_" + "{i}") + \
                operation_cycle_end("j", "j + 1", "multiText_cycle_teamDetect_cite_assign_deacti") + \
            operation_ifend("multiText_if_teamDetect_cite_assign_acti", 3) + \
        operation_ifend("multiText_exist_if_teamDetect_cite_assign") + \
        operation_exist_if(f"{INFOKEY.numDetect_cite}", "multiText_exist_if_numDetect_cite_assign") + \
            operation_if("i < {" + f"{INFOKEY.numDetect_cite}" + "}" + f".{INFOKEY.lenidNum}", "multiText_if_numDetect_cite_assign_acti") + \
                operation_ids_assign(f"{INFOKEY.acti}_now_exist", f"{INFOKEY.acti}_now_" + "{i}", "{" + f"{INFOKEY.numDetect_cite}" + "}" + f".{INFOKEY.setidNum}" + "{i}_0", "multiText", "actiids_addnumDetect") + \
                operation_typeset_expression(f"{INFOKEY.acti}_now_exist", "True") + \
                operation_typeset_expression(f"{INFOKEY.acti}_now", f"{INFOKEY.acti}_now_" + "{i}") + \
            operation_ifend("multiText_if_numDetect_cite_assign_acti") + \
        operation_ifend("multiText_exist_if_numDetect_cite_assign") + \
        [
            {
                AUTOKEY.operation_type: AUTOKEY.object, 
                AUTOKEY.exist: ["text_now_exist"], 
                AUTOKEY.offset: "offset_now_{i}", 
                AUTOKEY.offsetsize: "offsetsize_now_{i}", 
                AUTOKEY.name: ("{name_now}", "name_now_exist", AUTOKEY.brace), 
                AUTOKEY.type: rw.const.OBJECTTYPE.mapText, 
                AUTOKEY.optional: multiText_info_operation_optional
            }
        ] + \
    operation_cycle_end("i", "i + 1", "multiText_cycle_lenText")



multiText_info = {
    INFOKEY.multiText_info:{
        AUTOKEY.info_args:multiText_info_args_dict, 
        AUTOKEY.default_args: multiText_info_default_args_dict, 
        AUTOKEY.var_dependent: multiText_info_var_dependent_dict, 
        AUTOKEY.optional:multiText_info_optional_set, 
        AUTOKEY.default_brace: multiText_info_default_brace_set, 
        AUTOKEY.initial_brace: multiText_info_initial_brace_dict, 
    
        AUTOKEY.ids: [], 
        AUTOKEY.prefix: AUTOKEY.prefix, 
        AUTOKEY.isprefixseg: AUTOKEY.isprefixseg, 
        AUTOKEY.args: [], 
        AUTOKEY.seg: ".", 
        AUTOKEY.opargs_prefix_len:1, 
        AUTOKEY.opargs: {}, 
        AUTOKEY.opargs_seg: ",", 

        AUTOKEY.operation_pre: multiText_info_operation_pre_list, 
        AUTOKEY.operation: multiText_info_operation_list, 
        AUTOKEY.no_check: True
    }
}

multiText_info = brace_add_info(multiText_info)
multiText_info = args_opargs_add_info(multiText_info)