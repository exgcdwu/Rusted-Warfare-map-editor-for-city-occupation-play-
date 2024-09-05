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

cite_object_dict = {}

def standard_out(ifdo:bool, info_str)->None:
    if ifdo:
        if isinstance(info_str, str):
            print(info_str)
        else:
            pprint(info_str)

def standard_error(info_err, error_id:int, sub_info_error:str = None)->None:
    print(info_err + f"(ERROR:{error_id})", file=sys.stderr)
    if sub_info_error != None:
        pprint(sub_info_error)
    if isdebug:
        import pdb;pdb.set_trace()
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


def get_args(info:dict, name:str, tobject:rw.case.TObject, id_to_tobject:dict, rwmap_now:rw.RWmap)->dict:
    args_dict = {}
    split_now = name.split(info[AUTOKEY.opargs_seg])
    opargs = split_now[1:]

    if split_now[0] == "":
        args_n = []
    else:
        args_n = split_now[0].split(info[AUTOKEY.seg])
    
    if len(args_n) < len(info[AUTOKEY.args]):
        info_args_temp = info[AUTOKEY.args][len(args_n):]
        standard_error(f"Required arguments are missing below in a tagged object.(name:{name},need:{len(info[AUTOKEY.args])},reality({len(args_n)}))", 8, info_args_temp)
    elif len(args_n) > len(info[AUTOKEY.args]):
        info_args_temp = args_n[len(info[AUTOKEY.args]):]
        standard_error(f"Too many required arguments below in a tagged object.(name:{name},need:{len(info[AUTOKEY.args])},reality({len(args_n)}))", 9, info_args_temp)

    for index, thing in enumerate(info[AUTOKEY.args]):
        args_dict[thing[0]] = thing[1](args_n[index])
    
    prefix_len = info[AUTOKEY.opargs_prefix_len]

    for info_thing in info[AUTOKEY.opargs].values():
        if len(info_thing[0].split(AUTOKEY.opargs_sys_seg)) == 2:
            args_dict[info_thing[0].split(AUTOKEY.opargs_sys_seg)[0]] = \
            mapvalue_to_value(info_thing[0].split(AUTOKEY.opargs_sys_seg)[1], info_thing[1])

    for oparg in opargs:
        prefix_now = oparg[0:prefix_len]
        var_now = oparg[prefix_len:]
        if info[AUTOKEY.opargs].get(prefix_now) != None:
            info_thing = info[AUTOKEY.opargs][prefix_now]
            if info_thing[1] != bool:
                args_dict[info_thing[0].split(AUTOKEY.opargs_sys_seg)[0]] = info_thing[1](var_now)
            else:
                args_dict[info_thing[0].split(AUTOKEY.opargs_sys_seg)[0]] = True
        else:
            if prefix_now != "d" and prefix_now != 'D':
                standard_error(f"Unknown optional arguments in a tagged object.(name:{name}|,{prefix_now})", 7)

    tobject_ids = tobject.returnOptionalProperty(AUTOKEY.IDs)
    tobject_ids = tobject_ids.split(AUTOKEY.IDs_seg) if tobject_ids != None else []
    if isresetid:
        tobject.deleteOptionalProperty(AUTOKEY.IDs)
        args_dict[AUTOKEY.IDs] = []
        for tobjectid in tobject_ids:
            if tobjectid == '415':
                debug_pdb()
            rwmap_now.delete_object_s(id_to_tobject[tobjectid])
    else:
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

def brace_translation(expression_b:str, dict_name:dict, prev:bool = True, ones:bool = False, depth = MAXTRANSDEPTH):
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

    if trans_dep_now == MAXTRANSDEPTH:
        standard_error(f"References occur in a loop(more than 1024).({expression_b})", 16)

    if (prev or expression_b_origin != expression_b) and (not ones):
        expression_b = expression_translation(expression_b, dict_name, False)
    try:
        expression_b_temp = aeval(expression_b)
    except Exception as e:
        return expression_b
    else:
        if expression_b_temp == None:
            return expression_b
        return expression_b_temp

