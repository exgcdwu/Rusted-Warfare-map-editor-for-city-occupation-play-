import os
import sys
from collections import OrderedDict
from copy import deepcopy

current_file_path = os.path.abspath(__file__)
current_dir_path = os.path.dirname(current_file_path)
auto_dir_path = os.path.dirname(current_dir_path)
package_dir = os.path.dirname(auto_dir_path)
sys.path.append(package_dir)
import rwmap as rw

from command.objectgroupauto._core import AUTOKEY
from command.objectgroupauto._data._const import *
from command.objectgroupauto._data._object import *

time_info_args_dict = OrderedDict()

time_info_args_dict[INFOKEY.prefix] = str
time_info_args_dict[INFOKEY.istime] = bool
time_info_args_dict[INFOKEY.iscorrectwarmup] = bool
time_info_args_dict[INFOKEY.timeratio] = str

time_info_default_args_dict = {
    INFOKEY.istime: "true", 
}

time_info_var_dependent_dict = {
    INFOKEY.iscorrectwarmup: INFOKEY.istime, 
    INFOKEY.timeratio: INFOKEY.istime, 
}

time_info_optional_set = {
    INFOKEY.istime, INFOKEY.iscorrectwarmup, 
}

def self_assign_operation_list(key:str, info_tag:str):
    return \
    operation_exist_if(f"{key}", info_tag + "_existif_selfassign_" + key) + \
        operation_typeset_expression(f"{key}", f"{key}") + \
    operation_ifend(info_tag + "_existif_selfassign_" + key)

def time_ratio_operation_list(key:str, info_tag:str):
    return \
    operation_exist_if(f"{key}", info_tag + "_existif_time_" + key) + \
        operation_typeset_expression(f"{key}", "(" + nbr(":.2f") + f").format(float('{key}'[:-1]) * {INFOKEY.timeratio}) + 's'") + \
    operation_ifend(info_tag + "_existif_time_" + key)

def time_list_ratio_operation_list(key:str, info_tag:str):
    return \
    operation_exist_if(f"{key}", info_tag + "_existif_time_list_" + key) + \
        operation_typeset_expression(f"{key}", "[(" + nbr(":.2f") + ").format((float(timeratio_now[:-1]) * timeratio)) + 's' " + f"for timeratio_now in {key}]") + \
    operation_ifend(info_tag + "_existif_time_list_" + key)

def sum_list(list_now:list):
    list_temp = []
    for ele_list in list_now:
        list_temp = list_temp + ele_list
    return list_temp

def time_operation_list(info_tag:str, warmup_keylist:list, warmuplist_keylist:list, reset_keylist:list, resetlist_keylist:list):
    return \
    operation_if(f"{INFOKEY.istime}", info_tag + "_if_istime") + \
        operation_if(INFOKEY.iscorrectwarmup, info_tag + "_if_assign_iscorrectwarmup") + \
        sum_list([self_assign_operation_list(warmup, info_tag) for warmup in warmup_keylist]) + \
        sum_list([self_assign_operation_list(warmuplist, info_tag) for warmuplist in warmuplist_keylist]) + \
        operation_ifend(info_tag + "_if_assign_iscorrectwarmup") + \
            sum_list([self_assign_operation_list(reset, info_tag) for reset in reset_keylist]) + \
            sum_list([self_assign_operation_list(resetlist, info_tag) for resetlist in resetlist_keylist]) + \
        operation_if(INFOKEY.iscorrectwarmup, info_tag + "_if_iscorrectwarmup") + \
        sum_list([time_ratio_operation_list(warmup, info_tag) for warmup in warmup_keylist]) + \
        sum_list([time_list_ratio_operation_list(warmuplist, info_tag) for warmuplist in warmuplist_keylist]) + \
        operation_ifend(info_tag + "_if_iscorrectwarmup") + \
            sum_list([time_ratio_operation_list(reset, info_tag) for reset in reset_keylist]) + \
            sum_list([time_list_ratio_operation_list(resetlist, info_tag) for resetlist in resetlist_keylist]) + \
    operation_ifend(info_tag + "_if_istime")

def time_info_sub(info_dict:str, warmup_keylist:list, warmuplist_keylist:list, reset_keylist:list, resetlist_keylist:list)->dict:
    info_dict_ans = deepcopy(info_dict)
    for key, value in info_dict_ans.items():
        value[AUTOKEY.info_args].update(time_info_args_dict)
        value[AUTOKEY.info_args][INFOKEY.time_prefix] = str
        time_operation_list_now = time_operation_list(key, warmup_keylist, warmuplist_keylist, reset_keylist, resetlist_keylist)
        if value.get(AUTOKEY.operation) == None:
            value[AUTOKEY.operation] = []
        value[AUTOKEY.operation] = time_operation_list_now + value[AUTOKEY.operation]
        if value.get(AUTOKEY.default_args) == None:
            value[AUTOKEY.default_args] = {}
        value[AUTOKEY.default_args].update(time_info_default_args_dict)
        value[AUTOKEY.default_args][INFOKEY.istime] = "false"
        if value.get(AUTOKEY.var_dependent) == None:
            value[AUTOKEY.var_dependent] = {}
        value[AUTOKEY.var_dependent].update(time_info_var_dependent_dict)
        if value.get(AUTOKEY.optional) == None:
            value[AUTOKEY.optional] = set()
        value[AUTOKEY.optional].update(time_info_optional_set)
        value[AUTOKEY.optional].update({INFOKEY.time_prefix,})
        if value.get(AUTOKEY.info_prefix) == None:
            value[AUTOKEY.info_prefix] = {}
        value[AUTOKEY.info_prefix].update({INFOKEY.time_info: INFOKEY.time_prefix})
    return info_dict_ans

time_info = {
    INFOKEY.time_info:{
        AUTOKEY.info_args:time_info_args_dict, 
        AUTOKEY.default_args:time_info_default_args_dict, 
        AUTOKEY.var_dependent: time_info_var_dependent_dict, 
        AUTOKEY.optional: time_info_optional_set, 
        AUTOKEY.prefix: INFOKEY.prefix, 
        AUTOKEY.isinfo_sub: True
    }
}

