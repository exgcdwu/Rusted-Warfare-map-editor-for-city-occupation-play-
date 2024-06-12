import argparse
import importlib
import os
import sys
current_file_path = os.path.abspath(__file__)
current_dir_path = os.path.dirname(current_file_path)
package_dir = os.path.dirname(current_dir_path)

sys.path.append(package_dir)
import rwmap as rw

from auto._data import *

class AUTOKEY:
    info_args = "info_args"
    prefix = "prefix"
    info = "info"
    args = "args"
    seg = "seg"
    opargs = "opargs"
    opargs_seg = "opargs_seg"
    opargs_prefix_len = "opargs_prefix_len"
    ids = "ids"
    operation = "operation"

    exist = "exist"
    death = "death"
    offset = "offset"
    size = "size"
    name = "name"
    type = "type"
    optional = "optional"

def get_args(info:dict, name:str)->dict:
    args_dict = {}
    split_now = name.split(info[AUTOKEY.opargs_seg])
    opargs = split_now[1:]
    args = split_now[0].split(info[AUTOKEY.seg])[1:]
    for index, thing in enumerate(info[AUTOKEY.args]):
        args_dict[thing[0]] = thing[1](args[index])
    
    prefix_len = info[AUTOKEY.opargs_prefix_len]

    for oparg in opargs:
        prefix_now = oparg[0:prefix_len]
        var_now = oparg[prefix_len:]
        if info[AUTOKEY.opargs].get(prefix_now) != None:
            info_thing = info[AUTOKEY.opargs][prefix_now]
            args_dict[info_thing[0].split("|")[0]] = info_thing[1](var_now)

    for key, info_thing in info[AUTOKEY.opargs].items():
        args_dict[info_thing[0].split("|")[0]] = info_thing[1](info_thing[0].split("|")[1])
    return args_dict

def str_translation(value:str, dict_name:dict)->str:
    if isinstance(value, dict):
        return value
    value_list = value.split("{")
    value_ans = value_list[0]
    for index in range(1, len(value_list)):
        value_list_now = value_list[index].split("}")
        value_list_now[0] = dict_name[value_list_now[0]]
        value_ans = value_ans + "".join(value_list_now)
    return value_ans

def get_tobject(operation:dict, dict_name:dict, ori_pos:rw.frame.Coordinate, ori_size:rw.frame.Coordinate)->rw.case.TObject:
    
    if operation.get(AUTOKEY.exist) != None:
        if dict_name.get(operation[AUTOKEY.exist]) == None or dict_name.get(operation[AUTOKEY.exist]) != True:
            return None
    if operation.get(AUTOKEY.death) != None:
        if dict_name.get(operation[AUTOKEY.death]) != None and dict_name.get(operation[AUTOKEY.death]) == True:
            return None
    
    offset = operation.get(AUTOKEY.offset)
    offset = offset if offset != None else rw.frame.Coordinate()
    size = operation.get(AUTOKEY.size)
    size = size if size != None else ori_size
    pos = ori_pos + offset

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

def auto_func():
    parser = argparse.ArgumentParser(
        description='Objects of Triggers are automatically processed by information\'s mode.')
    parser.add_argument('map_path', action = "store", metavar = 'file', type=str, nargs = 1, 
                        help='The input path of RW map file.')
    parser.add_argument("-i", "--info", dest = "info", 
                        action = "store", metavar = "file", type = str, nargs = 1, 
                        required = False, default = current_dir_path + "\\_data.py", 
                        help = "The file's path which has information's mode variable|current_file_path"
                        )
    parser.add_argument("-v", "--var", dest = "var", 
                        action = "store", metavar = "name", type = str, nargs = 1, 
                        required = False, default = "auto_func_arg", 
                        help = "The variable name of information\'s mode.|auto_func_arg"
                        )
    
    parser.add_argument("-o", "--output", dest = "output_path", 
                        action = "store", metavar = "file", type = str, nargs = 1, 
                        required = False, default = "|", 
                        help = "The output path of RW map file.|input path"
                        )

    args = parser.parse_args()
    map_now = rw.RWmap.init_mapfile(f'{args.map_path[0]}')
    output_path = args.map_path[0] if args.output_path == "|" else args.output_path[0]
    sys.path.append("".join(args.info.split("\\")[:-1]))
    info_file = importlib.import_module(".".join(".".join(args.info.split("\\")[-2:]).split(".")[:-1]))
    info_now = getattr(info_file, args.var, 'Not Found')

    info_dict = {}
    ids_now_dict = {}

    for key, info in info_now.items():
        for tobject in map_now.iterator_object_s(default_re = {rw.const.OBJECTDE.type: r"(?!.+)", 
                                                               rw.const.OBJECTDE.name: r".+"}):
            if key == tobject.returnDefaultProperty(rw.const.OBJECTDE.name):
                info_dict_now = {}
                for key_now, ntype in info[AUTOKEY.info_args].items():
                    info_dict_now[key_now] = ntype(tobject.returnOptionalProperty(key_now))
                info_dict_now[AUTOKEY.prefix] = info_dict_now[info[AUTOKEY.prefix]]
                info_dict_now[AUTOKEY.info] = key
                for thing in info[AUTOKEY.ids]:
                    ids_now_dict[info_dict_now[thing[0]]] = 1
                info_dict[info_dict_now[AUTOKEY.prefix]] = info_dict_now
                map_now.delete_object_s(tobject)


    for tobject in map_now.iterator_object_s(default_re = {rw.const.OBJECTDE.type: r"(?!.+)", 
                                                           rw.const.OBJECTDE.name: r".+"}):
        tobject_name = tobject.returnDefaultProperty(rw.const.OBJECTDE.name)
        ischange = False
        for key, info in info_dict.items():
            prefix_now = info[AUTOKEY.prefix]
            info_key = info[AUTOKEY.info]
            if prefix_now == tobject_name[0:len(prefix_now)]:
                myinfo = info_now[info_key]
                object_dict = get_args(myinfo, tobject_name)
                object_dict.update(info)
                ischange = True
                break
        if ischange:
            operation_id = []
            for thing in myinfo[AUTOKEY.ids]:
                idprefix = object_dict[thing[0]]
                for i in range(thing[1]):
                    id_now = idprefix + str(ids_now_dict[idprefix])
                    object_dict[AUTOKEY.ids + str(i)] = id_now
                    operation_id.append(id_now)
                    ids_now_dict[idprefix] = ids_now_dict[idprefix] + 1
            ori_pos = rw.frame.Coordinate(
                tobject.returnDefaultProperty(rw.const.OBJECTDE.x), 
                tobject.returnDefaultProperty(rw.const.OBJECTDE.y)
            )
            ori_size = rw.frame.Coordinate(
                tobject.returnDefaultProperty(rw.const.OBJECTDE.width), 
                tobject.returnDefaultProperty(rw.const.OBJECTDE.height)
            )
            map_now.delete_object_s(tobject)
            for operation_now in myinfo[AUTOKEY.operation]:
                object_now = get_tobject(operation_now, object_dict, ori_pos, ori_size)
                if object_now != None:
                    map_now.addObject_type(object_now)
    map_now.write_file(output_path)

if __name__ == "__main__":
    auto_func()        