def expression_translation(expression_s:str, dict_name:dict, prev:bool = True, depth = MAXTRANSDEPTH):
    expression_s_now = str_translation(expression_s, dict_name, depth = depth)
    if prev or expression_s != expression_s_now:
        return brace_translation(expression_s_now, dict_name, False, depth = depth)
    else:
        return expression_s_now
        
    


def str_translation(value:Union[str, bool], dict_name:dict, depth = MAXTRANSDEPTH)->str:
    if isinstance(value, bool):
        return value_to_mapvalue(value, bool)
    if isinstance(value, dict):
        return deepcopy(value)
    left_index = -1
    left_brace = 0
    index_list = []
    for index in range(0, len(value)):
        if value[index] == "{":
            if left_index == -1:
                left_index = index
            left_brace = left_brace + 1
        elif value[index] == "}":
            left_brace = left_brace - 1
            if left_brace == 0:
                right_index = index
                if left_index == -1:
                    raise ValueError("The string have '{' but don't have'}'.")
                index_list.append((left_index, right_index))
                left_index = -1
    if index_list == []:
        return value
    value_ans = value[0:index_list[0][0]]
    index_list.append((len(value), len(value)))
    for index in range(len(index_list) - 1):
        value_ans = value_ans + type_to_str(brace_translation(value[index_list[index][0] + 1:index_list[index][1]], dict_name, depth = depth), str) + value[index_list[index][1] + 1:index_list[index + 1][0]]
    return value_ans

def tobject_args_translation(key:str, value:str, dict_name:dict)->str:
    if isinstance(value, tuple):
        if value[2] == AUTOKEY.brace:
            if brace_translation(value[1], dict_name) == True:
                return {key:str_translation(value[0], dict_name)}
        elif value[2] == AUTOKEY.exist:
            value_list = value[1].split(",")
            isend = True
            for value_n in value_list:
                if dict_name.get(value_n) == None:
                    isend = False
                    break
            if isend:
                return {key:str_translation(value[0], dict_name)}
        
    else:
        return {key:str_translation(value, dict_name)}
    return {}

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
            value_now = ntype(True) if value["value"] == "true" else ntype(False) 
            if isinstance(value_now, str):
                value_now = value_now.lower()
            return value_now
    else:
        if ntype == bool:
            value_now = str(value)
            value_now = True if value_now == "true" else False
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
        return ntype(value)

def value_to_mapvalue(value, ntype):
    if ntype == bool:
        return {"value": str(bool(value)).lower(), "type": "bool"}
    if isinstance(ntype, tuple):
        if ntype[0] == list:
            if ntype[1] == str:
                value_now = value.join(",")
            elif ntype[1] == int:
                value = [str(value_i) for value_i in value]
                value_now = value.join(" ")
            elif ntype[1] == list:
                if ntype[2] == str:
                    value_now = ";".join([",".join(value_i) for value_i in value])
                elif ntype[2] == int:
                    value_now = [[str(value_ij) for value_ij in value_i] for value_i in value]
                    value_now = ",".join([" ".join(value_i) for value_i in value_now])
            return value_now
        return ntype(value)
    
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
    if idsh == None:
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


def tobject_ids_do(tobject:rw.case.TObject, myinfo, info, ids_now_dict, isreset):
    for thing_prefix_num in myinfo[AUTOKEY.ids]:
        tobject_prefix = tobject.returnOptionalProperty(thing_prefix_num[0])
        if tobject_prefix != None:
            tobject_prefix = tobject_prefix.split(",")
        else:
            tobject_prefix = []
        if isreset:
            tobject_prefix = []
            tobject.deleteOptionalPropertySup([AUTOKEY.IDs])
        prefix_now = brace_translation(thing_prefix_num[0], info)
        if ids_now_dict.get(prefix_now) == None:
            ids_now_dict[prefix_now] = 1
        
        for index in range(len(tobject_prefix)):
            tobject_prefix[index] = int(tobject_prefix[index][len(thing_prefix_num[0]):])
            ids_now_dict[prefix_now] = max(ids_now_dict[prefix_now], 
                                                    tobject_prefix[index])

