from typing import Union
from copy import deepcopy
import re
import argparse
import importlib
import os
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
    
    normal_city_nexist_re = ".*_"
    opargs_sys_seg = "|"
    IDs_seg = ","




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
        value_list_now[0] = dict_name[value_list_now[0]]
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
    offset = offset if offset != None else rw.frame.Coordinate()
    offsetsize = operation.get(AUTOKEY.offsetsize)
    offsetsize = offsetsize if offsetsize != None else rw.frame.Coordinate()
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
        return ntype(value)

def value_to_mapvalue(value, ntype):
    if ntype == bool:
        return {"value": str(bool(value)).lower(), "type": "bool"}
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
        idsh = ""
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
                        action = 'store_true', help = 'Delete all info and tagged objects.')

    parser.add_argument("-r", "--reset", 
                        action = 'store_true', help = 'Reset the ids of objects.(not recommend)')

    args = parser.parse_args()
    map_now = rw.RWmap.init_mapfile(f'{args.map_path[0]}')
    output_path = args.map_path[0] if args.output == "|" else args.output[0]
    sys.path.append("".join(args.info.split("\\")[:-1]))
    info_file = importlib.import_module(".".join(".".join(args.info.split("\\")[-2:]).split(".")[:-1]))
    info_now = getattr(info_file, args.var, 'Not Found')
    isdelete = args.delete
    isreset = args.reset

    info_dict = {}
    ids_now_dict = {}
    
    dtobject = []

    id_to_tobject = {}

    for tobject in map_now.iterator_object_s():
        id_to_tobject[tobject.returnDefaultProperty("id")] = tobject
                
    for key, info in info_now.items():
        for tobject in map_now.iterator_object_s(default_re = {rw.const.OBJECTDE.type: r"(?!.+)", 
                                                               rw.const.OBJECTDE.name: r".+"}):
            if key == tobject.returnDefaultProperty(rw.const.OBJECTDE.name):
                info_dict_now = {}
                for key_now, value in info[AUTOKEY.default_args].items():
                    info_dict_now[key_now] = mapvalue_to_value(value, info[AUTOKEY.info_args][key_now])
                for key_now, ntype in info[AUTOKEY.info_args].items():
                    if tobject.returnOptionalProperty(key_now) != None:
                        info_dict_now[key_now] = mapvalue_to_value(tobject.returnOptionalProperty(key_now), ntype)
                info_dict_now[AUTOKEY.prefix] = info_dict_now[info[AUTOKEY.prefix]]
                info_dict_now[AUTOKEY.info] = key
                info_dict_now[AUTOKEY.tobject] = tobject
                IDs = tobject.returnOptionalProperty(AUTOKEY.IDs)
                if IDs != None:
                    idlist = IDs.split(AUTOKEY.IDs_seg)[1:]
                    info_dict_now[AUTOKEY.IDs] = idlist
                info_dict[info_dict_now[AUTOKEY.prefix]] = info_dict_now
                dtobject.append(tobject)
    if isdelete:
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

                tobject_prefix = tobject.returnDefaultProperty(thing_prefix_num[0])
                if tobject_prefix != None:
                    tobject_prefix = tobject_prefix.split(",")
                else:
                    tobject_prefix = []
                if isreset:
                    tobject.deleteOptionalPropertySup([AUTOKEY.IDs])
                
                if ids_now_dict.get(thing_prefix_num[0]) == None:
                    ids_now_dict[info[thing_prefix_num[0]]] = 1
                
                for index in range(len(tobject_prefix)):
                    tobject_prefix[index] = int(tobject_prefix[index][len(thing_prefix_num[0]):])
                    ids_now_dict[info[thing_prefix_num[0]]] = max(ids_now_dict[thing_prefix_num[0]], 
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
                ischange = True
                break
        if ischange:
            for thing in myinfo[AUTOKEY.ids]:
                idprefix = object_dict[thing[0]]
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
            dtobject.append(tobject)
            tottobid = 0
            for index, operation_now in enumerate(myinfo[AUTOKEY.operation]):
                object_now = get_tobject(operation_now, object_dict, ori_pos, ori_size)
                if object_now != None:
                    if object_dict.get(AUTOKEY.IDs) != None and tottobid < len(object_dict[AUTOKEY.IDs]):
                        object_now.assignDefaultProperty("id", object_dict[AUTOKEY.IDs][tottobid])
                        id_to_tobject[object_dict[AUTOKEY.IDs][tottobid]].copy(object_now)
                    else:
                        map_now.addObject_type(object_now)
                        if not isdelete:
                            IDs_update(tobject, object_now)
                    tottobid = tottobid + 1

            id_delete = IDs_balance(tobject, tottobid)
            for idnow in id_delete:
                map_now.delete_object_s(id_to_tobject[idnow])
                    
    if isdelete:
        for tobject in dtobject:
            map_now.delete_object_s(tobject)

    map_now.write_file(output_path)

if __name__ == "__main__":
    auto_func()        
