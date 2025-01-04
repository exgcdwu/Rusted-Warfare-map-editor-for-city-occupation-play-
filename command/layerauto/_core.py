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

def json_to_LAOBG_TILE_one(isdebug:bool, language:str, configpre_list:list, tileplace, simplify_dict:dict, ts_name_set:set, ts_name_size_dict:dict)->rw.const.LAOBG_TILE:
    if isinstance(tileplace, dict):
        
        for k, v in tileplace.items():
            kl = config_get_ex(isdebug, language, None, configpre_list, k, config_code = 1, error_id = 98, 
                               itype = str, value_set = ts_name_set, 
                               simplify = simplify_dict)
            vl = config_get_ex(isdebug, language, tileplace, configpre_list, k, config_code = 2, error_id = 102, 
                               itype = (int, list), islist_add = True,  
                               len_max = 2, int_min = 0)
            if isinstance(v, list):
                v0 = config_get_ex(isdebug, language, v, configpre_list, 0, config_code = 3, error_id = 106, 
                                   itype = (int, list), islist_add = True, islist = True, 
                                   int_min = 0, len_max = 2)
                sz = ts_name_size_dict[kl]
                if isinstance(v0, list):
                    v00 = config_get_ex(isdebug, language, v0, configpre_list, 0, config_code = 4, error_id = 116, 
                                   itype = int, islist = True, 
                                   int_min = 0)
                    v01 = config_get_ex(isdebug, language, v0, configpre_list, 1, config_code = 5, error_id = 119, 
                                   itype = int, islist = True, 
                                   int_min = 0)
                    coointileset_ex(isdebug, language, kl, (v00, v01), sz, configpre_list, config_code = 6, error_id = 122)

                configpre_list.pop()

                v1 = config_get_ex(isdebug, language, v, configpre_list, 1, config_code = 7, error_id = 112, 
                                   itype = (int, list), islist_add = True, islist = True, 
                                   int_min = 0, len_max = 2)
                
                if isinstance(v1, list):
                    v10 = config_get_ex(isdebug, language, v1, configpre_list, 0, config_code = 8, error_id = 123, 
                                   itype = int, islist = True, 
                                   int_min = 0)
                    v11 = config_get_ex(isdebug, language, v1, configpre_list, 1, config_code = 9, error_id = 126, 
                                   itype = int, islist = True, 
                                   int_min = 0)
                    coointileset_ex(isdebug, language, kl, (v10, v11), sz, configpre_list, config_code = 10, error_id = 129)
                    
                configpre_list.pop()
                
                if isinstance(v0, list) ^ isinstance(v1, list):
                    standard_error(isdebug, language, f"Tileset tile unrecognized, Coordinate/Rectangle?(({v0, v1}), path:{configpre_list})" + \
                                f"|地块集地块识别错误，是坐标还是矩形?(({v1}, {v0}), 路径:{configpre_list})", error_id = 156)
                    

                if isinstance(v0, list):
                    tp = rw.frame.TagRectangle.init_ae(kl, 
                            rw.frame.Coordinate(v00, v01), 
                            rw.frame.Coordinate(v10, v11))
                else:
                    tp = rw.frame.TagCoordinate.init_xy(kl, v0, v1)
            else:
                tileidintileset_ex(isdebug, language, kl, v, sz, configpre_list, config_code = 49, error_id = 157)
                    
                tp = tuple(kl, v)
            configpre_list.pop()
    else:
        config_get_ex(isdebug, language, None, configpre_list, tileplace, config_code = 11, error_id = 86, int_min = 0)
        tp = tileplace
    return tp

def json_to_LAOBG_TILE(isdebug:bool, language:str, configpre_list:list, tileplace, simplify_dict:dict, ts_name_set:set, ts_name_size_dict:dict)->rw.const.LAOBG_TILE:
    if isinstance(tileplace, list):
        tileplace_t_list = []
        for i, tileplace_one in enumerate(tileplace):
            tpt = config_get_ex(isdebug, language, tileplace, configpre_list, i, config_code = 12, error_id = 96, itype = (int, dict), islist_add = True, islist = True)
            tileplace_t_list.append(json_to_LAOBG_TILE_one(isdebug, language, configpre_list, tileplace_one, simplify_dict, ts_name_set, ts_name_size_dict))
            configpre_list.pop()
        return tileplace_t_list
    else:
        return json_to_LAOBG_TILE_one(isdebug, language, configpre_list, tileplace, simplify_dict, ts_name_set, ts_name_size_dict)