def is_tagged_object_simple(tobject:rw.case.TObject):
    object_type = tobject.returnDefaultProperty(rw.const.OBJECTDE.type)
    isnewtaggedobject = (object_type == None or re.match(r"(?!.+)", object_type))
    return isnewtaggedobject
def auto_func():
    parser = argparse.ArgumentParser(
        description='Objects of Triggers are automatically processed by information\'s mode.')
    parser.add_argument('map_path', action = "store", metavar = 'file', type=str, nargs = 1, 
                        help='The input path of RW map file.')
    parser.add_argument("--infopath", 
                        action = "store", metavar = "file", type = str, nargs = 1, 
                        required = False, default = current_file_path[:-8] + "_data",  
                        help = "The file's path which has information's mode variable|current_file_path"
                        )
    parser.add_argument("--infovar", 
                        action = "store", metavar = "name", type = str, nargs = 1, 
                        required = False, default = "auto_func_arg", 
                        help = "The variable name of information\'s mode.|auto_func_arg"
                        )
    
    parser.add_argument("-o", "--output", 
                        action = "store", metavar = "file", type = str, nargs = 1, 
                        required = False, default = "|", 
                        help = "The output path of RW map file.|input path"
                        )

    parser.add_argument("-d", "--delete", 
                        action = 'store_true', help = 'Delete the info and tagged objects with ,d.')

    parser.add_argument("-D", "--DeleteAllSym", 
                        action = 'store_true', help = 'Delete all info and tagged objects.')

    parser.add_argument("--DeleteAll", 
                        action = 'store_true', help = 'Delete all info, tagged objects and relative objects.')

    parser.add_argument("-r", "--reset", 
                        action = 'store_true', help = 'Reset the ids of objects.(not recommend)')

    parser.add_argument("-v", "--verbose", 
                        action = 'store_true', help = 'Detailed output of the prompt message.')

    parser.add_argument("--debug", 
                        action = 'store_true', help = 'Mode of debuging.')
    
    parser.add_argument("--resetid", 
                        action = 'store_true', help = 'Reset the IDs of objects.')
    
    parser.add_argument("-c", "--citetrans", 
                        action = 'store_true', help = 'Cite translation.(other objects)')

    dev_null = open(os.devnull, "w")
    global aeval

    aeval = Interpreter(err_writer = dev_null, writer = dev_null, user_symbols = USER_SYMBOLS)

    args = parser.parse_args()

    global isdebug
    isdebug = args.debug

    output_path = args.map_path[0] if args.output == "|" else args.output[0]

    module_fa = os.path.dirname(args.infopath)

    module_name = os.path.basename(args.infopath)

    sys.path.append(module_fa)

    if module_name[-3:] == ".py":
        module_name = module_name[:-3]
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

    debug_pdb()

    standard_out(isverbose, "\t\t\t\t------------------------------")
    standard_out(isverbose, "\t\t\t\t--------Initialization--------")
    standard_out(isverbose, "\t\t\t\t------------------------------")

    standard_out(isverbose, "Map data is being imported...")

    map_now = rw.RWmap.init_mapfile(f'{args.map_path[0]}')

    info_doids_dict = {}
    info_dict = {}
    ids_now_dict = {}
    
    dtobject = []

    id_to_tobject = {}

    info_tagged_objects_exist = []

    standard_out(isverbose, "The maximum ID of object in RW maps is resetting...")
    map_now.resetnextobjectid()

    standard_out(isverbose, "ID mapping is being established...")
    for tobject in map_now.iterator_object_s():
        id_to_tobject[tobject.returnDefaultProperty("id")] = tobject

    standard_out(isverbose, "The info object is rearranging...")
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
        standard_error(f"External info import loop error.", 1)

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
            standard_error(f"Info input dependence loop error.({key})", 5)

    standard_out(isverbose, "\t\t\t\t--------------------------------------")
    standard_out(isverbose, "\t\t\t\t--------Info objects procedure--------")
    standard_out(isverbose, "\t\t\t\t--------------------------------------")
    for key, info in info_now.items():
        for tobject in map_now.iterator_object_s(default_re = {rw.const.OBJECTDE.type: r"(?!.+)", 
                                                               rw.const.OBJECTDE.name: r".+"}):
            info_name = tobject.returnDefaultProperty(rw.const.OBJECTDE.name)

            if bool(re.match(key, info_name)):
                tobject_id = tobject.returnDefaultProperty("id")
                standard_out(isverbose, f"An object(ID:{tobject_id}, name:{info_name}) has been identified as an info object. Initialization...")
                info_dict_now = {}

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
                                standard_error(f"External info import error(target_info:{info_pre_now},info_key:{value_name},info_prefix:{info_dict_now[value_name]}).", 0)
                            info_temp = info_now[tar_info[AUTOKEY.info_key]]
                            if tar_info[AUTOKEY.isdelete_sym] and (info_temp.get(AUTOKEY.isinfo_sub) != None and info_temp[AUTOKEY.isinfo_sub] == True):
                                standard_error(f"External info import error(The target info has \",d\")(target_info:{info_pre_now},info_key:{value_name},info_prefix:{info_dict_now[value_name]}).", 10)
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

                        info_dict_now[key_now] = mapvalue_to_value(tobject_temp.returnOptionalProperty(key_now), ntype)
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
                        info_dict_now[key_now] = brace_translation(info_dict_now[key_now], info_dict_now, ones = True)


                info[AUTOKEY.isinfo_sub] = (info.get(AUTOKEY.isinfo_sub) != None and info[AUTOKEY.isinfo_sub])



                info_dict_now[AUTOKEY.prefix] = info_dict_now[info[AUTOKEY.prefix]]
                info_doids_dict[info_dict_now[AUTOKEY.prefix]] = deepcopy(info)

                info_dict_now[AUTOKEY.info] = info_dict_now[AUTOKEY.prefix]

                info_dict_now[AUTOKEY.tobject] = tobject
                info_dict_now[AUTOKEY.info_key] = key

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
                        
                        elif operation_now[AUTOKEY.operation_type] == AUTOKEY.typeset:
                            for key_n, value in operation_now.items():
                                if key_n != AUTOKEY.operation_type and key_n != AUTOKEY.totype:
                                    if operation_now.get(AUTOKEY.totype) == None:
                                        object_dict[str_translation(key_n, object_dict)] = value
                                    else:
                                        object_dict[str_translation(key_n, object_dict)] = str_to_type(type_to_str(value, get_type(value)), operation_now[AUTOKEY.totype])
                        elif operation_now[AUTOKEY.operation_type] == AUTOKEY.typeset_expression:
                            depth_now = MAXTRANSDEPTH if operation_now.get(AUTOKEY.depth) == None else operation_now[AUTOKEY.depth]
                            for key_n, value in operation_now.items():
                                if key_n != AUTOKEY.operation_type and key_n != AUTOKEY.depth:
                                    object_dict[str_translation(key_n, object_dict, depth = depth_now)] = brace_translation(value, object_dict)
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
                                    for i in range(num):
                                        info_dict_now[key_trans] = mapvalue_to_value(str_translation(operation_now[AUTOKEY.real_idexp], object_dict), str)
                        elif operation_now[AUTOKEY.operation_type] == AUTOKEY.typeadd_args:
                            for key_n, value in operation_now.items():
                                if key_n != AUTOKEY.operation_type:
                                    value_brace = brace_translation(value, object_dict)
                                    value_brace = aeval_globals(value_brace)
                                    info_doids_dict[info_dict_now[AUTOKEY.prefix]][AUTOKEY.args].append((str_translation(key_n, object_dict), value_brace))
                        elif operation_now[AUTOKEY.operation_type] == AUTOKEY.typeadd_opargs:
                            for key_n, value in operation_now.items():
                                if key_n != AUTOKEY.operation_type:
                                    value_brace = brace_translation(value, object_dict)
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
                            standard_error(str_translation(operation_now[AUTOKEY.error_info]), -1)
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
                            standard_error(f"An argument of the info object is invalid.(ID:{tobject_id}, name:{info_name}, arg:{key_now})", 12)

                if info_new.get(AUTOKEY.opargs) != None:
                    for value in info_new[AUTOKEY.opargs].values():
                        args_now = value[0].split(AUTOKEY.opargs_sys_seg)
                        if len(args_now) == 2:
                            args_dict[args_now[0]] = value[1]
                        args_now = args_now[0]
                        if info_new[AUTOKEY.info_args].get(args_now) == None and info_new[AUTOKEY.no_check] == False:
                            standard_error(f"An optional argument of the info object is invalid.(ID:{tobject_id}, name:{info_name}, arg:{args_now})", 13)

                # var_dependent check
                
                for key_now, ntype in info_new[AUTOKEY.info_args].items():
                    if tobject.returnOptionalProperty(key_now) != None:
                        if info_new.get(AUTOKEY.var_dependent) != None and info_new[AUTOKEY.var_dependent].get(key_now) != None:
                            for args_dependent in info_new[AUTOKEY.var_dependent][key_now].split(","):
                                if (args_dict.get(args_dependent) == None or args_dict[args_dependent] == False):
                                    standard_error(f"Unuseful arguments in an info object.({key_now} exists but {args_dependent} is none or false.)", 4)

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
                        standard_error(f"A required argument is missing in an info object.({str(key_now)})", 6)
                
                if len(tobject_temp._optional_properties) != 0 and info_new[AUTOKEY.no_check] == False:
                        standard_error("Unknown arguments below in an info object.", 3, f"{tobject_temp._optional_properties}")


                standard_out(isverbose, "Info object information is being output...")
                if isverbose:
                    temp_pri = OrderedDict()
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
                    standard_out(isverbose, temp_pri)


                info_dict[info_dict_now[AUTOKEY.prefix]] = info_dict_now
                if isdelete_all or isdelete or info_dict_now[AUTOKEY.isdelete_all_sym] or (isdelete_d and info_dict_now[AUTOKEY.isdelete_sym]):
                    dtobject.append(tobject)
                else:
                    info_tagged_objects_exist.append(tobject)

    info_now = info_doids_dict

    standard_out(isverbose and (isdelete_all or isdelete), "The info object is being deleted...")
    standard_out(isverbose and (isdelete_d), "The info object is being deleted if eligible...")
    for tobject in dtobject:
        map_now.delete_object_s(tobject)
        tobject_id = tobject.returnDefaultProperty("id")
        standard_out(isverbose, f"An info object(ID:{tobject_id}, name:{tobject.returnDefaultProperty(rw.const.OBJECTDE.name)}) has been deleted...")

    standard_out(isverbose, "\t\t\t\t----------------------------------------")
    standard_out(isverbose, "\t\t\t\t--------Tagged objects procedure--------")
    standard_out(isverbose, "\t\t\t\t----------------------------------------")

    standard_out(isverbose, "The ids of tagged objects are collecting...")
    for tobject in map_now.iterator_object_s(default_re = {rw.const.OBJECTDE.type: r"(?!.+)", 
                                                           rw.const.OBJECTDE.name: r".+"}):
        tobject_name = tobject.returnDefaultProperty(rw.const.OBJECTDE.name)
        ischange__newname__myinfo__info = is_tagged_tobject__newname__myinfo__info(tobject_name, info_dict, info_now)
        ischange = ischange__newname__myinfo__info[0]
        tobject_name_to_solve = ischange__newname__myinfo__info[1]
        myinfo = ischange__newname__myinfo__info[2]
        info = ischange__newname__myinfo__info[3]
        if ischange:
            if myinfo.get(AUTOKEY.ids) != None:
                tobject_ids_do(tobject, myinfo, info, ids_now_dict, isreset)

    dtobject = []
    tobject_list = [tobject for tobject in map_now.iterator_object_s(default_re = {rw.const.OBJECTDE.type: r"(?!.+)", 
                                                           rw.const.OBJECTDE.name: r".+"}) if is_tagged_object_simple(tobject) and (tobject.returnOptionalProperty(AUTOKEY.IDdep) == None or tobject.returnOptionalProperty(AUTOKEY.IDdep) == '0')]
    index_tobject = 0
    while index_tobject < len(tobject_list):
        tobject = tobject_list[index_tobject]
        insert_index = index_tobject + 1
        index_tobject = index_tobject + 1

        tobject_name = tobject.returnDefaultProperty(rw.const.OBJECTDE.name)
        tobject_id = tobject.returnDefaultProperty("id")
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
                object_dict.update(get_args(myinfo, tobject_name_to_solve, tobject, id_to_tobject, map_now))
                
                if info.get(AUTOKEY.info_prefix) != None:
                    for info_pre in info[AUTOKEY.info_prefix]:
                        info_temp = info_dict[info_pre]
                        object_dict.update(info_temp)
                ischange = True
                break
        if ischange:

            if tobject.returnOptionalProperty(AUTOKEY.IDdep) == None:
                tobject.assignOptionalProperty(AUTOKEY.IDdep, "0")
            tobject_IDdep = int(tobject.returnOptionalProperty(AUTOKEY.IDdep))
            
            if myinfo.get(AUTOKEY.isinfo_sub) != None and myinfo.get(AUTOKEY.isinfo_sub) == True:
                standard_error(f"Incorrect use of the subordinate info object.(ID:{tobject_id}, name:{tobject_name})", 2)
            isdelete_sym = bool(re.match(AUTOKEY.delete_symbol, tobject_name)) or info[AUTOKEY.isdelete_sym]
            isdelete_all_sym = bool(re.match(AUTOKEY.delete_all_symbol, tobject_name)) or info[AUTOKEY.isdelete_all_sym]
            if isdelete_all or isdelete or isdelete_all_sym or (isdelete_sym and isdelete_d):
                dtobject.append(tobject)
            else:
                if tobject.returnOptionalProperty(AUTOKEY.IDfa) == None:
                    info_tagged_objects_exist.append(tobject)
            standard_out(isverbose and (not(isdelete_sym or isdelete_all or isdelete_all_sym)), f"An object(ID:{tobject_id}, name:{tobject_name}) has been identified as a tagged object. Object generation...")
            standard_out(isverbose and (isdelete_all or isdelete_all_sym), f"An object(ID:{tobject_id}, name:{tobject_name}) has been identified as a tagged object. All objects generated by this tagged object and itself will be deleted...")
            standard_out(isverbose and (isdelete_sym and(not (isdelete_all or isdelete_all_sym))), f"An object(ID:{tobject_id}, name:{tobject_name}) has been identified as a tagged object with deleted tag. The objects will not be generated, existing ones will also be deleted...")

            if myinfo.get(AUTOKEY.ids) != None:
                for thing in myinfo[AUTOKEY.ids]:
                    
                    idprefix = brace_translation(thing[0], object_dict, ones = True)
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
                        if (isdelete_sym or isdelete_all_sym or isdelete_all) and isreset:
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
                        dtobject.append(id_to_tobject[ids])
                continue
            
            operation_index = {}
            for index, operation_now in enumerate(myinfo[AUTOKEY.operation]):
                if operation_now[AUTOKEY.operation_type] == AUTOKEY.tag:
                    if operation_index.get(operation_now[AUTOKEY.tag]) != None:
                        standard_error(f"operation tags are duplicated.({operation_now[AUTOKEY.tag]})", 15)
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
                            idnow_object:rw.case.TObject = deepcopy(id_to_tobject[object_dict[AUTOKEY.IDs][tottobid]])
                            if isnewtaggedobject:
                                if is_tagged_object_simple(idnow_object):
                                    object_now._optional_properties = deepcopy(idnow_object._optional_properties)
                            else:
                                if is_tagged_object_simple(idnow_object):
                                    idnow_object.assignDefaultProperty(rw.const.OBJECTDE.name, idnow_object.returnDefaultProperty(rw.const.OBJECTDE.name) + AUTOKEY.delete_all_op)
                                    tobject_list.append(idnow_object)
                                    map_now.addObject_type(idnow_object, isresetid = True)
                            id_to_tobject[object_dict[AUTOKEY.IDs][tottobid]].copy(object_now)
                        else:
                            map_now.addObject_type(object_now)
                            if not isdelete:
                                IDs_update(tobject, object_now)
                        tottobid = tottobid + 1
                    
                elif operation_now[AUTOKEY.operation_type] == AUTOKEY.goto:
                    index = operation_index[operation_now[str_translation(AUTOKEY.goto_tag, object_dict)]]
                    continue

                elif operation_now[AUTOKEY.operation_type] == AUTOKEY.typeif:
                    if not brace_translation(operation_now[AUTOKEY.ifvar], object_dict):
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
                            for key_n, value in operation_now.items():
                                if key_n != AUTOKEY.operation_type and key_n != AUTOKEY.depth:
                                    object_dict[str_translation(key_n, object_dict, depth = depth_now)] = brace_translation(value, object_dict)
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
                    standard_error(str_translation(operation_now[AUTOKEY.error_info]), -1)
                elif operation_now[AUTOKEY.operation_type] == AUTOKEY.pdb_pause:
                    debug_pdb(object_dict)
                index = index + 1

            id_delete = IDs_balance(tobject, tottobid)
            for idnow in id_delete:
                if is_tagged_object_simple(id_to_tobject[idnow]):
                    id_to_tobject[idnow].assignDefaultProperty(rw.const.OBJECTDE.name, id_to_tobject[idnow].returnDefaultProperty(rw.const.OBJECTDE.name) + AUTOKEY.delete_all_op)
                    tobject_list.append(id_to_tobject[idnow])
                else:
                    dtobject.append(id_to_tobject[idnow])

            if object_dict.get(AUTOKEY.cite_name) != None:
                for key, value in object_dict.items():
                    if cite_object_dict.get(object_dict[AUTOKEY.cite_name] + "." + key) != None:
                        standard_error(f"Reference tags are duplicated. An object(ID:{tobject_id}, name:{tobject_name}, Cite:{object_dict[AUTOKEY.cite_name]})", 14)
                    cite_object_dict[object_dict[AUTOKEY.cite_name] + "." + key] = deepcopy(value)
      

    standard_out(isverbose and (isdelete_all or isdelete), "The tagged object is being deleted...")
    standard_out(isverbose and (isdelete_d), "The tagged object is being deleted if eligible...")
    for tobject in dtobject:
        map_now.delete_object_s(tobject)

    debug_pdb()
    if iscitetrans:
        standard_out(isverbose, "Other objects are being translated by cite.")
        for tobject in map_now.iterator_object_s(default_re = {rw.const.OBJECTDE.type: r"(.+)"}):
            for key, value in tobject._default_properties.items():
                value_now = mapvalue_to_value_basic(value)
                if not isinstance(value_now, bool):
                    tobject.assignDefaultProperty(key, brace_one_translation_cycle(value_now, cite_object_dict, AUTOKEY.not_useful_char_ad_point_for_cite))
            for key, value in tobject._optional_properties.items():
                value_now = mapvalue_to_value_basic(value)
                if not isinstance(value_now, bool):
                    tobject.assignOptionalProperty(key, brace_one_translation_cycle(value_now, cite_object_dict, AUTOKEY.not_useful_char_ad_point_for_cite))

    standard_out(isverbose, "\t\t\t\t----------------------------------------")
    standard_out(isverbose, "\t\t\t\t--------Rearrangement and output--------")
    standard_out(isverbose, "\t\t\t\t----------------------------------------")
    
    standard_out(isverbose, "Info and tagged objects are rearranging...")
    
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

    standard_out(isverbose and isresetid, "The IDs are rearranging...")

    if isresetid:

        id_mapping = {}
        id_now = 1
        for tobject in map_now.iterator_object_s():
            tobid = tobject.returnDefaultProperty("id")
            if id_mapping.get(tobid) != None:
                standard_error(f"The IDs are coincident and the mapping cannot be performed.(ID:{tobid})", 11)
            
            id_mapping[tobid] = str(id_now)
            id_now = id_now + 1
        id_now = 1
        for tobject in map_now.iterator_object_s():
            tobid = tobject.returnDefaultProperty("id")
            if is_tagged_object_simple(tobject):
                ids_now = tobject.returnOptionalProperty(AUTOKEY.IDs)
                if ids_now != None:
                    if ids_now == "":
                        continue
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

    standard_out(isverbose, "New RW map is being establishing...")
    map_now.write_file(output_path)

    dev_null.close()

if __name__ == "__main__":
    auto_func()        
