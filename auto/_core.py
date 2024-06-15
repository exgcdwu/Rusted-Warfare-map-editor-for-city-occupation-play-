from typing import Union
from copy import deepcopy
import re
import os
from asteval import Interpreter
from pprint import pprint
import argparse
import importlib

import sys

current_file_path = os.path.abspath(__file__)
current_dir_path = os.path.dirname(current_file_path)
package_dir = os.path.dirname(current_dir_path)

sys.path.append(package_dir)
import rwmap as rw

class AUTOKEY:
    info_args = "info_args"
    default_args = "default_args"
    prefix = "prefix"
    info = "info"
    args = "args"
    seg = "seg"
    opargs = "opargs"
    opargs_seg = "opargs_seg"
    opargs_prefix_len = "opargs_prefix_len"
    ids = "ids"
    IDs = "IDs"
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
    info_prefix = "info_prefix"

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
    id_operation = "id_operation"
    real_idexp = "real_idexp"
    
    normal_city_nexist_re = ".*_"
    opargs_sys_seg = "|"
    IDs_seg = ","
    delete_symbol = ".*,d"
    not_useful_char = "[^A-Za-z0-9_{}]"






def get_args(info:dict, name:str, object_dict:dict, tobject:rw.case.TObject, isreset:bool, id_to_tobject:dict, rwmap_now:rw.RWmap)->dict:
    args_dict = {}
    split_now = name.split(info[AUTOKEY.opargs_seg])
    opargs = split_now[1:]
    split_now = split_now[0].split(info[AUTOKEY.seg])
    if object_dict.get(AUTOKEY.isprefixseg) != None and object_dict.get(AUTOKEY.isprefixseg) == True:
        args_n = split_now[1:]
    else:
        args_n = [split_now[0][len(object_dict[AUTOKEY.prefix]):]] + split_now[1:]
    
    for index, thing in enumerate(info[AUTOKEY.args]):
        args_dict[thing[0]] = thing[1](args_n[index])
    
    prefix_len = info[AUTOKEY.opargs_prefix_len]

    for oparg in opargs:
        prefix_now = oparg[0:prefix_len]
        var_now = oparg[prefix_len:]
        if info[AUTOKEY.opargs].get(prefix_now) != None:
            info_thing = info[AUTOKEY.opargs][prefix_now]
            args_dict[info_thing[0].split(AUTOKEY.opargs_sys_seg)[0]] = info_thing[1](var_now)

    for key, info_thing in info[AUTOKEY.opargs].items():
        args_dict[info_thing[0].split(AUTOKEY.opargs_sys_seg)[0]] = \
        mapvalue_to_value(info_thing[0].split(AUTOKEY.opargs_sys_seg)[1], info_thing[1])

    tobject_ids = tobject.returnOptionalProperty(AUTOKEY.IDs)
    tobject_ids = tobject_ids.split(AUTOKEY.IDs_seg) if tobject_ids != None else []
    if isreset:
        tobject.deleteOptionalProperty(AUTOKEY.IDs)
        args_dict[AUTOKEY.IDs] = []
        for tobjectid in tobject_ids:
            rwmap_now.delete_object_s(id_to_tobject[tobjectid])
    else:
        args_dict[AUTOKEY.IDs] = tobject_ids

    return args_dict

def match_compare(match_value:list)->int:
    return -match_value[0].start()

def brace_translation(expression_b:str, dict_name:dict, prev:bool = True):
    #import pdb;pdb.set_trace()
    expression_b = " " + expression_b + " "
    match_value_list = []
    for key, value in dict_name.items():
        match_list_now = [re_now for re_now in re.finditer(AUTOKEY.not_useful_char + key + AUTOKEY.not_useful_char, expression_b)]
        match_value_list = match_value_list + [[match_now, str(value)] for match_now in match_list_now]
    match_value_list.sort(key = match_compare)
    #import pdb;pdb.set_trace()
    for match_value in match_value_list:
        match_now = match_value[0]
        value_now = match_value[1]
        expression_b = expression_b[:match_now.start() + 1] + value_now + expression_b[match_now.end() - 1:]

    expression_b = expression_b[1:len(expression_b) - 1]
    if len(match_value_list) == 0:
        if prev:
            expression_b = expression_translation(expression_b, dict_name, False)
    else:
        expression_b = expression_translation(expression_b, dict_name)


    try:
        expression_b_temp = aeval(expression_b)
    except Exception as e:
        return expression_b
    else:
        if expression_b_temp == None:
            return expression_b
        return expression_b_temp