def layer_to_exe__to__tileplace_to_exe_one(isdebug:bool, language:str, configpre_list:list, config_list:list, simplify_dict:dict, layer_name_set:set, ts_name_set:set, ts_name_size_dict:dict)->list[dict[str, rw.const.LAOBG_TILE], int]:
    gid = config_get_ex(isdebug, language, config_list, configpre_list, 1, config_code = 13, error_id = 75, itype = int, islist = True, int_min = 0)
    tl = config_get_ex(isdebug, language, config_list, configpre_list, 0, config_code = 14, error_id = 78, itype = dict, islist = True, islist_add = True)
    t_dict_l = {}
    for k, v in tl.items():
        kl = config_get_ex(isdebug, language, None, configpre_list, k, config_code = 15, error_id = 80, itype = str, value_set = layer_name_set, simplify = simplify_dict)
        v = config_get_ex(isdebug, language, tl, configpre_list, k, config_code = 16, error_id = 84, itype = (int, dict, list), islist_add = True)
        t_dict_l[kl] = json_to_LAOBG_TILE(isdebug, language, configpre_list, v, simplify_dict, ts_name_set, ts_name_size_dict)
        configpre_list.pop()
    configpre_list.pop()

    return [t_dict_l, gid]

def layer_to_exe__to__tileplace_to_exe(isdebug:bool, language:str, configpre_list:list, config_list:list, simplify_dict:dict, layer_name_set:set, ts_name_set:set, ts_name_size_dict:dict)->list[list[dict[str, rw.const.LAOBG_TILE], int]]:
    tileplace_to_exe = []
    for i, config_one in enumerate(config_list):
        conf = config_get_ex(isdebug, language, config_list, configpre_list, i, config_code = 17, error_id = 72, itype = list, islist_add = True, islist = True, len_max = 2)
        temp = layer_to_exe__to__tileplace_to_exe_one(isdebug, language, configpre_list, config_one, simplify_dict, layer_name_set, ts_name_set, ts_name_size_dict)
        configpre_list.pop()
        tileplace_to_exe.append(temp)
    return tileplace_to_exe
    


def list_to_strtagcoo(isdebug:bool, language:str, configpre_list:list, li:list[str, str, int, int], simplify_dict:dict, lobe_name_set:set, ts_name_set:set, ts_name_size_dict:dict)->list[str, rw.frame.TagCoordinate]:
    li0 = config_get_ex(isdebug, language, li, configpre_list, 0, config_code = 18, error_id = 138, itype = str, value_set = lobe_name_set, 
                        simplify = simplify_dict, islist = True)
    li1 = config_get_ex(isdebug, language, li, configpre_list, 1, config_code = 19, error_id = 143, itype = str, value_set = ts_name_set, 
                        simplify = simplify_dict, islist = True)
    li2 = config_get_ex(isdebug, language, li, configpre_list, 2, config_code = 20, error_id = 148, itype = int, islist = True, int_min = 0)
    li3 = config_get_ex(isdebug, language, li, configpre_list, 3, config_code = 21, error_id = 152, itype = int, islist = True, int_min = 0)
    sz = ts_name_size_dict[li1]
    coointileset_ex(isdebug, language, li1, (li2, li3), sz, configpre_list, config_code = 22, error_id = 155)
    return [li0, rw.frame.TagCoordinate.init_xy(li1, li2, li3)]

