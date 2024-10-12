from typing import Union
from copy import deepcopy
import regex as re
import os
from pprint import pprint
import argparse
import importlib
from collections import OrderedDict
import sys
import pdb
import json
import xml.etree.ElementTree as et
import time
import shutil

from asteval import Interpreter

current_file_path = os.path.abspath(__file__)
current_dir_path = os.path.dirname(current_file_path)
package_dir = os.path.dirname(current_dir_path)

sys.path.append(package_dir)
import rwmap as rw

CLASS_DICT = {
    "str": str, 
    "bool": bool
}

def aeval_globals(name):
    return CLASS_DICT[name]

USER_SYMBOLS = {"aeval_globals": aeval_globals, "e": "e", "id": "id"}
MAXTRANSDEPTH = 1024

class AUTOKEY:
    info_args = "info_args"
    default_args = "default_args"
    prefix = "prefix"
    info = "info"
    info_key = "info_key"
    isinfo_sub = "isinfo_sub"
    args = "args"
    seg = "seg"
    opargs = "opargs"
    opargs_seg = "opargs_seg"
    opargs_prefix_len = "opargs_prefix_len"
    ids = "ids"
    IDs = "IDs"
    IDfa = "IDfa"
    IDdep = "IDdep"
    operation = "operation"
    tobject = "tobject"
    offset = "offset"
    offsetsize = "offsetsize"
    name = "name"
    type = "type"
    optional = "optional"
    exist = "exist"
    death = "death"
    isprefixseg = "isprefixseg"
    isdelete_sym = "isdelete_sym"
    isdelete_all_sym = "isdelete_all_sym"
    info_prefix = "info_prefix"
    initial_brace = "initial_brace"
    default_brace = "default_brace"
    var_dependent = "var_dependent"
    no_check = "no_check"
    cite_name = "cite_name"
    depth = "depth"
    tobject_id = "tobject_id"
    tobject_name = "tobject_name"
    brace_exp_depth = "brace_exp_depth"
    errorif = "errorif"

    operation_type = "operation_type"
    object = "object"
    goto = "goto"
    ifend_tag = "ifend_tag"
    goto_tag = "goto_tag"
    tag = "tag"
    setvar = "setvar"
    typeif = "typeif"
    ifvar = "ifvar"
    typeset = "typeset"
    typeset_id = "typeset_id"
    info_name = "info_name"

    changetype = "changetype"
    totype = "totype"
    typeset_expression = "typeset_expression"
    typeset_exist = "typeset_exist"
    keyname_list = "keyname_list"
    operation_pre = "operation_pre"
    real_idexp = "real_idexp"
    typeadd_args = "typeadd_args"
    typeadd_opargs = "typeadd_opargs"
    typedelete_optional = "typedelete_optional"
    namedelete_optional = "namedelete_optional"
    typeadd_optional = "typeadd_optional"
    nameadd_optional = "nameadd_optional"
    exist = "exist"
    brace = "brace"
    pdb_pause = "pdb_pause"
    error = "error"
    error_info = "error_info"
    isnot_cite_check = "isnot_cite_check"
    is_cite_white_list = "is_cite_white_list"

    opargs_sys_seg = "|"
    IDs_seg = ","
    delete_op = ",d"
    delete_all_op = ",D"

    info_re = ".*_info"
    delete_symbol = ".*,d"
    delete_all_symbol = ".*,D"
    not_useful_char = "[^\u4e00-\u9fa5A-Za-z0-9_{}]"
    not_useful_char_ad_point = "[^\u4e00-\u9fa5A-Za-z0-9_{}.]"
    not_useful_char_ad_point_for_cite = "[^\u4e00-\u9fa5A-Za-z0-9_{}.]|(?<=[.][\u4e00-\u9fa5A-Za-z0-9_{}]*)[.]"
    language_seg = "|"

cite_object_dict = {}

language_dict = {"eg" : 0, "ch" : 1}
language_set = set(language_dict.keys())

full_screen = int(shutil.get_terminal_size().columns / 2) * 2
underline_even_num = int(full_screen * 3 / 8) * 2

def search_cite(prefix):
    results = {}
    for key in cite_object_dict:
        if key.startswith(prefix):
            results[key] = cite_object_dict[key]
    return results

def str_lang(info_str:str)->str:
    language_index = language_dict[language]
    info_list = info_str.split(AUTOKEY.language_seg)
    if len(info_list) != len(language_set):
        debug_pdb("standard print error(language).")
    return info_list[language_index]

def standard_out(ifdo:bool, info_str)->None:
    if ifdo:
        if isinstance(info_str, str):
            print(str_lang(info_str))
        else:
            pprint(info_str)

def weighted_char_count(s):
    weight = 0
    for char in s:
        if '\u4e00' <= char <= '\u9fff':  # 检测汉字的Unicode范围
            weight += 2
        else:
            weight += 1
    return weight

def standard_out_underline(ifdo:bool, info_str:str)->None:
    info_str_now = str_lang(info_str)
    lenstr = weighted_char_count(info_str_now)
    if ifdo:
        if lenstr % 2 != 0:
            info_str_now = info_str_now + "-"
            lenstr = lenstr + 1

        left_bk = int(full_screen / 2 - underline_even_num / 2)
        left_ul = int(underline_even_num / 2 - lenstr / 2)
        right_ul = left_ul

        print(" " * left_bk + "-" * underline_even_num)
        print(" " * left_bk + "-" * left_ul + info_str_now + "-" * right_ul)
        print(" " * left_bk + "-" * underline_even_num)

def standard_error(info_err, error_id:int, ID_now:str = None, name_now:str = None, x_now:str = None, y_now:str = None, sub_info_error:str = None)->None:
    ID_now_l = str_lang(f", ID:{ID_now}|, ID:{ID_now}") if ID_now != None else ""
    name_now_l = str_lang(f", name:{name_now}|, 名称:{name_now}") if name_now != None else ""
    xy_now_l = str_lang(f", coordinate:({x_now}, {y_now})|, 坐标:({x_now}, {y_now})") if x_now != None else ""
    error_l = str_lang(f", ERROR:{error_id}|, 错误码:{error_id}")
    str_error_default = "(" + f"{ID_now_l}{name_now_l}{xy_now_l}{error_l}"[2:] + ")"
    print(str_lang(info_err) + str_error_default, file=sys.stderr)
    if sub_info_error != None:
        pprint(sub_info_error)
    if isdebug:
        import pdb;pdb.set_trace()
    exit(error_id)

def standard_warning(info_warn, warn_id:int, error_id:int, ID_now:str = None, name_now:str = None, x_now:str = None, y_now:str = None, sub_info_warn:str = None)->None:
    ID_now_l = str_lang(f", ID:{ID_now}|, ID:{ID_now}") if ID_now != None else ""
    name_now_l = str_lang(f", name:{name_now}|, 名称:{name_now}") if name_now != None else ""
    xy_now_l = str_lang(f", coordinate:({x_now}, {y_now})|, 坐标:({x_now}, {y_now})") if x_now != None else ""
    warn_l = str_lang(f", WARNING:{warn_id}|, 警告码:{warn_id}")
    str_warning_default = "(" + f"{ID_now_l}{name_now_l}{xy_now_l}{warn_l}"[2:] + ")"
    print(str_lang(info_warn) + str_warning_default, file=sys.stdout)
    if sub_info_warn != None:
        pprint(sub_info_warn)
    if isdebug:
        import pdb;pdb.set_trace()
    if not ignorewarning:
        exit(error_id)

def debug_dict(dict_now:dict, name:str):
    if isdebug:
        pprint(f"{name} = " + str(dict_now.get(name)))

def debug_pdb(thing = ""):
    if isdebug: 
        if isinstance(thing, str):
            print(thing)
        else:
            pprint(thing)
        import pdb;pdb.set_trace()

def id_debug_pdb(tobject:rw.case.TObject, ID:int):
    if isdebug and tobject.returnDefaultProperty("id") == str(ID):
        import pdb;pdb.set_trace()


def get_args(info:dict, name:str, tobject:rw.case.TObject, info_tobject:rw.case.TObject, object_dict:dict)->dict:
    args_dict = {}
    split_now = name.split(info[AUTOKEY.opargs_seg])
    opargs = split_now[1:]

    if split_now[0] == "":
        args_n = []
    else:
        args_n = split_now[0].split(info[AUTOKEY.seg])
    
    tobject_id = tobject.returnDefaultProperty("id")
    tobject_name = tobject.returnDefaultProperty("name")
    tobject_x = tobject.returnDefaultProperty("x")
    tobject_y = tobject.returnDefaultProperty("y")
    info_tobject_id = info_tobject.returnDefaultProperty("id")
    info_tobject_name = info_tobject.returnDefaultProperty("name")
    info_tobject_x = info_tobject.returnDefaultProperty("x")
    info_tobject_y = info_tobject.returnDefaultProperty("y")
    
    if len(args_n) < len(info[AUTOKEY.args]):
        info_args_temp = info[AUTOKEY.args][len(args_n):]
        standard_error(f"Required arguments are missing below in a tagged object.(maybe \".\" is missing?)(name:{name},need:{info[AUTOKEY.args]},reality:{args_n})(info name:{info_tobject_name},info id:{info_tobject_id},info coordinate:({info_tobject_x}, {info_tobject_y}))" + \
                       f"|标记宾语中的必需参数缺失。(也许\".\"缺失？)(扣除前缀后的名称:{name},必需参数要求:{info[AUTOKEY.args]},必需参数实际:{args_n})(info 名称:{info_tobject_name},info ID:{info_tobject_id},info 坐标:({info_tobject_x}, {info_tobject_y}))", 
                       8, tobject_id, tobject_name, tobject_x, tobject_y, info_args_temp)
    elif len(args_n) > len(info[AUTOKEY.args]):
        info_args_temp = args_n[len(info[AUTOKEY.args]):]
        standard_error(f"Too many required arguments below in a tagged object.(name:{name},need:{info[AUTOKEY.args]},reality:{args_n})(info name:{info_tobject_name},info id:{info_tobject_id},info coordinate:({info_tobject_x}, {info_tobject_y}))" + \
                       f"|标记宾语中的必需参数过多。(扣除前缀后的名称:{name},必需参数要求:{info[AUTOKEY.args]},必需参数实际:{args_n})(info 名称:{info_tobject_name},info ID:{info_tobject_id},info 坐标:({info_tobject_x}, {info_tobject_y}))", 
                       9, tobject_id, tobject_name, tobject_x, tobject_y, info_args_temp)

    for index, thing in enumerate(info[AUTOKEY.args]):
        args_dict[thing[0]] = thing[1](args_n[index])
    
    prefix_len = info[AUTOKEY.opargs_prefix_len]

    for info_thing in info[AUTOKEY.opargs].values():
        if len(info_thing[0].split(AUTOKEY.opargs_sys_seg)) == 2:
            key_now = info_thing[0].split(AUTOKEY.opargs_sys_seg)[0]
            opdefault_now = info_thing[0].split(AUTOKEY.opargs_sys_seg)[1]
            type_now = info_thing[1]
            if object_dict.get(key_now) != None:
                continue
            args_dict[key_now] = mapvalue_to_value(opdefault_now, type_now)


    for oparg in opargs:
        prefix_now = oparg[0:prefix_len]
        var_now = oparg[prefix_len:]
        if info[AUTOKEY.opargs].get(prefix_now) != None:
            info_thing = info[AUTOKEY.opargs][prefix_now]
            key_now = info_thing[0].split(AUTOKEY.opargs_sys_seg)[0]
            type_now = info_thing[1]

            if type_now == bool:
                deal_bool = True if var_now == "" else mapvalue_to_value(var_now, type_now)
                args_dict[key_now] = (deal_bool ^ object_dict[key_now]) if object_dict.get(key_now) != None else deal_bool
            else:
                if var_now == "None":
                    continue
                args_dict[key_now] = type_now(var_now)
        else:
            if prefix_now != "d" and prefix_now != 'D':
                standard_error(f"Unknown optional arguments in a tagged object.(name:{name}, optional tag:,{prefix_now})" + \
                               f"|在标记宾语中出现的可选参数无法识别。(扣除前缀后的名称:{name}, 问题可选前缀:,{prefix_now})", 7, tobject_id, tobject_name, tobject_x, tobject_y)

    tobject_ids = tobject.returnOptionalProperty(AUTOKEY.IDs)
    tobject_ids = tobject_ids.split(AUTOKEY.IDs_seg) if (tobject_ids != None and tobject_ids != '') else []
    args_dict[AUTOKEY.IDs] = tobject_ids

    return args_dict

