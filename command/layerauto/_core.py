import os
import sys
import argparse
current_file_path = os.path.abspath(__file__)
current_dir_path = os.path.dirname(current_file_path)
command_dir_path = os.path.dirname(current_dir_path)
package_dir = os.path.dirname(command_dir_path)

sys.path.append(package_dir)

from copy import deepcopy
import numpy as np
from typing import Callable
import colorsys

import rwmap as rw
from command._util import *

DEFAULT_OBMAPTYPE = rw.const._LAYERAUTO.left_top

def objectre_to_layer__to__obg_re_to_int_dict(config_dict:dict)->dict[str, dict[str, int]]:
    config_dict_temp = deepcopy(config_dict)
    for obg, obg_re_list in config_dict_temp.items():
        for obg_re_dict in obg_re_list:
            if obg_re_dict.get(rw.const._LAYERAUTO.map_type) == None:
                obg_re_dict[rw.const._LAYERAUTO.map_type] = DEFAULT_OBMAPTYPE
    return config_dict_temp

def json_to_LAOBG_TILE_one(tileplace, simplify_dict:dict)->rw.const.LAOBG_TILE:
    if isinstance(tileplace, dict):
        for k, v in tileplace.items():
            kl = simplify_dict.get(k)
            kl = k if kl == None else kl
            if isinstance(v, list):
                if isinstance(v[0], list):
                    return rw.frame.TagRectangle.init_ae(kl, 
                            rw.frame.Coordinate(v[0][0], v[0][1]), 
                            rw.frame.Coordinate(v[1][0], v[1][1]))
                else:
                    return rw.frame.TagCoordinate.init_xy(kl, v[0], v[1])
            else:
                return tuple(kl, v)
    else:
        return tileplace

def json_to_LAOBG_TILE(tileplace, simplify_dict:dict)->rw.const.LAOBG_TILE:
    if isinstance(tileplace, list):
        return [json_to_LAOBG_TILE_one(tileplace_one, simplify_dict) for tileplace_one in tileplace]
    else:
        return json_to_LAOBG_TILE_one(tileplace, simplify_dict)

def layer_to_exe__to__tileplace_to_exe_one(config_list:list, simplify_dict:dict)->list[dict[str, rw.const.LAOBG_TILE], int]:
    gid = config_list[1]
    t_dict_l = {}
    for k, v in config_list[0].items():
        t_dict_l[k] = json_to_LAOBG_TILE(v, simplify_dict)
    return [t_dict_l, gid]

def layer_to_exe__to__tileplace_to_exe(config_list:list, simplify_dict:dict)->list[list[dict[str, rw.const.LAOBG_TILE], int]]:
    tileplace_to_exe = [layer_to_exe__to__tileplace_to_exe_one(config_one, simplify_dict) for config_one in config_list]
    return tileplace_to_exe
    
def list_to_strtagcoo(li:list[str, str, int, int], simplify_dict:dict)->list[str, rw.frame.TagCoordinate]:
    li0 = li[0] if simplify_dict.get(li[0]) == None else simplify_dict[li[0]]
    li1 = li[1] if simplify_dict.get(li[1]) == None else simplify_dict[li[1]]
    return [li0, rw.frame.TagCoordinate.init_xy(li1, li[2], li[3])]

def exe_to_layer__to__exe_to_tileplace(config_dict:dict[str, list[list[str, str, int, int]]], simplify_dict:dict)->dict[int, list[list[str, rw.frame.TagCoordinate]]]:
    return {int(k):[list_to_strtagcoo(vi, simplify_dict) for vi in v] for k, v in config_dict.items()}

def exe__to__exetype_and_exe_to_exe(config_dict:dict)->tuple[str, dict[int, list[list[int]]]]:
    exe_mode = config_dict["exe_type"]
    exe_operation = config_dict["exe_operation"]
    exe_operation = {int(k):v for k, v in exe_operation.items()}
    return (exe_mode, exe_operation)