def exe_to_layer__to__exe_to_tileplace(isdebug:bool, language:str, configpre_list:list, config_dict:dict[str, list[list[str, str, int, int]]], simplify_dict:dict, lobe_name_set:set, ts_name_set:set, ts_name_size_dict:dict)->dict[int, list[list[str, rw.frame.TagCoordinate]]]:
    exe_to_tileplace_now = {}
    for k, v in config_dict.items():
        is_int_min_integer_ex(isdebug, language, k, 0, configpre_list, config_code = 23, error_id = 132)
        config_get_ex(isdebug, language, config_dict, configpre_list, k, config_code = 24, error_id = 133, itype = list, 
                      islist_add = True)
        ls_now = []
        for i, vi in enumerate(v):
            config_get_ex(isdebug, language, v, configpre_list, i, config_code = 25, error_id = 135, itype = list, 
                            islist_add = True, len_max = 4, islist = True)
            ls_now.append(list_to_strtagcoo(isdebug, language, configpre_list, vi, simplify_dict, lobe_name_set, ts_name_set, ts_name_size_dict))
            configpre_list.pop()

        configpre_list.pop()
        exe_to_tileplace_now[int(k)] = ls_now
    
    return exe_to_tileplace_now

def ma33_split(ma:list, ov2:list):
    v1 = []
    v2 = deepcopy(ov2)
    for i, ma1 in enumerate(ma):
        v1.append([])
        for j, ma2 in enumerate(ma1):
            if isinstance(ma2, list):
                v1[i].append(ma2[0])
                v2[i][j] = ma2[1]
            else:
                v1[i].append(ma2)
    return v1, v2

def ma33_new(sz:tuple, va):
    ma = []
    for i in range(sz[0]):
        ma.append([])
        for j in range(sz[1]):
            ma[i].append(va)
    return ma

def ma33_assign(ma:list, va):
    for i in range(len(ma)):
        for j in range(len(ma[i])):
            ma[i][j] = va

def exe__to__exetype_and_exe_to_exe(isdebug:bool, language:str, configpre_list:list, config_dict:dict)->tuple[str, dict[int, list[list[int]]]]:
    exe_mode = config_get_ex(isdebug, language, config_dict, configpre_list, "exe_type", config_code = 60, error_id = 88, itype = str, value_set = {"expansion", "terrain", "random"})
    
    exe_border = config_get_ex(isdebug, language, config_dict, configpre_list, "exe_border", config_code = 61, error_id = 160, itype = dict, islist_add = True, default = {})
    
    exe_border_all = config_get_ex(isdebug, language, exe_border, configpre_list, "all", config_code = 62, error_id = 161, itype = int, int_min = -3, default = -3)

    configpre_list.pop()

    exe_operation = config_get_ex(isdebug, language, config_dict, configpre_list, "exe_operation", config_code = 63, error_id = 163, itype = dict, islist_add = True)
    exe_operation_now = {}
    for k, v in exe_operation.items():
        is_int_min_integer_ex(isdebug, language, k, 1, configpre_list, config_code = 64, error_id = 91)
        configpre_list.append(k)
        if exe_mode in {"expansion"}:
            ismatrix_ex(isdebug, language, configpre_list, v, (3, 3), int, config_code = 65, int_min = -1, error_id = 92)
            vl = v
        elif exe_mode in {"terrain"}:
            ismatrix_ex(isdebug, language, configpre_list, v, (3, 3), int, config_code = 66, int_min = [-1, -2], error_id = 165, islist = True, list_lenmin = 1, list_lenmax = 2)
            
            ov2 = ma33_new((3, 3), -2)
            if exe_border_all != -3:
                ma33_assign(ov2, exe_border_all)
            v1, v2 = ma33_split(v, ov2)
            vl = [v1, v2]

        elif exe_mode in {"random"}:
            config_get_ex(isdebug, language, exe_operation, configpre_list, k, config_code = 67, error_id = 166, 
                          itype = dict, islist_add = True)
            for ki in v.keys():
                is_int_min_integer_ex(isdebug, language, ki, 0, configpre_list, config_code = 68, error_id = 168)
                config_get_ex(isdebug, language, v, configpre_list, ki, config_code = 71, error_id = 169, 
                              itype = float, int_min = 0, int_max = 1)
            vl = v
            configpre_list.pop()
        exe_operation_now[int(k)] = vl
        configpre_list.pop()
    configpre_list.pop()

    return (exe_mode, exe_operation_now)