def match_compare(match_value:list)->int:
    return -match_value[0].start()

def brace_one_str(value):
    if isinstance(value, dict):
        value_list = [[v1, v2] for v1, v2 in value.items()]
        return "dict(" + str(value_list) + ")"
    else:
        if isinstance(value, set):
            value_list = [v1 for v1 in value]
            return "set(" + str(value_list) + ")"
        else:
            return str(value)

def brace_one_translation(expression_b:str, dict_name:dict, seg_re:str)->str:
    
    expression_b = " " + expression_b + " "

    expression_b_seg_index = [match_now.start() for match_now in re.finditer(seg_re, expression_b)]
    match_now_list = [(expression_b_seg_index[index] + 1, expression_b_seg_index[index + 1]) for index in range(len(expression_b_seg_index) - 1)]
    brace_one_list = [expression_b[match_now[0]:match_now[1]] for match_now in match_now_list]
    brace_one_list = [brace_one if dict_name.get(brace_one) == None else brace_one_str(dict_name[brace_one]) for brace_one in brace_one_list]
    expression_b_ans = ""
    for index in range(len(brace_one_list)):
        expression_b_ans = expression_b_ans + expression_b[expression_b_seg_index[index]] + brace_one_list[index]
    expression_b_ans = expression_b_ans[1:]
    return expression_b_ans

def brace_one_translation_cycle(expression_b:str, dict_name:dict, seg_re:str)->str:
    expression_b_temp = ""
    while expression_b_temp != expression_b:
        expression_b_temp = expression_b
        expression_b = brace_one_translation(expression_b, dict_name, seg_re)
    return expression_b

def brace_translation(expression_b:str, dict_name:dict, prev:bool = True, depth = MAXTRANSDEPTH, brace_exp_depth:int = MAXTRANSDEPTH):
    if brace_exp_depth == 0:
        return expression_b
    #import pdb;pdb.set_trace()
    expression_b_origin = expression_b
    expression_b = brace_one_translation_cycle(expression_b, cite_object_dict, AUTOKEY.not_useful_char_ad_point_for_cite)
    expression_b_origin_now = expression_b
    expression_b = brace_one_translation(expression_b, dict_name, AUTOKEY.not_useful_char_ad_point)
    trans_dep_now = 1
    while(trans_dep_now < depth):
        if expression_b_origin_now == expression_b:
            break
        expression_b_origin_now = expression_b
        expression_b = brace_one_translation_cycle(expression_b, cite_object_dict, AUTOKEY.not_useful_char_ad_point_for_cite)
        if expression_b_origin_now == expression_b:
            break
        expression_b_origin_now = expression_b
        expression_b = brace_one_translation(expression_b, dict_name, AUTOKEY.not_useful_char_ad_point)

        trans_dep_now = trans_dep_now + 1

    tobject:rw.case.TObject = dict_name["tobject"]
    tobject_id = tobject.returnDefaultProperty("id")
    tobject_name = tobject.returnDefaultProperty("name")
    tobject_x = tobject.returnDefaultProperty("x")
    tobject_y = tobject.returnDefaultProperty("y")

    if trans_dep_now == MAXTRANSDEPTH:
        standard_error(f"References occur in a loop(more than 1024).({expression_b})" + \
                       f"|宾语内引用发生了循环(超过1024次)。({expression_b})", 16, tobject_id, tobject_name, tobject_x, tobject_y)

    if (prev or expression_b_origin != expression_b):
        expression_b = expression_translation(expression_b, dict_name, False, brace_exp_depth = brace_exp_depth - 1)
    try:
        expression_b_temp = aeval(expression_b)
    except Exception as e:
        return expression_b
    else:
        if expression_b_temp == None:
            return expression_b
        return expression_b_temp

def expression_translation(expression_s:str, dict_name:dict, prev:bool = True, depth = MAXTRANSDEPTH, brace_exp_depth:int = MAXTRANSDEPTH):
    if brace_exp_depth == 0:
        return expression_s
    expression_s_now = str_translation(expression_s, dict_name)
    if (prev or expression_s != expression_s_now):
        return brace_translation(expression_s_now, dict_name, False, depth = depth, brace_exp_depth = brace_exp_depth - 1)
    else:
        return expression_s_now
        
    


def str_translation(value:Union[str, bool], dict_name:dict)->str:
    if isinstance(value, bool):
        return value_to_mapvalue(value, bool)
    if isinstance(value, dict):
        return deepcopy(value)
    left_index = -1
    left_brace = 0
    index_list = []
    for index in range(0, len(value)):
        if left_brace == -1:
            raise ValueError("The string have '}' but don't have '{'.")
        if value[index] == "{":
            if left_index == -1:
                left_index = index
            left_brace = left_brace + 1
        elif value[index] == "}":
            left_brace = left_brace - 1
            if left_brace == 0:
                right_index = index
                if index + 1 < len(value) and value[index + 1] == '&':
                    depth = int(value[index + 2])
                    brace_exp_brace = int(value[index + 3])
                    index_list.append((left_index, right_index, depth, brace_exp_brace))
                else:
                    index_list.append((left_index, right_index))
                left_index = -1
    if left_brace > 0:
        raise ValueError("The string have '{' but don't have '}'.")
    if index_list == []:
        return value
    value_ans = value[0:index_list[0][0]]
    index_list.append((len(value), len(value)))
    for index in range(len(index_list) - 1):
        if len(index_list[index]) == 2:
            value_ans = value_ans + type_to_str(brace_translation(value[index_list[index][0] + 1:index_list[index][1]], dict_name), str) + value[index_list[index][1] + 1:index_list[index + 1][0]]
        else:
            value_ans = value_ans + type_to_str(brace_translation(value[index_list[index][0] + 1:index_list[index][1]], dict_name, depth = index_list[index][2], brace_exp_depth = index_list[index][3]), str) + value[index_list[index][1] + 4:index_list[index + 1][0]]
    return value_ans

lower_bool_dict = {
    "True": True, 
    "False": False, 
    "true": True, 
    "false": False
}

def lower_bool(value:str)->str:
    if not isinstance(value, dict) and lower_bool_dict.get(value) != None:
        return value_to_mapvalue(lower_bool_dict[value], bool)
    else:
        return value

def tobject_args_translation(key:str, value:str, dict_name:dict)->dict:
    dict_ans = {}
    if isinstance(value, tuple):
        if value[2] == AUTOKEY.brace:
            if brace_translation(value[1], dict_name) == True:
                dict_ans = {key:str_translation(value[0], dict_name)}
        elif value[2] == AUTOKEY.exist:
            value_list = value[1].split(",")
            isend = True
            for value_n in value_list:
                if dict_name.get(value_n) == None or str_translation("{" + value_n + "}", dict_name) == 'None':
                    isend = False
                    break
            if isend:
                dict_ans = {key:str_translation(value[0], dict_name)}
        
    else:
        dict_ans =  {key:str_translation(value, dict_name)}

    for key_d, value_d in dict_ans.items():
        dict_ans[key_d] = lower_bool(value_d)

    return dict_ans

def get_tobject(operation:dict, dict_name:dict, ori_pos:rw.frame.Coordinate, ori_size:rw.frame.Coordinate)->rw.case.TObject:
    
    if operation.get(AUTOKEY.exist) != None:
        for exist_now in operation[AUTOKEY.exist]:
            if dict_name.get(exist_now) == None or dict_name.get(exist_now) != True:
                return None
    if operation.get(AUTOKEY.death) != None:
        for death_now in operation[AUTOKEY.death]:
            if dict_name.get(death_now) != None and dict_name.get(death_now) == True:
                return None
    
    offset = operation.get(AUTOKEY.offset)
    if offset != None:
        offset = brace_translation(offset, dict_name)
        offset = rw.frame.Coordinate(offset[0], offset[1])
    else:
        offset = rw.frame.Coordinate()

    offsetsize = rw.frame.Coordinate()
    offsetsize = operation.get(AUTOKEY.offsetsize)
    if offsetsize != None:
        offsetsize = brace_translation(offsetsize, dict_name)
        offsetsize = rw.frame.Coordinate(offsetsize[0], offsetsize[1])
    else:
        offsetsize = rw.frame.Coordinate()
    pos = ori_pos + offset
    size = ori_size + offsetsize

    default_pro = {
        rw.const.OBJECTDE.x: str(pos.x()), 
        rw.const.OBJECTDE.y: str(pos.y()), 
        rw.const.OBJECTDE.width: str(size.x()), 
        rw.const.OBJECTDE.height: str(size.y())
    }
    if operation.get(AUTOKEY.name) != None:
        default_pro.update(tobject_args_translation(rw.const.OBJECTDE.name, operation[AUTOKEY.name], dict_name))
    if operation.get(AUTOKEY.type) != None:
        default_pro.update(tobject_args_translation(rw.const.OBJECTDE.type, operation[AUTOKEY.type], dict_name))

    optional_pro = {}
    if operation.get(AUTOKEY.optional) != None:
        for key, value in operation[AUTOKEY.optional].items():
            optional_pro.update(tobject_args_translation(key, value, dict_name))

    return rw.case.TObject("object", default_pro, optional_pro)

def mapvalue_to_value(value, ntype):
    if isinstance(value, dict):
        if value["type"] == "bool":
            value_now = ntype(True) if (value["value"] == "true" or value["value"] == "True") else ntype(False) 
            if isinstance(value_now, str):
                value_now = value_now.lower()
            return value_now
    else:
        if ntype == bool:
            value_now = str(value)
            if (value_now == "true" or value_now == "True"):
                value_now = True
            elif (value_now == "false" or value_now == "False"):
                value_now = False
            else:
                value_now = value_now
            return value_now
        elif isinstance(ntype, tuple):
            if ntype[0] == list:
                if ntype[1] == str:
                    value_now = value.split(",")
                elif ntype[1] == int:
                    value_now = value.split(" ")
                    value_now = [int(value_now_i) for value_now_i in value_now]
                elif ntype[1] == list:
                    if ntype[2] == str:
                        value_now = [value_i.split(",") for value_i in value.split(";")]
                    elif ntype[2] == int:
                        value_now = [[int(value_ij) for value_ij in value_i.split(" ")] for value_i in value.split(",")]
            return value_now
        value_now = lower_bool_dict.get(value)
        return value_now if value_now != None else value

def value_to_mapvalue(value, ntype):
    if ntype == bool:
        return {"value": str(bool(value)).lower(), "type": "bool"}
    if isinstance(ntype, tuple):
        if ntype[0] == list:
            if ntype[1] == str:
                    value_now = ",".join(value)
            elif ntype[1] == int:
                value = [str(value_i) for value_i in value]
                value_now = " ".join(value)
            elif ntype[1] == list:
                if ntype[2] == str:
                    value_now = ";".join([",".join(value_i) for value_i in value])
                elif ntype[2] == int:
                    value_now = [[str(value_ij) for value_ij in value_i] for value_i in value]
                    value_now = ",".join([" ".join(value_i) for value_i in value_now])
            return value_now
        return value
    