def get_config_layerauto(config_dict:dict)->tuple:
    if config_dict['rwmapauto_type'] != 'layerauto':
        return ()
    simplify_dict = config_dict['simplify'] if config_dict.get('simplify') != None else {}
    objectre_to_layer_dict = config_dict['objectre_to_layer'] if config_dict.get('objectre_to_layer') != None else {}
    exe_list = config_dict['exe']
    tileplace_to_exe_list = []
    exe_mode_list = []
    exe_to_exe_list = []
    exe_to_tileplace_list = []
    exe_name_list = []
    for exe in exe_list:
        tileplace_to_exe_list.append(layer_to_exe__to__tileplace_to_exe(exe["layer_to_exe"], simplify_dict))
        exetype, exe_to_exe = exe__to__exetype_and_exe_to_exe(exe["exe"])
        exe_mode_list.append(exetype)
        exe_to_exe_list.append(exe_to_exe)
        exe_to_tileplace = exe_to_layer__to__exe_to_tileplace(exe["exe_to_layer"], simplify_dict)
        exe_to_tileplace_list.append(exe_to_tileplace)
        exe_name = exe["exe_name"]
        exe_name_list.append(exe_name)
    return (exe_name_list, tileplace_to_exe_list, 
            exe_to_tileplace_list, 
            objectre_to_layer_dict, exe_to_exe_list, 
            exe_mode_list)

def auto_func():
    parser = argparse.ArgumentParser(
        description='Resize of rwmap.\n' + \
                    '地图放大。')
    
    parser.add_argument('map_path', action = "store", metavar = 'file', type=str, 
                        help='The input path of RW map file.\n' + \
                            '铁锈地图文件的输入路径。')
    
    parser.add_argument("-o", "--output", 
                        action = "store", metavar = "file", type = str, nargs = "?", 
                        required = False, default = "|", 
                        const = "|", 
                        help = "The output path of RW map file.|input path\n" + \
                               "铁锈地图文件的输出路径。"
                        )

    parser.add_argument("-y", "--isyes", 
                        action = 'store_true', help = 'Requests are always y.\n' + \
                            "所有输入请求默认为y，继续执行。")
    
    parser.add_argument("-v", "--verbose", 
                        action = 'store_true', help = 'Detailed output of the prompt message.\n' + \
                            "提供运行信息。")

    parser.add_argument("--debug", 
                        action = 'store_true', help = 'Mode of debuging.\n' + \
                            "进入python debug模式。")

    parser.add_argument("--ignorewarning", 
                        action = 'store_true', help = 'Warning would not exit.\n' + \
                            "警告将不会退出。")
    
    parser.add_argument("--language", 
                        action = "store", metavar = "language", type = str, nargs = "?", 
                        required = False, default = "default", 
                        const = "default", 
                        help = "The language of prompt(ch/eg). The language configuration will be stored.(command/config.json)\n" + \
                        "命令行提示的语言(中文(ch),英文(eg))。语言设置将会被存储。(command/config.json)"
                        )

    parser.add_argument('-j', '--config', 
                        action = "store", metavar = "file", type = str, nargs = "?", 
                        required = True, default = '|', const = '|', 
                        help='Setting(.json).\n' + \
                            '设置(.json)')

    args = parser.parse_args()

    input_path = args.map_path

    output_path = args.map_path if args.output == "|" else args.output

    isyes = args.isyes

    isverbose = args.verbose

    language = args.language

    isdebug = args.debug

    ignorewarning = args.ignorewarning

    config_path = args.config

    language = input_language(isdebug, language)

    standard_out_underline(language, isverbose, "Initialization|初始化")
    standard_out(language, isverbose, "Map data is being imported...|地图数据载入...")
    check_input_output_path(isdebug, language, isyes, input_path, output_path)
    map_now = get_rwmap(isdebug, language, input_path)

    standard_out_underline(language, isverbose, "Automatic processing of RWmap|地层自动处理")

    config_dict = get_config_dict(config_path)
    exe_name_list, tileplace_to_exe_list, \
            exe_to_tileplace_list, \
            objectre_to_layer_dict, exe_to_exe_list, \
            exe_mode_list = get_config_layerauto(config_dict)
    
    new_map_now = map_now.layerobjectgroup_map_auto(exe_name_list, tileplace_to_exe_list, 
            exe_to_tileplace_list, 
            objectre_to_layer_dict, exe_to_exe_list, 
            exe_mode_list, isaddlayer_obg_exe = isdebug)
    
    standard_out_underline(language, isverbose, "Map outputting|地图输出")
    output_rwmap(isdebug, language, new_map_now, output_path)

if __name__ == "__main__":
    auto_func()        