def get_config_layerauto(language:str, isdebug:bool, config_dict:dict, rwmap:rw.RWmap, config_path:str)->tuple:
    
    config_list = [config_path]
    rwmapauto_type = config_get_ex(isdebug, language, config_dict, config_list, "rwmapauto_type", config_code = 30, error_id = 38, itype = str, value_set = {"layerauto"}, default = "layerauto")
    simplify_dict = config_get_ex(isdebug, language, config_dict, config_list, "simplify", config_code = 31, error_id = 40, itype = dict, islist_add = True, default = {})
    for k, v in simplify_dict.items():
        isaddc = True
        v_now = config_get_ex(isdebug, language, simplify_dict, config_list, k, config_code = 32, error_id = 41, itype = (str, list), len_max = 2)
        if isinstance(v_now, list):
            v1 = config_get_ex(isdebug, language, v_now, config_list, 1, config_code = 33, error_id = 44, itype = str, value_set = {"re", "norm"}, islist = True)
            v0 = config_get_ex(isdebug, language, v_now, config_list, 0, config_code = 34, error_id = 47, itype = str, islist = True)
            if v1 == "re":
                isaddc = False
        else:
            v0 = v_now
        if isaddc:
            v0 = f"^{re.escape(v0)}$"
        
        simplify_dict[k] = v0
    config_list.pop()

    objectre_to_layer_dict_pre = config_get_ex(isdebug, language, config_dict, config_list, "objectre_to_layer", 
                                               config_code = 35, error_id = 49, itype = dict, islist_add = True, default = {})
    ob_name_set = set(rwmap.get_objectgroup_name())
    ts_name_set = set(rwmap.get_tileset_name())
    ts_name_size_dict = {}
    for ts_name in ts_name_set:
        tsn = rwmap.get_tileset_s(ts_name).size()
        ts_name_size_dict[ts_name] = (tsn.x(), tsn.y())
    lobe_set = set()
    objectre_to_layer_dict = {}
    for k, v in objectre_to_layer_dict_pre.items():
        
        kl = config_get_ex(isdebug, language, None, config_list, k, config_code = 36, error_id = 50, itype = str, value_set = ob_name_set, simplify = simplify_dict)
        vl = config_get_ex(isdebug, language, objectre_to_layer_dict_pre, config_list, k, config_code = 37, error_id = 54, itype = list, islist_add = True)
        for i, av in enumerate(v):
            avl = config_get_ex(isdebug, language, v, config_list, i, config_code = 38, error_id = 56, itype = dict, islist_add = True, islist = True, len_max = 3)
            pre = config_get_ex(isdebug, language, av, config_list, "re", config_code = 39, error_id = 59, itype = str)
            isvalid_re_ex(isdebug, language, pre, config_list + ["re"], config_code = 40, error_id = 61)
            mre = config_get_ex(isdebug, language, av, config_list, "map_type", config_code = 41, error_id = 62, 
                                itype = str, value_set = {"middle", "left-top"}, default = "left-top")
            avl["map_type"] = mre
            gid = config_get_ex(isdebug, language, av, config_list, "gid", config_code = 42, error_id = 64, itype = int, int_min = 1)
            vl[i] = avl
            config_list.pop()
        config_list.pop()
        lobe_set.add(kl)
        objectre_to_layer_dict[kl] = vl
    config_list.pop()
    lobe_set.update(set(rwmap.get_layer_name()))

    exe_list = config_get_ex(isdebug, language, config_dict, config_list, "execution", config_code = 43, error_id = 67, itype = list, islist_add = True, default = [])
    tileplace_to_exe_list = []
    exe_mode_list = []
    exe_to_exe_list = []
    exe_to_tileplace_list = []
    exe_name_list = []
    for i, exe in enumerate(exe_list):

        exe_p = config_get_ex(isdebug, language, exe_list, config_list, i, config_code = 44, error_id = 68, itype = dict, islist = True)

        exe_name = config_get_ex(isdebug, language, exe, config_list, "exe_name", config_code = 48, error_id = 94, itype = str)

        config_list.append(exe_name)

        layer_to_exe = config_get_ex(isdebug, language, exe, config_list, "layer_to_exe", config_code = 45, error_id = 70, itype = list, islist_add = True)

        temp = layer_to_exe__to__tileplace_to_exe(isdebug, language, config_list, layer_to_exe, simplify_dict, lobe_set, ts_name_set, ts_name_size_dict)
        tileplace_to_exe_list.append(temp)
        config_list.pop()

        exe_n_list = config_get_ex(isdebug, language, exe, config_list, "exe", config_code = 69, error_id = 87, itype = list, islist_add = True, default = [])

        exetype = []
        exe_to_exe = []

        for i, exe_n in enumerate(exe_n_list):
            exe_nl = config_get_ex(isdebug, language, exe_n_list, config_list, i, config_code = 70, error_id = 158, itype = dict, islist_add = True, islist = True)
            exetype_e, exe_to_exe_e = exe__to__exetype_and_exe_to_exe(isdebug, language, config_list, exe_n)
            exetype.append(exetype_e)
            exe_to_exe.append(exe_to_exe_e)
            config_list.pop()

        exe_mode_list.append(exetype)
        exe_to_exe_list.append(exe_to_exe)
        config_list.pop()

        exe_to_layer = config_get_ex(isdebug, language, exe, config_list, "exe_to_layer", config_code = 47, error_id = 93, itype = dict, islist_add = True, default = {})

        exe_to_tileplace = exe_to_layer__to__exe_to_tileplace(isdebug, language, config_list, exe_to_layer, simplify_dict, lobe_set, ts_name_set, ts_name_size_dict)
        exe_to_tileplace_list.append(exe_to_tileplace)
        config_list.pop()

        lobe_set.add(exe_name)
        exe_name_list.append(exe_name)
        config_list.pop()

    config_list.pop()

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
    
    parser.add_argument("-v", "--verbose", type = int, default = 0, const = 1, nargs = "?", action = "store", 
                        required = False, 
                        help = 'Detailed output of the prompt message(0:none, 1:main, 2:detail).\n' + \
                            "提供运行信息(0:无, 1:主要部分, 2:细节)。")

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
                        action = "store", metavar = "file", type = str, nargs = "+", 
                        required = True, 
                        help='List of Setting(.json).\n' + \
                            '设置文件路径列表(.json)')

    args = parser.parse_args()

    input_path = args.map_path

    output_path = args.map_path if args.output == "|" else args.output

    isyes = args.isyes

    isverbose = args.verbose

    language = args.language

    isdebug = args.debug

    ignorewarning = args.ignorewarning

    config_path_list = args.config

    language = input_language(isdebug, language)

    standard_out_underline(language, isverbose, "Initialization|初始化")
    check_input_output_path(isdebug, language, isyes, input_path, output_path)
    map_now = get_rwmap(isdebug, language, isverbose, input_path)

    standard_out_underline(language, isverbose, "Automatic processing of RWmap layer|图层自动处理")

    new_map_now = deepcopy(map_now)

    for i, config_path in enumerate(config_path_list):
        standard_out(language, isverbose, f"Cycle {i + 1}, config: {config_path} running..." + \
                     f"|第 {i + 1} 次图层处理, 图层自动化设置: {config_path} 处理中...")
        standard_out(language, isverbose, f"  config: {config_path} loading..." + \
                     f"|  图层自动化设置: {config_path} 载入中...")
        
        config_dict = get_config_dict(config_path)
        exe_name_list, tileplace_to_exe_list, \
                exe_to_tileplace_list, \
                objectre_to_layer_dict, exe_to_exe_list, \
                exe_mode_list = get_config_layerauto(language, isdebug, config_dict, new_map_now, config_path)
        
        standard_out(language, isverbose, f"  config: {config_path} running..." + \
                     f"|  图层自动化: {config_path} 运行中...")
        
        new_map_now = new_map_now.layerobjectgroup_map_auto(exe_name_list, tileplace_to_exe_list, 
                exe_to_tileplace_list, 
                objectre_to_layer_dict, exe_to_exe_list, 
                exe_mode_list, isaddlayer_obg_exe = isdebug, language = language, 
                isverbose = (isverbose == 2), bl = 4)
    
    standard_out_underline(language, isverbose, "Map outputting|地图输出")
    output_rwmap(isdebug, language, isverbose, new_map_now, output_path)

if __name__ == "__main__":
    auto_func()        