def mapvalue_to_value_basic(value):
    if isinstance(value, dict):
        return mapvalue_to_value(value, bool)
    else:
        return mapvalue_to_value(value, str)
    
def value_to_mapvalue_basic(value):
    return value_to_mapvalue(value, get_type(value))

def get_type(value):
    if isinstance(value, list):
        if len(value) == 0 or isinstance(value[0], str):
            return (list, str)
        elif isinstance(value[0], int):
            return (list, int)
        elif isinstance(value[0], list):
            if len(value[0]) == 0 or isinstance(value[0][0], str):
                return (list, list, str)
            elif isinstance(value[0][0], int):
                return (list, list, int)
    else:
        return type(value)

def type_to_str(value, ntype):
    if isinstance(ntype, tuple):
        if ntype[0] == list:
            if ntype[1] == str:
                value_now = ",".join(value)
            elif ntype[1] == int:
                value = [str(value_i) for value_i in value]
                value_now = " ".join(value)
            elif ntype[1] == list:
                if ntype[2] == str:
                    value_now = ";".join([",".join(value_i) for value_i in value])
                elif ntype[2] == int:
                    value_now = [[str(value_ij) for value_ij in value_i] for value_i in value]
                    value_now = ",".join([" ".join(value_i) for value_i in value_now])
            return value_now
    else:
        return str(value)
    
def str_to_type(value, ntype):
    if isinstance(ntype, tuple):
        if ntype[0] == list:
            if ntype[1] == str:
                value_now = value.split(",")
            elif ntype[1] == int:
                value_now = value.split(" ")
                value_now = [int(value_now_i) for value_now_i in value_now]
            elif ntype[1] == list:
                if ntype[2] == str:
                    value_now = [value_i.split(",") for value_i in value.split(";")]
                elif ntype[2] == int:
                    value_now = [[int(value_ij) for value_ij in value_i.split(" ")] for value_i in value.split(",")]
            return value_now
    elif ntype == bool:
        value_now = True if value == "True" else False
    else:
        return ntype(value)
    

def IDs_update(tagged_tobject:rw.case.TObject, tobject_now:rw.case.TObject)->None:
    idsh = tagged_tobject.returnOptionalProperty(AUTOKEY.IDs)
    if idsh == None:
        idsh = ""
    if idsh == "":
        idsh = tobject_now.returnDefaultProperty("id")
    else:
        idsh = idsh + AUTOKEY.IDs_seg + tobject_now.returnDefaultProperty("id")
    tagged_tobject.assignOptionalProperty(
        AUTOKEY.IDs, 
        idsh
    )

def IDs_balance(tobject_now:rw.case.TObject, tottob:int)->list:
    idsh = tobject_now.returnOptionalProperty(AUTOKEY.IDs)
    if idsh == None or idsh == '':
        idsh_list = []
    else:
        idsh_list = idsh.split(",")
    idsh = ",".join(idsh_list[0:min(tottob, len(idsh_list))])
    tobject_now.assignOptionalProperty(
        AUTOKEY.IDs, 
        idsh
    )

    id_delete = idsh_list[min(tottob, len(idsh_list)):]

    return id_delete

def is_tagged_tobject__newname__myinfo__info(tobject_name:str, info_dict, info_now):
    ischange = False
    myinfo = {}
    info = {}
    tobject_name_to_solve = ""
    for key, info in info_dict.items():
        prefix_now = info[AUTOKEY.prefix]
        info_key = info[AUTOKEY.info]
        myinfo = info_now[info_key]

        if info.get(AUTOKEY.isprefixseg) != None and info.get(AUTOKEY.isprefixseg) == True:
            prefix_to_match = tobject_name.split(myinfo[AUTOKEY.seg])[0]
            tobject_name_to_solve = tobject_name[len(prefix_to_match) + 1:]
            if prefix_now == prefix_to_match:
                ischange = True
                break
        else:
            prefix_to_match = tobject_name[0:len(prefix_now)]
            tobject_name_to_solve = tobject_name[len(prefix_to_match):]
            if prefix_now == prefix_to_match \
                and (not re.match(AUTOKEY.info_re, tobject_name)):
                ischange = True
                break
    return (ischange, tobject_name_to_solve, myinfo, info)

def is_tagged_tobject(tobject:rw.case.TObject, info_dict, info_now):
    tobject_name = tobject.returnDefaultProperty(rw.const.OBJECTDE.name)
    ischange__newname__myinfo__info = is_tagged_tobject__newname__myinfo__info(tobject_name, info_dict, info_now)
    ischange = ischange__newname__myinfo__info[0]
    return ischange


def tobject_ids_do(tobject:rw.case.TObject, myinfo, info, ids_now_dict, isreset, id_to_tobject):
    iddep = tobject.returnOptionalProperty(AUTOKEY.IDdep)
    idfa = tobject.returnOptionalProperty(AUTOKEY.IDfa)
    id_now = tobject.returnDefaultProperty("id")
    tobject_name = tobject.returnDefaultProperty("name")

    tobject_id = tobject.returnDefaultProperty("id")
    tobject_x = tobject.returnDefaultProperty("x")
    tobject_y = tobject.returnDefaultProperty("y")

    if iddep != None and iddep != "0":
        tobject_idfa:rw.case.TObject = id_to_tobject.get(idfa)
        if tobject_idfa == None:
            standard_warning(f"A tagged object created by tree tagged object can't find its parent object, then this tagged object will be unavailable.(parent ID:{idfa}, IDdep:{iddep})" + \
                             f"|一个树标记宾语产生的标记宾语不能找到它父亲的宾语，然后该标记宾语无法使用。(父亲 ID:{idfa}, 高度:{iddep})", 
                             2, 19, tobject_id, tobject_name, tobject_x, tobject_y)
        elif int(tobject_idfa.returnOptionalProperty(AUTOKEY.IDdep)) != int(iddep) - 1:
            standard_error(f"The depth of tagged objects is disordered.(IDdep:{iddep}), parent ID:{idfa}, parent IDdep:({tobject_idfa.returnOptionalProperty(AUTOKEY.IDdep)})" + \
                           f"|标记宾语在树中的高度出现错误。(高度:{iddep}), 父亲 ID:{idfa}, 父亲高度:({tobject_idfa.returnOptionalProperty(AUTOKEY.IDdep)})", 
                           17, tobject_id, tobject_name, tobject_x, tobject_y)
        elif not id_now in tobject_idfa.returnOptionalProperty(AUTOKEY.IDs).split(","):
            standard_warning(f"A tree tagged object can't find its child object, although the child object has its father, then this child object will be unavailable.(parent ID:{idfa}, child IDs:{tobject_idfa.returnOptionalProperty(AUTOKEY.IDs)})" + \
                             f"|一个树标记宾语无法找到它的孩子标记宾语，虽然该孩子宾语有自己的父亲树宾语，然后该标记宾语无法使用。(父亲 ID:{idfa},孩子 IDs:{tobject_idfa.returnOptionalProperty(AUTOKEY.IDs)})", 
                             3, 20, tobject_id, tobject_name, tobject_x, tobject_y)
        
    for thing_prefix_num in myinfo[AUTOKEY.ids]:
        prefix_now = brace_translation(thing_prefix_num[0], info)
        tobject_prefix = tobject.returnOptionalProperty(prefix_now)
        if tobject_prefix != None:
            tobject_prefix = tobject_prefix.split(",")
        else:
            tobject_prefix = []
        if isreset:
            tobject_prefix = []
            tobject.deleteOptionalPropertySup([AUTOKEY.IDs, AUTOKEY.IDfa, AUTOKEY.IDdep])
        if ids_now_dict.get(prefix_now) == None:
            ids_now_dict[prefix_now] = 1
        
        for index in range(len(tobject_prefix)):
            tobject_prefix[index] = int(tobject_prefix[index][len(prefix_now):])
            ids_now_dict[prefix_now] = max(ids_now_dict[prefix_now], 
                                                    tobject_prefix[index] + 1)

def is_tagged_object_simple(tobject:rw.case.TObject):
    object_type = tobject.returnDefaultProperty(rw.const.OBJECTDE.type)
    isnewtaggedobject = (object_type == None or re.match("^$", object_type))
    return isnewtaggedobject

def isdigit_str(s):
    return s.isdigit() or (s[0] == '-' and s[1:].isdigit())

def langstr_add_str(langstr:str, str_now:str):
    return "|".join([langstr + str_now for langstr in langstr.split("|")])

def langstrlist_add(langstr_list:list):
    langstr_matrix = [langstr.split("|") for langstr in langstr_list]
    max_lang = max([len(langstr_list) for langstr_list in langstr_matrix])
    langstr_ans = "|".join([''.join([langstr_matrix[i][j] for i in range(len(langstr_matrix)) if j < len(langstr_matrix[i])]) for j in range(max_lang)])
    return langstr_ans

def question(condition:bool, tip:str, chosen_list:list, break_list:set, chosen_dict:dict, isauto = False, auto = None)->bool:
    chosen_set = set(chosen_list)
    break_set = set(break_list)
    chosen = "(" +  "/".join(chosen_list) + ")"
    break_n = "(" +  "/".join(break_list) + ")"
    break_langstr = "Otherwise the program will be terminated.|否则程序终止。"
    tip_now = langstr_add_str(tip, chosen)
    if len(break_list) != 0:
        tip_now = langstrlist_add([tip_now, break_langstr])
        tip_now = langstr_add_str(tip_now, break_n)
    error_langstr = "Identification error, please re-enter.|识别错误，请重新输入。"
    error_langstr = langstr_add_str(error_langstr, chosen)
    if len(break_list) != 0:
        error_langstr = langstrlist_add([error_langstr, break_langstr])
        error_langstr = langstr_add_str(error_langstr, break_n)
    while(condition):
        if isauto:
            standard_out(True, tip_now)
            standard_out(True, f"Automatically enter {auto}.|自动输入{auto}。")
            ispathsame = auto
        else:
            ispathsame = input(str_lang(tip_now))
        
        if chosen_set.issuperset([ispathsame]):
            if chosen_dict.get(ispathsame) != None:
                standard_out(True, chosen_dict[ispathsame])
            if break_set.issuperset([ispathsame]):
                standard_out(True, "Termination of Program.|程序终止。")
                exit(0)
            return ispathsame
        else:
            standard_out(True, error_langstr)