def expression_translation(expression_s:str, dict_name:dict, prev:bool = True):
    lb_now = re.match(".*{", expression_s)
    rb_now = re.match(".*}", expression_s)
    if lb_now and rb_now:
        translation_value = brace_translation(expression_s[lb_now.end():rb_now.end() - 1], dict_name)
        expression_s = expression_s[:lb_now.end() - 1] + type_to_str(translation_value, get_type(translation_value)) + expression_s[rb_now.end(): ]
        return expression_translation(expression_s, dict_name)
    else:
        if prev:
            return brace_translation(expression_s, dict_name, False)
        else:
            return expression_s
        
    


def str_translation(value:Union[str, bool], dict_name:dict)->str:
    if isinstance(value, bool):
        return value_to_mapvalue(value, bool)
    if isinstance(value, dict):
        return deepcopy(value)
    if bool(re.match(".*{", value)):
        if not bool(re.match(".*}", value)):
            raise ValueError("The string have '{' but don't have'}'.")
    value_list = value.split("{")
    value_ans = value_list[0]
    for index in range(1, len(value_list)):
        value_list_now = value_list[index].split("}")
        value_temp = brace_translation(value_list_now[0], dict_name)
        value_list_now[0] = type_to_str(value_temp, get_type(value_temp))
        value_ans = value_ans + "".join(value_list_now)
    if bool(re.match(".*{", value_ans)):
        return str_translation(value_ans, dict_name)
    return value_ans

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
        default_pro[rw.const.OBJECTDE.name] = str_translation(operation[AUTOKEY.name], dict_name)
    if operation.get(AUTOKEY.type) != None:
        default_pro[rw.const.OBJECTDE.type] = operation[AUTOKEY.type]

    optional_pro = {key:str_translation(value, dict_name) for key, value in operation[AUTOKEY.optional].items()}

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