def try_to_deal_id_coincide(map_now:rw.RWmap):
    id_now = 1
    id_mapping = {}
    for objectGroup in map_now._objectGroup_list:
        for tobject in objectGroup._object_list:
            tobject_id = tobject.returnDefaultProperty("id")
            if id_mapping.get(tobject_id) == None:
                id_mapping[tobject_id] = [[tobject, id_now]]
            else:
                id_mapping[tobject_id] = id_mapping[tobject_id] + [[tobject, id_now]]
            id_now = id_now + 1
    map_now.resetnextobjectid(isaboutnextobjectid = False)

    id_coincide_num = 0
    id_coincide_dict = {}
    for objectGroup in map_now._objectGroup_list:
        for tobject in objectGroup._object_list:
            tobject_id = tobject.returnDefaultProperty("id")
            IDs = tobject.returnOptionalProperty(AUTOKEY.IDs)
            IDfa = tobject.returnOptionalProperty(AUTOKEY.IDfa)
            id_temp_list = []
            if IDfa != None:
                id_temp_list.append(IDfa)
            if IDs != None:
                ID_list = IDs.split(",")
                for index, ID_now in enumerate(ID_list):
                    new_ID_list = id_mapping.get(ID_now)
                    if new_ID_list == None:
                        continue
                    elif len(new_ID_list) == 1:
                        continue
                    else:
                        id_temp_list.append(ID_now)
            id_coincide_num = id_coincide_num + len(id_temp_list)    
            if id_temp_list != []:
                    id_coincide_dict[tobject_id] = id_temp_list
    if id_coincide_num == 0:
        standard_out(True, f"Some confusing IDs are coincident to zero and do not need to be adjusted." + 
            f"|混淆ID重合为0，无需调整，正常重排ID。")
    else:
        standard_out(True, f"Some confusing IDs are being outputing." + 
            f"|混淆ID正在输出。")
        for key, value in id_coincide_dict.items():
            print(f"{key}:{value}")
        question(True, f"Some confusing IDs have coincidence, the number:{id_coincide_num}(If the number is too large, it is recommended to fix them manually.). Do you want to correct coincidence?" + 
            f"|混淆ID存在重合，数量为{id_coincide_num}（如果数量很多(比如几百个)，建议外部手动修复）。是否开始解决混淆？", ["y", "n"], ["n"], {}, isyes, "y")


    id_coincide_now = 1
    for objectGroup in map_now._objectGroup_list:
        for tobject in objectGroup._object_list:
            IDs = tobject.returnOptionalProperty(AUTOKEY.IDs)
            IDfa = tobject.returnOptionalProperty(AUTOKEY.IDfa)
            ID_list = []
            if IDfa != None:
                ID_list.append(IDfa)
            if IDs != None:
                ID_list = ID_list + IDs.split(",")
            for index, ID_now in enumerate(ID_list):
                new_ID_list = id_mapping.get(ID_now)
                if new_ID_list == None:
                    ID_list[index] = "999999"
                elif len(new_ID_list) == 1:
                    ID_list[index] = str(new_ID_list[0][1])
                else:
                    
                    chosen_set = [str(num + 1) for num in range(len(new_ID_list))] + ["n"]
                    chosen_dict = dict([[chosen_one, f"{chosen_one}th object has been chosen." + \
                                            f"|第{chosen_one}个宾语已选择。"] for chosen_one in chosen_set])
                    standard_out(True, "Tagged Objects|标记宾语:")
                    print(tobject)
                    standard_out(True, "objects ID Coincide|ID混淆的宾语:")
                    for index_coi in range(len(new_ID_list)):
                        standard_out(True, f"{index_coi + 1}th object|第{index_coi + 1}个混淆宾语:")
                        print(new_ID_list[index_coi][0])
                    chosen_one = question(True, 
                                    f"({id_coincide_now}/{id_coincide_num})Please choose which object is generated by this tagged object.(ID:{ID_now})" + \
                                    f"|({id_coincide_now}/{id_coincide_num})尝试选择哪一个宾语是该标记宾语产生的宾语。(ID:{ID_now})", 
                                    chosen_set, ["n"], chosen_dict)
                    ID_list[index] = str(new_ID_list[int(chosen_one) - 1][1])
                    id_coincide_now = id_coincide_now + 1

                ID_l = 0
                if IDfa != None:
                    IDfa_now = ID_list[0]
                    tobject.assignOptionalProperty(AUTOKEY.IDfa, IDfa_now)
                    ID_l = 1
                if IDs != None:
                    IDs_now = ",".join(ID_list[ID_l:])
                    tobject.assignOptionalProperty(AUTOKEY.IDs, IDs_now)

    id_now = 1
    for objectGroup in map_now._objectGroup_list:
        for tobject in objectGroup._object_list:
            tobject.assignDefaultProperty("id", str(id_now))
            id_now = id_now + 1

def auto_func():
    parser = argparse.ArgumentParser(
        description='Objects of Triggers are automatically processed by information\'s mode.\n' + \
                    '触发器(Triggers)的宾语将会根据信息变量进行自动化处理。')
    parser.add_argument('map_path', action = "store", metavar = 'file', type=str, 
                        help='The input path of RW map file.\n' + \
                            '铁锈地图文件的输入路径。')
    parser.add_argument("--infopath", 
                        action = "store", metavar = "file", type = str, nargs = "?", 
                        required = False, default = current_file_path[:-8] + "_data", 
                        const = current_file_path[:-8] + "_data", 
                        help = "The file's path which has information's mode variable(python package with config.json)|auto/_data\n" + \
                               "信息变量的文件路径。（python包，内含config.json）|auto/_data"
                        )
    parser.add_argument("--infovar", 
                        action = "store", metavar = "name", type = str, nargs = "?", 
                        required = False, default = "auto_func_arg", 
                        const = "auto_func_arg", 
                        help = "The variable name of information\'s mode.|auto_func_arg\n" + \
                                "信息变量的名字。|auto_func_args"
                        )
    
    parser.add_argument("-o", "--output", 
                        action = "store", metavar = "file", type = str, nargs = "?", 
                        required = False, default = "|", 
                        const = "|", 
                        help = "The output path of RW map file.|input path\n" + \
                               "铁锈地图文件的输出路径。"
                        )

    parser.add_argument("-d", "--delete", 
                        action = 'store_true', help = 'Delete the info and tagged objects with ,d.\n' + \
                            "删除带,d标记的info和标记宾语。")

    parser.add_argument("-D", "--DeleteAllSym", 
                        action = 'store_true', help = 'Delete all info and tagged objects.\n' + \
                            "删除所有info宾语和标记宾语。")

    parser.add_argument("--DeleteAll", 
                        action = 'store_true', help = 'Delete all info, tagged objects and relative objects.\n' + \
                            "删除所有info宾语和标记宾语，以及它们产生的宾语。")

    parser.add_argument("-r", "--reset", 
                        action = 'store_true', help = 'Reset the ids of objects.(not recommend)\n' + \
                            "重置宾语的检测id。（非必要不推荐）")

    parser.add_argument("-v", "--verbose", 
                        action = 'store_true', help = 'Detailed output of the prompt message.\n' + \
                            "提供运行信息。")

    parser.add_argument("--debug", 
                        action = 'store_true', help = 'Mode of debuging.\n' + \
                            "进入python debug模式。")

    parser.add_argument("--ignorewarning", 
                        action = 'store_true', help = 'Warning would not exit.\n' + \
                            "警告将不会退出。")
    
    parser.add_argument("--resetid", 
                        action = 'store_true', help = 'Reset the IDs of objects.\n' + \
                            "重置宾语ID。")
    
    parser.add_argument("-c", "--citetrans", 
                        action = 'store_true', help = 'Cite translation.(other objects)\n' + \
                            "对普通宾语进行引用翻译。")
    
    parser.add_argument("-y", "--isyes", 
                        action = 'store_true', help = 'Requests are always y.\n' + \
                            "所有输入请求默认为y，继续执行。")
    
    parser.add_argument("--check", 
                        action = 'store_true', help = 'Perform a detailed inspection. This option has a great impact on performance\n' + \
                            "进行细致的检查，对性能有很大影响。")
    
    parser.add_argument("--language", 
                        action = "store", metavar = "language", type = str, nargs = "?", 
                        required = False, default = "default", 
                        const = "default", 
                        help = "The language of prompt(ch/eg). The language configuration will be stored.(auto/_data/config.json)\n" + \
                        "命令行提示的语言(中文(ch),英文(eg))。语言设置将会被存储。(config.json)"
                        )

    dev_null = open(os.devnull, "w")

    time_all_i = time.time()

    global aeval

    aeval = Interpreter(err_writer = dev_null, writer = dev_null, user_symbols = USER_SYMBOLS)

    args = parser.parse_args()

    global isdebug
    isdebug = args.debug

    global ignorewarning
    ignorewarning = args.ignorewarning

    output_path = args.map_path if args.output == "|" else args.output
    input_path = args.map_path

    module_fa = os.path.dirname(args.infopath)

    module_name = os.path.basename(args.infopath)

    sys.path.append(module_fa)

    info_file = importlib.import_module(module_name)

    info_now_pre = getattr(info_file, args.infovar, 'Not Found')

    isdelete = args.DeleteAllSym
    isdelete_d = args.delete
    isdelete_all = args.DeleteAll
    global isreset
    isreset = args.reset
    isverbose = args.verbose
    global isresetid
    isresetid = args.resetid
    iscitetrans = args.citetrans
    global isyes
    isyes = args.isyes
    global language
    language = args.language
    global isquick
    isquick = not args.check

    if not (language_set.issuperset([language]) or language == "default"):
        print(f"Language is not \"ch\" or \"eg\".({language})\n" + 
              f"语言(--language)不是中文(ch)或者英文(eg)({language})", file=sys.stderr)
        if isdebug:
            import pdb;pdb.set_trace()
        exit(23)

    cf_seg = current_file_path[-9]
    with open(f'{args.infopath}{cf_seg}config.json', 'r') as f:
        config_dict = json.load(f)
    if language != "default":
        config_dict["language"] = language
    else:
        language = config_dict["language"]
    with open(f'{args.infopath}{cf_seg}config.json', 'w') as f:
        json.dump(config_dict, f)

    debug_pdb()

    time_ini_i = time.time()

    standard_out_underline(isverbose, "Initialization|初始化")

    standard_out(isverbose, "Map data is being imported...|地图数据载入...")

    question(input_path == output_path, "The input path is the same as output path. The source file will be overwritten. Do you want to continue?" + \
             "|输入地图路径和输出地图路径相同。原文件将被覆盖。是否要继续？", ["y", "n"], ["n"], {}, isyes, "y")

    try:
        map_now = rw.RWmap.init_mapfile(f'{input_path}')
    except FileNotFoundError:
        standard_error("RW map file is not found, please check your input path.|铁锈输入地图文件未找到，请仔细检查地图路径。", 24)
    except et.ParseError:
        standard_error("File parsing error, the file may not be XML file. Maybe it's not RW map file.|地图文件解析错误，不符合xml格式。也许导入的不是铁锈地图。", 25)

    info_doids_dict = {}
    info_dict = {}
    ids_now_dict = {}
    
    dtobject = []

    info_tagged_objects_exist = []

    standard_out(isverbose, "The maximum ID of object in RW maps is resetting...|铁锈地图宾语最大ID重置中...")
    map_now.resetnextobjectid(isaboutnextobjectid = False)

    standard_out(isverbose, "ID mapping is being established...|宾语ID映射正在建立...")
    
    id_to_tobject_do = True
    debug_do_num = 0
    while(id_to_tobject_do):
        if debug_do_num == 2:
            print("程序出现bug，请联系作者。")
            exit(0)
        id_to_tobject_do = False
        id_to_tobject:dict[int, rw.case.TObject] = {}
        for tobject in map_now.iterator_object_s():
            tobid = tobject.returnDefaultProperty("id")
            if id_to_tobject.get(tobid) != None:
                ox = id_to_tobject.get(tobid).returnDefaultProperty("x")
                oy = id_to_tobject.get(tobid).returnDefaultProperty("y")
                oname = id_to_tobject.get(tobid).returnDefaultProperty("name")
                tobject_x = tobject.returnDefaultProperty("x")
                tobject_y = tobject.returnDefaultProperty("y")
                tobject_name = tobject.returnDefaultProperty("name")


                istriggerauto = False
                for tobject in map_now.iterator_object_s():
                    if tobject.returnOptionalProperty(AUTOKEY.IDs) != None:
                        istriggerauto = True
                        break

                if not istriggerauto:
                    question(True, "The IDs are coincident and the mapping cannot be performed. And the map has not executed triggerauto. Would you want to rearrange ID?" + \
                            "|宾语ID发生重合，ID映射无法进行。且尚未自动化。是否重排ID？", ["y", "n"], ["n"], {}, 
                            isyes, "y")
                    standard_out(isverbose, "IDs are arranging in the map...|铁锈地图宾语ID重排中...")
                    map_now.resetid()
                else:
                    standard_out(True, f"The IDs are coincident and the mapping cannot be performed. And the map has executed triggerauto. Maybe object ID adjustment is required." + 
                                f"|宾语ID发生重合，ID映射无法进行。且已经进行过宾语自动化。可能需要手动调整。")
                    try_to_deal_id_coincide(map_now)

                if input_path != output_path:
                    isrestore = question(True, "Is the map saved back to the input path after the objects ID is rearranged?" + \
                                            "|宾语ID重排后的地图是否保存回原文件？", ["y", "n"], [], 
                                            {"n": "The map doesn't save in input path. Continue.|原文件未保存，程序继续。"}, 
                                            isyes, "y")
                    if isrestore == "y":
                        standard_out(isverbose, "The map which objects ID is rearranged is restoring...|ID重排地图正在保存中...")
                        map_now.write_file(input_path)
                
                id_to_tobject_do = True
                break
            id_to_tobject[tobid] = tobject
        debug_do_num = debug_do_num + 1

    standard_out(isverbose, "The info object is rearranging...|info宾语重排中...")
    num_info = len(info_now_pre)
    info_now = OrderedDict()
    while_i = 0
    while(while_i < num_info + 1 and len(info_now) < num_info):
        for key, info in info_now_pre.items():
            isend = True
            if info.get(AUTOKEY.info_prefix) != None:
                for info_prefix_now in info[AUTOKEY.info_prefix].keys():
                    if info_now.get(info_prefix_now) == None:
                        isend = False
                        break
            if isend:
                info_now[key] = deepcopy(info)
        while_i = while_i + 1

    if while_i == num_info + 1:
        standard_error(f"External info import loop error.|info宾语引用循环。", 1, None, None, None, None)

    for key, info in info_now.items():
        infolen = len(info[AUTOKEY.info_args])
        while_i = 0
        info_args_temp = OrderedDict()
        while(while_i < infolen + 1 and len(info_args_temp) < infolen):
            for args_now, ntype in info[AUTOKEY.info_args].items():
                isend = True
                if info.get(AUTOKEY.var_dependent) != None and info[AUTOKEY.var_dependent].get(args_now) != None:
                    var_den_list = info[AUTOKEY.var_dependent][args_now].split(",")
                    for var_den in var_den_list:
                        if info_args_temp.get(var_den) == None:
                            isend = False
                            break
                if isend:
                    info_args_temp[args_now] = deepcopy(ntype)
            while_i = while_i + 1
        info[AUTOKEY.info_args] = info_args_temp
        if while_i == infolen + 1:
            standard_error(f"Info input dependence loop error.({key})|info宾语独立性发生循环。({key})", 5, None, None, None, None)

    time_ini_e = time.time()
    time_ini = time_ini_e - time_ini_i

    time_allinfo_i = time.time()

    standard_out_underline(isverbose, "Info objects precedure|info宾语处理")

    for key, info in info_now.items():
        for tobject in map_now.iterator_object_s(default_re = {rw.const.OBJECTDE.type: r"(?!.+)", 
                                                               rw.const.OBJECTDE.name: r".+"}):
            info_name = tobject.returnDefaultProperty(rw.const.OBJECTDE.name)

            if bool(re.match(key, info_name)):
                tobject_id = tobject.returnDefaultProperty("id")
                tobject_x = tobject.returnDefaultProperty("x")
                tobject_y = tobject.returnDefaultProperty("y")
                standard_out(isverbose, f"An object(ID:{tobject_id}, name:{info_name}) has been identified as an info object. Initialization..." + 
                             f"|一个宾语(ID:{tobject_id}, 名称:{info_name})已被确认为info宾语。初始化...")
                info_dict_now = {}
                info_dict_now[AUTOKEY.tobject] = tobject
                # info_prefix
                
                tobject_temp = deepcopy(tobject)
                if info.get(AUTOKEY.info_prefix) != None:
                    for value_name in info[AUTOKEY.info_prefix].values():
                        if tobject_temp.returnOptionalProperty(value_name) == None:
                            continue
                        info_dict_now[value_name] = mapvalue_to_value(tobject_temp.returnOptionalProperty(value_name), str)
                        tobject_temp.deleteOptionalProperty(value_name)
                    #debug_pdb("info_prefix end")
                    for info_pre_now, value_name in info[AUTOKEY.info_prefix].items():
                        if info_dict_now.get(value_name) != None:
                            tar_info = info_dict.get(info_dict_now[value_name])
                            if tar_info == None or info_pre_now != tar_info[AUTOKEY.info_key]:
                                standard_error(f"External info import error(target_info:{info_pre_now},info_key:{value_name},info_prefix:{info_dict_now[value_name]})." + 
                                               f"|info宾语导入循环(目标info:{info_pre_now},info类型:{value_name},info导入前缀:{info_dict_now[value_name]})。", 
                                               0, tobject_id, info_name, tobject_x, tobject_y)
                            info_temp = info_now[tar_info[AUTOKEY.info_key]]
                            if tar_info[AUTOKEY.isdelete_sym] and (info_temp.get(AUTOKEY.isinfo_sub) != None and info_temp[AUTOKEY.isinfo_sub] == True):
                                standard_error(f"External info import error(The target info has \",d\")(target_info:{info_pre_now},info_key:{value_name},info_prefix:{info_dict_now[value_name]})." + 
                                               f"|info宾语导入循环(目标info:{info_pre_now},info类型:{value_name},info导入前缀:{info_dict_now[value_name]})。", 
                                               10, tobject_id, info_name, tobject_x, tobject_y)
                            info_dict_now.update(tar_info)

                #debug_pdb("external info end")

                # add default_args
                info_dict_now[AUTOKEY.isdelete_sym] = bool(re.match(AUTOKEY.delete_symbol, info_name))
                info_dict_now[AUTOKEY.isdelete_all_sym] = bool(re.match(AUTOKEY.delete_all_symbol, info_name))
                default_brace = deepcopy(info.get(AUTOKEY.default_brace))
                if info.get(AUTOKEY.default_args) != None:
                    for key_now, value in info[AUTOKEY.default_args].items():
                        if info_dict_now.get(key_now) != None:
                            if default_brace.issuperset([key_now]):
                                default_brace.remove(key_now)
                            continue
                        if default_brace != None and default_brace.issuperset([key_now]):
                            info_dict_now[key_now] = value
                        else:
                            info_dict_now[key_now] = mapvalue_to_value(value, info[AUTOKEY.info_args][key_now])

                #debug_pdb("default_args end")

                # add info_args
                for key_now, ntype in info[AUTOKEY.info_args].items():
                    if tobject_temp.returnOptionalProperty(key_now) != None:
                        try:
                            info_dict_now[key_now] = mapvalue_to_value(tobject_temp.returnOptionalProperty(key_now), ntype)
                        except ValueError:
                            standard_error(f"An argument of info is wrong, maybe not a number.(key:{key_now}, value:\"{tobject_temp.returnOptionalProperty(key_now)}\", type:{ntype})" + \
                                           f"|info 数据读取错误，可能是本来填数字的地方不是数字。(参数:{key_now}, 参数内容:\"{tobject_temp.returnOptionalProperty(key_now)}\", 类型:{ntype})", 
                                           27, tobject_id, info_name, tobject_x, tobject_y)
                        tobject_temp.deleteOptionalProperty(key_now)
                        if default_brace != None and default_brace.issuperset([key_now]):
                            default_brace.remove(key_now)

                info[AUTOKEY.no_check] = (info.get(AUTOKEY.no_check) != None and info[AUTOKEY.no_check])
                if info[AUTOKEY.no_check]:
                    for key_now in tobject_temp._optional_properties.keys():
                        info_dict_now[key_now] = mapvalue_to_value_basic(tobject_temp.returnOptionalProperty(key_now))
                    tobject_temp._optional_properties = {}
                
                if info.get(AUTOKEY.initial_brace) != None:
                    for key_now, value in info[AUTOKEY.initial_brace].items():
                        info_dict_now[key_now] = brace_translation(value, info_dict_now)
                if default_brace != None:
                    for key_now in default_brace:
                        info_dict_now[key_now] = brace_translation(info_dict_now[key_now], info_dict_now, brace_exp_depth = 1)


                info[AUTOKEY.isinfo_sub] = (info.get(AUTOKEY.isinfo_sub) != None and info[AUTOKEY.isinfo_sub])



                info_dict_now[AUTOKEY.prefix] = info_dict_now[info[AUTOKEY.prefix]]
                info_doids_dict[info_dict_now[AUTOKEY.prefix]] = deepcopy(info)

                info_dict_now[AUTOKEY.info] = info_dict_now[AUTOKEY.prefix]

                info_dict_now[AUTOKEY.info_key] = key
                info_dict_now[AUTOKEY.info_name] = info_name

                if info.get(AUTOKEY.operation_pre) != None:
                    operation_index = {}
                    for index, operation_now in enumerate(info[AUTOKEY.operation_pre]):
                        if operation_now[AUTOKEY.operation_type] == AUTOKEY.tag:
                            operation_index[operation_now[AUTOKEY.tag]] = index
                    
                    object_dict = deepcopy(info_dict_now)
                    index = 0
                        
                    while(index < len(info[AUTOKEY.operation_pre])):
                        
                        operation_now = info[AUTOKEY.operation_pre][index]
                        
                        if operation_now[AUTOKEY.operation_type] == AUTOKEY.goto:
                            index = operation_index[operation_now[str_translation(AUTOKEY.goto_tag, object_dict)]]
                            continue

                        elif operation_now[AUTOKEY.operation_type] == AUTOKEY.typeif:
                            ifvar_exp = brace_translation(operation_now[AUTOKEY.ifvar], object_dict)
                            if isinstance(ifvar_exp, str) or (not bool(ifvar_exp)):
                                index = operation_index[operation_now[str_translation(AUTOKEY.ifend_tag, object_dict)]]

                        elif operation_now[AUTOKEY.operation_type] == AUTOKEY.errorif:
                            if isquick:
                                index = operation_index[operation_now[str_translation(AUTOKEY.ifend_tag, object_dict)]]
                

                        elif operation_now[AUTOKEY.operation_type] == AUTOKEY.typeset:
                            for key_n, value in operation_now.items():
                                if key_n != AUTOKEY.operation_type and key_n != AUTOKEY.totype:
                                    if operation_now.get(AUTOKEY.totype) == None:
                                        object_dict[str_translation(key_n, object_dict)] = value
                                    else:
                                        object_dict[str_translation(key_n, object_dict)] = str_to_type(type_to_str(value, get_type(value)), operation_now[AUTOKEY.totype])
                        elif operation_now[AUTOKEY.operation_type] == AUTOKEY.typeset_expression:
                            depth_now = MAXTRANSDEPTH if operation_now.get(AUTOKEY.depth) == None else operation_now[AUTOKEY.depth]
                            brace_exp_depth_now = MAXTRANSDEPTH if operation_now.get(AUTOKEY.brace_exp_depth) == None else operation_now[AUTOKEY.brace_exp_depth]
                            for key_n, value in operation_now.items():
                                if key_n != AUTOKEY.operation_type and key_n != AUTOKEY.depth and key_n != AUTOKEY.brace_exp_depth:
                                    object_dict[str_translation(key_n, object_dict)] = brace_translation(value, object_dict, depth = depth_now, brace_exp_depth = brace_exp_depth_now)
                        elif operation_now[AUTOKEY.operation_type] == AUTOKEY.changetype:
                            for key_n in operation_now[AUTOKEY.keyname_list]:
                                str_trans = str_translation(key_n, object_dict)
                                value = object_dict[str_trans]
                                object_dict[str_trans] = str_to_type(type_to_str(value, get_type(value)), operation_now[AUTOKEY.totype])
                        elif operation_now[AUTOKEY.operation_type] == AUTOKEY.typeset_exist:
                            for key_n, value in operation_now.items():
                                if key_n != AUTOKEY.operation_type:
                                    object_dict[str_translation(key_n, object_dict)] = object_dict.get(value) != None
                        elif operation_now[AUTOKEY.operation_type] == AUTOKEY.typeset_id:
                            for key_n, value in operation_now.items():
                                if key_n != AUTOKEY.operation_type and key_n != AUTOKEY.real_idexp:
                                    key_trans = str_translation(key_n, object_dict)
                                    num = brace_translation(value, object_dict)
                                    info_doids_dict[info_dict_now[AUTOKEY.prefix]][AUTOKEY.ids].append([key_trans, num])
                                    info_dict_now[key_trans] = mapvalue_to_value(str_translation(operation_now[AUTOKEY.real_idexp], object_dict), str)
                        elif operation_now[AUTOKEY.operation_type] == AUTOKEY.typeadd_args:
                            for key_n, value in operation_now.items():
                                if key_n != AUTOKEY.operation_type:
                                    value_brace = brace_translation(value, object_dict, brace_exp_depth = 1)
                                    value_brace = aeval_globals(value_brace)
                                    info_doids_dict[info_dict_now[AUTOKEY.prefix]][AUTOKEY.args].append((str_translation(key_n, object_dict), value_brace))
                        elif operation_now[AUTOKEY.operation_type] == AUTOKEY.typeadd_opargs:
                            for key_n, value in operation_now.items():
                                if key_n != AUTOKEY.operation_type:
                                    value_brace = brace_translation(value, object_dict, brace_exp_depth = 1)
                                    value_brace = (value_brace[0], aeval_globals(value_brace[1]))
                                    info_doids_dict[info_dict_now[AUTOKEY.prefix]][AUTOKEY.opargs][str_translation(key_n, object_dict)] = value_brace
                        elif operation_now[AUTOKEY.operation_type] == AUTOKEY.typedelete_optional:
                            for key_n, value in operation_now.items():
                                if key_n == AUTOKEY.namedelete_optional:
                                    value_brace = brace_translation(value, object_dict)
                                    for value_n in value_brace:
                                        if info_doids_dict[info_dict_now[AUTOKEY.prefix]][AUTOKEY.optional].issuperset([value_n]):
                                            info_doids_dict[info_dict_now[AUTOKEY.prefix]][AUTOKEY.optional].remove(value_n)
                        elif operation_now[AUTOKEY.operation_type] == AUTOKEY.typeadd_optional:
                            for key_n, value in operation_now.items():
                                if key_n == AUTOKEY.nameadd_optional:
                                    value_brace = brace_translation(value, object_dict)
                                    for value_n in value_brace:
                                        info_doids_dict[info_dict_now[AUTOKEY.prefix]][AUTOKEY.optional].add(value_n)
                        elif operation_now[AUTOKEY.operation_type] == AUTOKEY.error:
                            standard_error(str_translation(operation_now[AUTOKEY.error_info], object_dict), -1, tobject_id, info_name, tobject_x, tobject_y)
                        elif operation_now[AUTOKEY.operation_type] == AUTOKEY.pdb_pause:
                            debug_pdb(object_dict)
                        index = index + 1

                info_new = info_doids_dict[info_dict_now[AUTOKEY.prefix]]
                args_dict = deepcopy(info_dict_now)

                #args/opargs check
                if info_new.get(AUTOKEY.args) != None:
                    for key_n in info_new[AUTOKEY.args]:
                        key_now = key_n[0]
                        args_dict[key_n[0]] = key_n[1]
                        if info_new[AUTOKEY.info_args].get(key_now) == None and info_new[AUTOKEY.no_check] == False:
                            standard_error(f"An argument of the info object is invalid.(arg:{key_now})" +
                                           f"|info宾语的一个必需参数不合法。(参数:{key_now})", 
                                           12, tobject_id, info_name, tobject_x, tobject_y)

                if info_new.get(AUTOKEY.opargs) != None:
                    for value in info_new[AUTOKEY.opargs].values():
                        args_now = value[0].split(AUTOKEY.opargs_sys_seg)
                        if len(args_now) == 2:
                            args_dict[args_now[0]] = value[1]
                        args_now = args_now[0]
                        if info_new[AUTOKEY.info_args].get(args_now) == None and info_new[AUTOKEY.no_check] == False:
                            standard_error(f"An optional argument of the info object is invalid.(arg:{args_now})" + 
                                           f"|info宾语的一个可选参数不合法。(参数:{args_now})", 13, tobject_id, info_name, tobject_x, tobject_y)

                # var_dependent check
                
                for key_now, ntype in info_new[AUTOKEY.info_args].items():
                    if tobject.returnOptionalProperty(key_now) != None:
                        if info_new.get(AUTOKEY.var_dependent) != None and info_new[AUTOKEY.var_dependent].get(key_now) != None:
                            for args_dependent in info_new[AUTOKEY.var_dependent][key_now].split(","):
                                if (args_dict.get(args_dependent) == None or args_dict[args_dependent] == False):
                                    standard_error(f"Unuseful arguments in an info object.({key_now} exists but {args_dependent} is none or not \"true\".)" + 
                                                   f"|info宾语中出现无用参数({key_now}出现但是{args_dependent}没有或者不为\"true\")。", 
                                                   4, tobject_id, info_name, tobject_x, tobject_y)

                # required arguments check
                for key_now, ntype in info_new[AUTOKEY.info_args].items():
                    if info_new.get(AUTOKEY.optional) != None and info_new[AUTOKEY.optional].issuperset([key_now]):
                        continue
                    if info_new.get(AUTOKEY.var_dependent) != None and info_new[AUTOKEY.var_dependent].get(key_now) != None:
                        var_dep_list = info_new[AUTOKEY.var_dependent][key_now].split(",")
                        isend = True
                        for var_dep in var_dep_list:
                            if args_dict.get(var_dep) == None or args_dict[var_dep] != True:
                                isend = False
                                break
                        if not isend:
                            continue
                    if args_dict.get(key_now) == None and (not info_new[AUTOKEY.isinfo_sub]):
                        standard_error(f"A required argument is missing in an info object.({str(key_now)})" + 
                                       f"|info宾语中的一个必需参数缺失。({str(key_now)})", 
                                       6, tobject_id, info_name, tobject_x, tobject_y)
                
                if len(tobject_temp._optional_properties) != 0 and info_new[AUTOKEY.no_check] == False:
                        standard_error(f"Unknown arguments below in an info object." +
                                       f"|未知参数出现在了info宾语中。", 
                                       3, f"{tobject_temp._optional_properties}", tobject_id, info_name, tobject_x, tobject_y)


                standard_out(isverbose, "Info object information is being output..." + 
                             "|info宾语信息正在输出...")
                if isverbose:
                    temp_pri = OrderedDict()
                    if info_new.get(AUTOKEY.no_check) == None or info_new[AUTOKEY.no_check] == False:
                        for args_now in info_new[AUTOKEY.info_args].keys():
                            if info_dict_now.get(args_now) == None:
                                continue
                            value_now = info_dict_now[args_now]
                            if value_now == False:
                                continue
                            if info_new.get(AUTOKEY.var_dependent) != None:
                                var_dep_list = info_new[AUTOKEY.var_dependent].get(args_now)
                                if var_dep_list == None:
                                    temp_pri[args_now] = value_now 
                                    continue
                                var_dep_list = var_dep_list.split(",")
                                isend = True
                                for var_dep in var_dep_list:
                                    if info_dict_now.get(var_dep) == None or info_dict_now[var_dep] != True:
                                        isend = False
                                        break
                                if not isend:
                                    continue
                            temp_pri[args_now] = value_now 
                    else:
                        temp_pri = OrderedDict(info_dict_now)
                        temp_pri.pop("tobject")
                    standard_out(isverbose, temp_pri)

                for key_now in info_dict.keys():
                    if (key_now.startswith(info_dict_now[AUTOKEY.prefix]) and not info_dict_now[AUTOKEY.isprefixseg]) or \
                        (info_dict_now[AUTOKEY.prefix].startswith(key_now) and not info_dict[key_now][AUTOKEY.isprefixseg]):
                        standard_error(f"An info's prefix is the prefix of another.(name1:({info_dict[key_now][AUTOKEY.info_name]}), prefix1({key_now}); name2:({info_dict_now[AUTOKEY.info_name]})), prefix2:({info_dict_now[AUTOKEY.prefix]})" + 
                                       f"|一个info宾语的前缀是另一个info宾语的前缀。(名称1:({info_dict[key_now][AUTOKEY.info_name]}), 前缀1({key_now}); 名称2:({info_dict_now[AUTOKEY.info_name]})), 前缀2:({info_dict_now[AUTOKEY.prefix]})", 22, tobject_id, info_name, tobject_x, tobject_y)

                info_dict[info_dict_now[AUTOKEY.prefix]] = info_dict_now
                if isdelete_all or isdelete or info_dict_now[AUTOKEY.isdelete_all_sym] or (isdelete_d and info_dict_now[AUTOKEY.isdelete_sym]):
                    dtobject.append(tobject)
                else:
                    info_tagged_objects_exist.append(tobject)

    info_now = info_doids_dict

    standard_out(isverbose and (isdelete_all or isdelete), "The info object is being deleted...|info宾语正在全部删除...")
    standard_out(isverbose and (isdelete_d), "The info object is being deleted if eligible...|打删除标记的info宾语正在全部删除...")
    for tobject in dtobject:
        map_now.delete_object_s(tobject)
        tobject_id = tobject.returnDefaultProperty("id")
        standard_out(isverbose, f"An info object(ID:{tobject_id}, name:{tobject.returnDefaultProperty(rw.const.OBJECTDE.name)}) has been deleted..." + 
                     f"|一个info宾语(ID:{tobject_id}, 名称:{tobject.returnDefaultProperty(rw.const.OBJECTDE.name)})已经删除了")


    time_allinfo_e = time.time()
    time_allinfo = time_allinfo_e - time_allinfo_i
    time_tagged_i = time.time()

    standard_out_underline(isverbose, "Tagged objects procedure|标记宾语处理")

    standard_out(isverbose, "The ids of tagged objects are collecting...|标记宾语检测id正在收集...")
    for tobject in map_now.iterator_object_s(default_re = {rw.const.OBJECTDE.type: r"(?!.+)", 
                                                           rw.const.OBJECTDE.name: r".+"}):
        tobject_name = tobject.returnDefaultProperty(rw.const.OBJECTDE.name)
        ischange__newname__myinfo__info = is_tagged_tobject__newname__myinfo__info(tobject_name, info_dict, info_now)
        ischange = ischange__newname__myinfo__info[0]
        tobject_name_to_solve = ischange__newname__myinfo__info[1]
        myinfo = ischange__newname__myinfo__info[2]
        info = ischange__newname__myinfo__info[3]
        if ischange:
            if myinfo.get(AUTOKEY.ids) != None and myinfo.get(AUTOKEY.ids) != '':
                tobject_ids_do(tobject, myinfo, info, ids_now_dict, isreset, id_to_tobject)

    dtobject_id:set[str] = set()
    tobject_list = [tobject for tobject in map_now.iterator_object_s(default_re = {rw.const.OBJECTDE.type: r"(?!.+)", 
                                                           rw.const.OBJECTDE.name: r".+"}) if is_tagged_object_simple(tobject) and (tobject.returnOptionalProperty(AUTOKEY.IDdep) == None or tobject.returnOptionalProperty(AUTOKEY.IDdep) == '0')]
    index_tobject = 0

    time_dif_info = {}
    time_info = {}

    while index_tobject < len(tobject_list):
        tobject = tobject_list[index_tobject]
        insert_index = index_tobject + 1
        index_tobject = index_tobject + 1

        tobject_name = tobject.returnDefaultProperty(rw.const.OBJECTDE.name)
        tobject_id = tobject.returnDefaultProperty("id")
        tobject_x = tobject.returnDefaultProperty("x")
        tobject_y = tobject.returnDefaultProperty("y")
        ischange = False

        for key, info in info_dict.items():
            prefix_now = info[AUTOKEY.prefix]
            info_key = info[AUTOKEY.info]
            info_tobject:rw.case.TObject = info[AUTOKEY.tobject]
            myinfo = info_now[info_key]

            if info.get(AUTOKEY.isprefixseg) != None and info.get(AUTOKEY.isprefixseg) == True:
                prefix_to_match = tobject_name.split(myinfo[AUTOKEY.seg])[0]
                tobject_name_to_solve = tobject_name[len(prefix_to_match) + 1:]
            else:
                prefix_to_match = tobject_name[0:len(prefix_now)]
                tobject_name_to_solve = tobject_name[len(prefix_to_match):]

            if prefix_now == prefix_to_match \
                and (not re.match(AUTOKEY.info_re, tobject_name)):
                object_dict = deepcopy(info)
                object_dict[AUTOKEY.tobject_id] = tobject_id
                object_dict[AUTOKEY.tobject_name] = tobject_name

                object_dict.update(get_args(myinfo, tobject_name_to_solve, tobject, info_tobject, object_dict))
                
                if info.get(AUTOKEY.info_prefix) != None:
                    for info_pre in info[AUTOKEY.info_prefix]:
                        info_temp = info_dict[info_pre]
                        object_dict.update(info_temp)
                ischange = True
                break
        
        if not ischange and (tobject.returnOptionalProperty(AUTOKEY.IDdep) != None and int(tobject.returnOptionalProperty(AUTOKEY.IDdep)) > 0):
            tobject_info = id_to_tobject[tobject.returnOptionalProperty(AUTOKEY.IDfa)]
            info_id = tobject_info.returnDefaultProperty("id")
            info_name = tobject_info.returnDefaultProperty("name")
            info_x = tobject_info.returnDefaultProperty("x")
            info_y = tobject_info.returnDefaultProperty("y")
            standard_error(f"A tree tagged object produced by tree tagged object cannot match any info. Please check if the prefix is corret in the name(properties) of tree_info.(father ID:{info_id}, father name:{info_name}, father coordinate({info_x}, {info_y}))" + 
                           f"|生成的标记宾语无法匹配，请查找对应tree_info name中前缀是否正确。(上级 ID:{info_id}, 上级 名称:{info_name}, 上级 坐标({info_x}, {info_y}))", 
                           26, tobject_id, tobject_name, tobject_x, tobject_y)
        if ischange:
            time_tag_i = time.time()
            isdelete_sym = bool(re.match(AUTOKEY.delete_symbol, tobject_name)) or info[AUTOKEY.isdelete_sym]
            isdelete_all_sym = bool(re.match(AUTOKEY.delete_all_symbol, tobject_name)) or info[AUTOKEY.isdelete_all_sym]

            standard_out(isverbose and (not(isdelete_sym or isdelete_all or isdelete_all_sym)), 
                         f"An object(ID:{tobject_id}, name:{tobject_name}) has been identified as a tagged object. Object generation..." + 
                         f"|一个宾语(ID:{tobject_id}, 名称:{tobject_name})已经被确认为标记宾语。宾语生成中...")
            standard_out(isverbose and (isdelete_all or isdelete_all_sym), 
                         f"An object(ID:{tobject_id}, name:{tobject_name}) has been identified as a tagged object. All objects generated by this tagged object and itself will be deleted..." + 
                         f"|一个宾语(ID:{tobject_id}, 名称:{tobject_name})已经被确认为标记宾语。所有该标记宾语产生的宾语和自身都将被删除...")
            standard_out(isverbose and (isdelete_sym and(not (isdelete_all or isdelete_all_sym))), 
                         f"An object(ID:{tobject_id}, name:{tobject_name}) has been identified as a tagged object with deleted tag. The objects will not be generated, existing ones will also be deleted..." +
                         f"|一个宾语(ID:{tobject_id}, 名称:{tobject_name})已经被确认为有删除标记的标记宾语. 将不会新产生宾语，之前产生的宾语也将全部删除...")

            if myinfo.get(AUTOKEY.isinfo_sub) != None and myinfo.get(AUTOKEY.isinfo_sub) == True:
                standard_error(f"Incorrect use of the subordinate info object.|" + 
                               f"附属宾语的不正确使用。", 2, tobject_id, tobject_name, tobject_x, tobject_y)

            if tobject.returnOptionalProperty(AUTOKEY.IDdep) == None:
                tobject.assignOptionalProperty(AUTOKEY.IDdep, "0")
            tobject_IDdep = int(tobject.returnOptionalProperty(AUTOKEY.IDdep))

            if isdelete_all or isdelete or isdelete_all_sym or (isdelete_sym and isdelete_d):
                dtobject_id.add(tobject_id)
            else:
                if tobject.returnOptionalProperty(AUTOKEY.IDfa) == None:
                    info_tagged_objects_exist.append(tobject)

            if myinfo.get(AUTOKEY.ids) != None:
                for thing in myinfo[AUTOKEY.ids]:
                    
                    idprefix = brace_translation(thing[0], object_dict, brace_exp_depth = 1)
                    if ids_now_dict.get(idprefix) == None:
                        ids_now_dict[idprefix] = 1
                    idnow_list = tobject.returnOptionalProperty(idprefix)
                    if idnow_list == None:
                        idnow_list = []
                    else:
                        idnow_list = idnow_list.split(",")
                    for i, idnow in enumerate(idnow_list):
                        object_dict[thing[0] + str(i)] = idnow
                    for i in range(len(idnow_list), thing[1]):
                        id_now = idprefix + str(ids_now_dict[idprefix])
                        idnow_list.append(id_now)
                        object_dict[thing[0] + str(i)] = id_now
                        if (isdelete_sym or isdelete_all_sym or isdelete_all):
                            continue
                        ids_now_dict[idprefix] = ids_now_dict[idprefix] + 1
                    tobject.assignOptionalProperty(idprefix, ",".join(idnow_list))

            
            ori_pos = rw.frame.Coordinate(
                tobject.returnDefaultProperty(rw.const.OBJECTDE.x), 
                tobject.returnDefaultProperty(rw.const.OBJECTDE.y)
            )
            ori_size = rw.frame.Coordinate(
                tobject.returnDefaultProperty(rw.const.OBJECTDE.width), 
                tobject.returnDefaultProperty(rw.const.OBJECTDE.height)
            )
            #import pdb;pdb.set_trace()
            if isdelete_all or isdelete_all_sym or isdelete_sym:
                if object_dict.get(AUTOKEY.IDs) != None:
                    for ids in object_dict[AUTOKEY.IDs]:
                        if id_to_tobject.get(ids) == None:
                            standard_warning(f"An object that needs to be deleted could not be found.(parent ID:{tobject_id})" + 
                                             f"|一个需要被删除的宾语无法找到。(父亲 ID:{tobject_id})", 
                                             4, 21, tobject_id, tobject_name, tobject_x, tobject_y)
                        elif not is_tagged_object_simple(id_to_tobject[ids]):
                            dtobject_id.add(ids)
                continue
            
            operation_index = {}
            for index, operation_now in enumerate(myinfo[AUTOKEY.operation]):
                if operation_now[AUTOKEY.operation_type] == AUTOKEY.tag:
                    if operation_index.get(operation_now[AUTOKEY.tag]) != None:
                        standard_error(f"operation tags are duplicated.({operation_now[AUTOKEY.tag]})" + 
                                       f"|命令标记发生重合。({operation_now[AUTOKEY.tag]})", 
                                       15, tobject_id, tobject_name, tobject_x, tobject_y)
                    operation_index[operation_now[AUTOKEY.tag]] = index

            tottobid = 0
            index = 0

            while(index < len(myinfo[AUTOKEY.operation])):

                operation_now = myinfo[AUTOKEY.operation][index]

                if operation_now[AUTOKEY.operation_type] == AUTOKEY.object:
                    

                    object_now = get_tobject(operation_now, object_dict, ori_pos, ori_size)

                    if object_now != None:
                        
                        isnewtaggedobject = is_tagged_object_simple(object_now)
                        if isnewtaggedobject:
                            if isdelete_sym:
                                object_now.assignDefaultProperty(rw.const.OBJECTDE.name, object_now.returnDefaultProperty(rw.const.OBJECTDE.name) + AUTOKEY.delete_op)
                            if isdelete_all_sym:
                                object_now.assignDefaultProperty(rw.const.OBJECTDE.name, object_now.returnDefaultProperty(rw.const.OBJECTDE.name) + AUTOKEY.delete_all_op)
                            object_now.assignOptionalProperty(AUTOKEY.IDfa, tobject_id)
                            object_now.assignOptionalProperty(AUTOKEY.IDdep, str(tobject_IDdep + 1))
                            tobject_list.insert(insert_index, object_now)
                            insert_index = insert_index + 1

                        if object_dict.get(AUTOKEY.IDs) != None and tottobid < len(object_dict[AUTOKEY.IDs]):
                            object_now.assignDefaultProperty("id", object_dict[AUTOKEY.IDs][tottobid])
                            if id_to_tobject.get(object_dict[AUTOKEY.IDs][tottobid]) == None:
                                standard_warning(f"A tagged object can't find the object that was once created.(child ID:{object_dict[AUTOKEY.IDs][tottobid]})" + 
                                                 f"|一个标记宾语不能找到它曾经产生的宾语。(儿子 ID:{object_dict[AUTOKEY.IDs][tottobid]})", 1, 18, tobject_id, tobject_name, tobject_x, tobject_y)
                                map_now.addObject_type(object_now, isresetid = False)
                            else:
                                idnow_object:rw.case.TObject = deepcopy(id_to_tobject[object_dict[AUTOKEY.IDs][tottobid]])
                                if isnewtaggedobject:
                                    if is_tagged_object_simple(idnow_object):
                                        object_now._optional_properties = deepcopy(idnow_object._optional_properties)
                                else:
                                    if is_tagged_object_simple(idnow_object):
                                        idnow_object.assignDefaultProperty(rw.const.OBJECTDE.name, idnow_object.returnDefaultProperty(rw.const.OBJECTDE.name) + AUTOKEY.delete_all_op)
                                        tobject_list.append(idnow_object)
                                        map_now.addObject_type(idnow_object, isresetid = True)
                            id_to_tobject[object_dict[AUTOKEY.IDs][tottobid]] = deepcopy(object_now)
                        else:
                            map_now.addObject_type(object_now)
                            if not isdelete:
                                IDs_update(tobject, object_now)
                        tottobid = tottobid + 1
                    
                elif operation_now[AUTOKEY.operation_type] == AUTOKEY.goto:
                    index = operation_index[operation_now[str_translation(AUTOKEY.goto_tag, object_dict)]]
                    continue

                elif operation_now[AUTOKEY.operation_type] == AUTOKEY.typeif:
                    ifvar_exp = brace_translation(operation_now[AUTOKEY.ifvar], object_dict)
                    if isinstance(ifvar_exp, str) or (not bool(ifvar_exp)):
                        index = operation_index[operation_now[str_translation(AUTOKEY.ifend_tag, object_dict)]]
                elif operation_now[AUTOKEY.operation_type] == AUTOKEY.errorif:
                    if isquick:
                        index = operation_index[operation_now[str_translation(AUTOKEY.ifend_tag, object_dict)]]
                elif operation_now[AUTOKEY.operation_type] == AUTOKEY.typeset:
                    for key, value in operation_now.items():
                        if key != AUTOKEY.operation_type and key != AUTOKEY.totype:
                            if operation_now.get(AUTOKEY.totype) == None:
                                object_dict[str_translation(key, object_dict)] = value
                            else:
                                object_dict[str_translation(key, object_dict)] = str_to_type(type_to_str(value, get_type(value)), operation_now[AUTOKEY.totype])
                elif operation_now[AUTOKEY.operation_type] == AUTOKEY.typeset_expression:
                            depth_now = MAXTRANSDEPTH if operation_now.get(AUTOKEY.depth) == None else operation_now[AUTOKEY.depth]
                            brace_exp_depth_now = MAXTRANSDEPTH if operation_now.get(AUTOKEY.brace_exp_depth) == None else operation_now[AUTOKEY.brace_exp_depth]
                            for key_n, value in operation_now.items():
                                if key_n != AUTOKEY.operation_type and key_n != AUTOKEY.depth and key_n != AUTOKEY.brace_exp_depth:
                                    object_dict[str_translation(key_n, object_dict)] = brace_translation(value, object_dict, depth = depth_now, brace_exp_depth = brace_exp_depth_now)
                elif operation_now[AUTOKEY.operation_type] == AUTOKEY.changetype:
                    for key in operation_now[AUTOKEY.keyname_list]:
                        str_trans = str_translation(key, object_dict)
                        value = object_dict[str_trans]
                        object_dict[str_trans] = str_to_type(type_to_str(value, get_type(value)), operation_now[AUTOKEY.totype])
                elif operation_now[AUTOKEY.operation_type] == AUTOKEY.typeset_exist:
                    for key, value in operation_now.items():
                        if key != AUTOKEY.operation_type:
                            object_dict[str_translation(key, object_dict)] = object_dict.get(value) != None
                elif operation_now[AUTOKEY.operation_type] == AUTOKEY.error:
                    standard_error(str_translation(operation_now[AUTOKEY.error_info], object_dict), -1, tobject_id, tobject_name, tobject_x, tobject_y)
                elif operation_now[AUTOKEY.operation_type] == AUTOKEY.pdb_pause:
                    debug_pdb(object_dict)
                index = index + 1

            id_delete = IDs_balance(tobject, tottobid)
            for idnow in id_delete:
                if id_to_tobject.get(idnow) == None:
                    standard_warning(f"An object that needs to be deleted could not be found.(parent ID:{tobject_id})" + 
                                     f"|一个需要被删除的宾语不能找到。(父亲 ID:{tobject_id})", 
                                     4, 21, tobject_id, tobject_name, tobject_x, tobject_y)
                else:
                    if is_tagged_object_simple(id_to_tobject[idnow]):
                        id_to_tobject[idnow].assignDefaultProperty(rw.const.OBJECTDE.name, id_to_tobject[idnow].returnDefaultProperty(rw.const.OBJECTDE.name) + AUTOKEY.delete_all_op)
                        tobject_list.append(id_to_tobject[idnow])
                    else:
                        if not (isdelete_all or isdelete_all_sym or isdelete_sym):
                            dtobject_id.add(idnow)
            
            if object_dict.get(AUTOKEY.cite_name) != None and (not (isdelete_all or isdelete_all_sym or isdelete_sym)):
                cite_dict = OrderedDict([[info_nowp, str] for info_nowp in info[AUTOKEY.brace]]) if info.get(AUTOKEY.brace) != None else OrderedDict()
                cite_dict.update(OrderedDict([[info_nowp, str] for info_nowp in myinfo[AUTOKEY.is_cite_white_list]]) if myinfo.get(AUTOKEY.is_cite_white_list) != None else OrderedDict())
                cite_dict.update(OrderedDict(myinfo[AUTOKEY.args]) if myinfo.get(AUTOKEY.args) != None else OrderedDict())
                cite_dict.update(OrderedDict([[info_nowp[0].split("|")[0], info_nowp[1]] for info_nowp in myinfo[AUTOKEY.opargs].values()]) if myinfo.get(AUTOKEY.opargs) != None else OrderedDict())
                cite_dict.update(myinfo[AUTOKEY.info_args] if myinfo.get(AUTOKEY.info_args) != None else OrderedDict())
                cite_dict.update(OrderedDict([[info_one[0] + str(ti), str] for info_one in myinfo[AUTOKEY.ids] for ti in range(info_one[1])] + [[info_one[0], str] for info_one in myinfo[AUTOKEY.ids]]) if myinfo.get(AUTOKEY.ids) != None else OrderedDict())
                
                for key, value in object_dict.items():
                    
                    if (not (myinfo.get(AUTOKEY.isnot_cite_check) != None and myinfo[AUTOKEY.isnot_cite_check])) and cite_dict.get(key) == None:
                        continue
                    
                    if cite_object_dict.get(object_dict[AUTOKEY.cite_name] + "." + key) != None:
                        origin_id = cite_object_dict.get(object_dict[AUTOKEY.cite_name] + "." + AUTOKEY.tobject_id)
                        origin_name = cite_object_dict.get(object_dict[AUTOKEY.cite_name] + "." + AUTOKEY.tobject_name)
                        standard_error(f"Reference tags(cite_name) are duplicated。(original ID:({origin_id}), original name:({origin_name}), Cite:{object_dict[AUTOKEY.cite_name]})" + \
                                       f"|标记宾语引用(cite_name)发生重合。(重合 ID:({origin_id}), 重合名称:({origin_name}), 引用名称(cite_name):{object_dict[AUTOKEY.cite_name]})", 
                                       14, tobject_id, tobject_name, tobject_x, tobject_y)
                    cite_object_dict[object_dict[AUTOKEY.cite_name] + "." + key] = value
            
            time_tag_e = time.time()
            time_tag = time_tag_e - time_tag_i
            time_dif_info[prefix_now] = time_tag + (time_dif_info[prefix_now] if time_dif_info.get(prefix_now) != None else 0)
            time_info[info[AUTOKEY.info_key]] = time_tag + (time_info[info[AUTOKEY.info_key]] if time_info.get(info[AUTOKEY.info_key]) != None else 0)

    standard_out(isverbose and (isdelete_all or isdelete), "Some objects are being deleted...|需要被删除的宾语正在回收...")
    standard_out(isverbose and (isdelete_d), "Some objects are being deleted if eligible...|需要被删除的宾语正在回收，如有必要...")
    for tobject in [tobject for tobject in map_now.iterator_object_s()]:
        if dtobject_id.issuperset([tobject.returnDefaultProperty("id")]):
            map_now.delete_object_s(tobject)

    debug_pdb()

    if iscitetrans:
        standard_out(isverbose, "Other objects are being translated by cite.|其他普通宾语正在被引用翻译...")
        for tobject in map_now.iterator_object_s(default_re = {rw.const.OBJECTDE.type: r"(.+)"}):
            for key, value in tobject._default_properties.items():
                value_now = mapvalue_to_value_basic(value)
                if not isinstance(value_now, bool):
                    tobject.assignDefaultProperty(key, brace_one_translation_cycle(value_now, cite_object_dict, AUTOKEY.not_useful_char_ad_point_for_cite))
            for key, value in tobject._optional_properties.items():
                value_now = mapvalue_to_value_basic(value)
                if not isinstance(value_now, bool):
                    tobject.assignOptionalProperty(key, brace_one_translation_cycle(value_now, cite_object_dict, AUTOKEY.not_useful_char_ad_point_for_cite))

    time_tagged_e = time.time()
    time_tagged = time_tagged_e - time_tagged_i
    time_rea_i = time.time()

    standard_out_underline(isverbose, "Rearrangement and output|宾语重排和地图输出")
    
    standard_out(isverbose, "Info and tagged objects are rearranging...|info宾语和标记宾语正在重排...")
    
    tagged_object_list:list[rw.case.TObject] = []
    maxIDdep = -1
    for tobject in map_now.iterator_object_s():
        if is_tagged_object_simple(tobject):
            if tobject.returnOptionalProperty(AUTOKEY.IDdep) != None:
                tagged_object_list.append(tobject)
                maxIDdep = max(maxIDdep, int(tobject.returnOptionalProperty(AUTOKEY.IDdep)))

    IDdep_now = maxIDdep
    for IDdep_now in range(maxIDdep, 0, -1):
        for tobject in tagged_object_list:
            if int(tobject.returnOptionalProperty(AUTOKEY.IDdep)) == IDdep_now:
                map_now.delete_object_s(tobject)
        for tobject in tagged_object_list:
            if int(tobject.returnOptionalProperty(AUTOKEY.IDdep)) == IDdep_now:
                map_now.addObject_type(tobject, isresetid = False)

    for info_tag in info_tagged_objects_exist:
        map_now.delete_object_s(info_tag)
    for info_tag in info_tagged_objects_exist:
        map_now.addObject_type(info_tag, isresetid = False)

    if isresetid:
        standard_out(isverbose and isresetid, "The IDs are rearranging...|ID正在重排...")
        id_mapping = {}
        id_now = 1
        for tobject in map_now.iterator_object_s():
            tobid = tobject.returnDefaultProperty("id")
            tobject_x = tobject.returnDefaultProperty("x")
            tobject_y = tobject.returnDefaultProperty("y")
            if id_mapping.get(tobid) != None:
                standard_error(f"The IDs are coincident and the mapping cannot be performed." + 
                               f"|宾语ID发生重合，ID映射无法进行。", 
                               11, tobid, tobject_name, tobject_x, tobject_y)

            id_mapping[tobid] = str(id_now)
            id_now = id_now + 1

        id_now = 1
        for tobject in map_now.iterator_object_s():
            tobid = tobject.returnDefaultProperty("id")
            if is_tagged_object_simple(tobject):
                ids_now = tobject.returnOptionalProperty(AUTOKEY.IDs)
                if ids_now != None and ids_now != "":
                    ids_now_l = ids_now.split(AUTOKEY.IDs_seg)
                    ids_now_l = [id_mapping[ids_nown] for ids_nown in ids_now_l]
                    ids_now = f"{AUTOKEY.IDs_seg}".join(ids_now_l)
                    tobject.assignOptionalProperty(AUTOKEY.IDs, ids_now)

                idfa_now = tobject.returnOptionalProperty(AUTOKEY.IDfa)

                if idfa_now != None:
                    tobject.assignOptionalProperty(AUTOKEY.IDfa, id_mapping[idfa_now])

            tobject.assignDefaultProperty("id", str(id_now))
            id_now = id_now + 1

    map_now.resetnextobjectid(isaboutnextobjectid = False)

    time_rea_e = time.time()
    time_rea = time_rea_e - time_rea_i



    standard_out(isverbose, "New RW map is being establishing...|新的铁锈地图正在建立...")
    map_now.write_file(output_path)

    time_all_e = time.time()
    time_all = time_all_e - time_all_i

    standard_out_underline(isverbose, "Time statistics|时间统计")

    standard_out(isverbose, f"Total time:{time_all:.1f}s|运行总时间:{time_all:.1f}s")
    standard_out(isverbose, f"Initialization time:{time_ini:.1f}s|初始化处理时间:{time_ini:.1f}s")
    standard_out(isverbose, f"Info objects process time:{time_allinfo:.1f}s|info宾语处理时间:{time_allinfo:.1f}s")
    standard_out(isverbose, f"Tagged objects process time:{time_tagged:.1f}s|标记宾语处理时间:{time_tagged:.1f}s")
    standard_out(isverbose, f"Objects rearrangement time:{time_rea:.1f}s|宾语重组时间:{time_rea:.1f}s")

    standard_out(isverbose, f"Tagged objects time with different prefix:|不同前缀标记宾语的运行时间:")

    langstr_time_list = [f"{key}:{value:.1f}s, |{key}:{value:.1f}s, " for key, value in time_info.items()]
    langstr_time = langstrlist_add(langstr_time_list)
    langstr_time = "|".join(["(" + langtime[:-2] + ")" for langtime in langstr_time.split("|")])
    standard_out(isverbose, langstr_time)

    standard_out(isverbose, f"Tagged objects time with different prefix:|不同前缀标记宾语的运行时间:")

    langstr_time_list = [f"{key}:{value:.1f}s, |{key}:{value:.1f}s, " for key, value in time_dif_info.items()]
    langstr_time = langstrlist_add(langstr_time_list)
    langstr_time = "|".join(["(" + langtime[:-2] + ")" for langtime in langstr_time.split("|")])
    standard_out(isverbose, langstr_time)

    dev_null.close()

if __name__ == "__main__":
    auto_func()        