def auto_func():
    parser = argparse.ArgumentParser(
        description='Objects of Triggers are automatically processed by information\'s mode.')
    parser.add_argument('map_path', action = "store", metavar = 'file', type=str, nargs = 1, 
                        help='The input path of RW map file.')
    parser.add_argument("-i", "--info", 
                        action = "store", metavar = "file", type = str, nargs = 1, 
                        required = False, default = current_dir_path + "\\_data.py", 
                        help = "The file's path which has information's mode variable|current_file_path"
                        )
    parser.add_argument("-v", "--var", 
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

    parser.add_argument("--debug", 
                        action = 'store_true', help = 'Mode of debuging.')

    dev_null = open(os.devnull, "w")
    global aeval
    aeval = Interpreter(err_writer = dev_null, writer = dev_null)


    args = parser.parse_args()
    map_now = rw.RWmap.init_mapfile(f'{args.map_path[0]}')
    output_path = args.map_path[0] if args.output == "|" else args.output[0]
    sys.path.append("".join(args.info.split("\\")[:-1]))
    info_file = importlib.import_module(".".join(".".join(args.info.split("\\")[-2:]).split(".")[:-1]))
    info_now = getattr(info_file, args.var, 'Not Found')
    isdelete = args.DeleteAllSym
    isdelete_d = args.delete
    isdelete_all = args.DeleteAll
    isreset = args.reset
    isdebug = args.debug

    info_doids_dict = {}
    info_dict = {}
    ids_now_dict = {}
    
    dtobject = []

    id_to_tobject = {}

    map_now.resetnextobjectid()

    brace_translation("i + 1", {"i": "0"})

    for tobject in map_now.iterator_object_s():
        id_to_tobject[tobject.returnDefaultProperty("id")] = tobject
                
    for key, info in info_now.items():
        for tobject in map_now.iterator_object_s(default_re = {rw.const.OBJECTDE.type: r"(?!.+)", 
                                                               rw.const.OBJECTDE.name: r".+"}):
            info_name = tobject.returnDefaultProperty(rw.const.OBJECTDE.name)
            
            if bool(re.match(key, info_name)):
                info_dict_now = {}
                info_dict_now[AUTOKEY.isdelete_sym] = bool(re.match(AUTOKEY.delete_symbol, info_name))

                for key_now, value in info[AUTOKEY.default_args].items():
                    info_dict_now[key_now] = mapvalue_to_value(value, info[AUTOKEY.info_args][key_now])
                for key_now, ntype in info[AUTOKEY.info_args].items():
                    if tobject.returnOptionalProperty(key_now) != None:
                        info_dict_now[key_now] = mapvalue_to_value(tobject.returnOptionalProperty(key_now), ntype)

                info_dict_now[AUTOKEY.prefix] = info_dict_now[info[AUTOKEY.prefix]]
                info_doids_dict[info_dict_now[AUTOKEY.prefix]] = deepcopy(info)
                info_dict_now[AUTOKEY.info] = info_dict_now[AUTOKEY.prefix]

                info_dict_now[AUTOKEY.tobject] = tobject
                if info.get(AUTOKEY.info_prefix) != None and info_dict_now.get(info[AUTOKEY.info_prefix]) != None:
                    info_dict_now[AUTOKEY.info_prefix] = info_dict_now[info[AUTOKEY.info_prefix]]

                if info.get(AUTOKEY.id_operation) != None:
                    operation_index = {}
                    for index, operation_now in enumerate(info[AUTOKEY.id_operation]):
                        if operation_now[AUTOKEY.operation_type] == AUTOKEY.tag:
                            operation_index[operation_now[AUTOKEY.tag]] = index
                    
                    object_dict = deepcopy(info_dict_now)
                    index = 0

                    while(index < len(info[AUTOKEY.id_operation])):
                        
                        operation_now = info[AUTOKEY.id_operation][index]
                            
                        if operation_now[AUTOKEY.operation_type] == AUTOKEY.goto:
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
                            for key, value in operation_now.items():
                                if key != AUTOKEY.operation_type:
                                    object_dict[str_translation(key, object_dict)] = brace_translation(value, object_dict)
                        elif operation_now[AUTOKEY.operation_type] == AUTOKEY.changetype:
                            for key in operation_now[AUTOKEY.keyname_list]:
                                str_trans = str_translation(key, object_dict)
                                value = object_dict[str_trans]
                                object_dict[str_trans] = str_to_type(type_to_str(value, get_type(value)), operation_now[AUTOKEY.totype])
                        elif operation_now[AUTOKEY.operation_type] == AUTOKEY.typeset_exist:
                            for key, value in operation_now.items():
                                if key != AUTOKEY.operation_type:
                                    object_dict[str_translation(key, object_dict)] = object_dict.get(value) != None
                        elif operation_now[AUTOKEY.operation_type] == AUTOKEY.typeset_id:

                            for key, value in operation_now.items():
                                if key != AUTOKEY.operation_type and key != AUTOKEY.real_idexp:
                                    key_trans = str_translation(key, object_dict)
                                    num = brace_translation(value, object_dict)
                                    info_doids_dict[info_dict_now[AUTOKEY.prefix]][AUTOKEY.ids].append([key_trans, num])
                                    for i in range(num):
                                        info_dict_now[key_trans] = mapvalue_to_value(str_translation(operation_now[AUTOKEY.real_idexp], object_dict), str)
                        index = index + 1
                    
            
                info_dict[info_dict_now[AUTOKEY.prefix]] = info_dict_now
                if isdelete_all or isdelete or (isdelete_d and info_dict_now[AUTOKEY.isdelete_sym]):
                    dtobject.append(tobject)

    info_now = info_doids_dict



    for tobject in dtobject:
        map_now.delete_object_s(tobject)

    for tobject in map_now.iterator_object_s(default_re = {rw.const.OBJECTDE.type: r"(?!.+)", 
                                                           rw.const.OBJECTDE.name: r".+"}):
        tobject_name = tobject.returnDefaultProperty(rw.const.OBJECTDE.name)
        ischange = False
        for key, info in info_dict.items():
            prefix_now = info[AUTOKEY.prefix]
            if prefix_now == tobject_name[0:len(prefix_now)] \
                and (not re.match(AUTOKEY.normal_city_nexist_re, tobject_name)):
                info_key = info[AUTOKEY.info]
                myinfo = info_now[info_key]
                object_dict = get_args(myinfo, tobject_name, info, tobject, isreset, id_to_tobject, map_now)
                
                ischange = True
                break
        if ischange:
            
            for thing_prefix_num in myinfo[AUTOKEY.ids]:
                tobject_prefix = tobject.returnOptionalProperty(thing_prefix_num[0])
                if tobject_prefix != None:
                    tobject_prefix = tobject_prefix.split(",")
                else:
                    tobject_prefix = []
                if isreset:
                    tobject.deleteOptionalPropertySup([AUTOKEY.IDs])
                    tobject_prefix = []

                prefix_now = brace_translation(thing_prefix_num[0], info)
                if ids_now_dict.get(prefix_now) == None:
                    ids_now_dict[prefix_now] = 1
                
                for index in range(len(tobject_prefix)):
                    tobject_prefix[index] = int(tobject_prefix[index][len(thing_prefix_num[0]):])
                    ids_now_dict[prefix_now] = max(ids_now_dict[prefix_now], 
                                                            tobject_prefix[index])

    dtobject = []

    

    for tobject in map_now.iterator_object_s(default_re = {rw.const.OBJECTDE.type: r"(?!.+)", 
                                                           rw.const.OBJECTDE.name: r".+"}):
        tobject_name = tobject.returnDefaultProperty(rw.const.OBJECTDE.name)
        ischange = False
        for key, info in info_dict.items():
            prefix_now = info[AUTOKEY.prefix]
            info_key = info[AUTOKEY.info]
            info_tobject:rw.case.TObject = info[AUTOKEY.tobject]
            if prefix_now == tobject_name[0:len(prefix_now)] \
                and (not re.match(AUTOKEY.normal_city_nexist_re, tobject_name)):
                myinfo = info_now[info_key]
                object_dict = get_args(myinfo, tobject_name, info, tobject, isreset, id_to_tobject, map_now)
                object_dict.update(info)
                if info.get(AUTOKEY.info_prefix) != None:
                    for info_pre in info[AUTOKEY.info_prefix]:
                        info_temp = info_dict[info_pre]
                        object_dict.update(info_temp)
                ischange = True
                break
        if ischange:

            isdelete_sym = bool(re.match(AUTOKEY.delete_symbol, tobject_name)) or info[AUTOKEY.isdelete_sym]
            if isdelete_all or isdelete or (isdelete_sym and isdelete_d):
                dtobject.append(tobject)


            for thing in myinfo[AUTOKEY.ids]:
                
                idprefix = brace_translation(thing[0], object_dict)
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
            if isdelete_all or isdelete_sym:
                if object_dict.get(AUTOKEY.IDs) != None:
                    for ids in object_dict[AUTOKEY.IDs]:
                        dtobject.append(id_to_tobject[ids])
                continue
            
            operation_index = {}
            for index, operation_now in enumerate(myinfo[AUTOKEY.operation]):
                if operation_now[AUTOKEY.operation_type] == AUTOKEY.tag:
                    operation_index[operation_now[AUTOKEY.tag]] = index

            tottobid = 0
            index = 0

            if isdebug:
                pprint(tobject)
                pprint(object_dict)

            while(index < len(myinfo[AUTOKEY.operation])):
                
                operation_now = myinfo[AUTOKEY.operation][index]

                if isdebug:
                    print(index)
                    if index == 16:
                        pprint(operation_now)
                    elif index == 13:
                        pprint(operation_now)
                    elif index == 21:
                        print("i = ", object_dict.get("i"))
                        print("j = ", object_dict.get("j"))
                        print("isi_eq_0 = ", object_dict.get("isi_eq_0"))
                        print("teamDetectname = ", object_dict.get("teamDetectname"))

                if operation_now[AUTOKEY.operation_type] == AUTOKEY.object:
                    object_now = get_tobject(operation_now, object_dict, ori_pos, ori_size)

                    if object_now != None:
                        if isdebug:
                            print(object_now)
                            
                        #import pdb;pdb.set_trace()
                        if object_dict.get(AUTOKEY.IDs) != None and tottobid < len(object_dict[AUTOKEY.IDs]):
                            object_now.assignDefaultProperty("id", object_dict[AUTOKEY.IDs][tottobid])
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
                    for key, value in operation_now.items():
                        if key != AUTOKEY.operation_type:
                            object_dict[str_translation(key, object_dict)] = brace_translation(value, object_dict)
                elif operation_now[AUTOKEY.operation_type] == AUTOKEY.changetype:
                    for key in operation_now[AUTOKEY.keyname_list]:
                        str_trans = str_translation(key, object_dict)
                        value = object_dict[str_trans]
                        object_dict[str_trans] = str_to_type(type_to_str(value, get_type(value)), operation_now[AUTOKEY.totype])
                elif operation_now[AUTOKEY.operation_type] == AUTOKEY.typeset_exist:
                    for key, value in operation_now.items():
                        if key != AUTOKEY.operation_type:
                            object_dict[str_translation(key, object_dict)] = object_dict.get(value) != None
                index = index + 1
                

            id_delete = IDs_balance(tobject, tottobid)
            for idnow in id_delete:
                dtobject.append(id_to_tobject[idnow])
                    
    for tobject in dtobject:
        map_now.delete_object_s(tobject)

    map_now.resetnextobjectid()

    map_now.write_file(output_path)
    dev_null.close()

if __name__ == "__main__":
    auto_func()        
