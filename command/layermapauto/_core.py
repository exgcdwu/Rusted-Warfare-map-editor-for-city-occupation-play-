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

import rwmap as rw
from command._util import *

fitcompare_dict = {
    "func_fit_compare_ave": rw.utility.func_fit_compare_ave
}

def layer_check(map_now:rw.RWmap, layer_name:str, language:str, isyes:bool):
    if map_now.get_layer_s(layer_name) != None:
        question(language, True, "The layer already exists, is it overwritten?" + \
                "|图层已经存在，是否覆盖？", ["y", "n"], ["n"], {}, isyes, "y")
    else:
        map_now.add_layer(layer_name)

def fitcompare_check(fitcompare:Callable, isdebug:bool, language:str):
    if fitcompare_dict.get(fitcompare) == None:
        standard_error(isdebug, language, f"The function's name of fitcompare is wrong.(name:{fitcompare})" + 
                           f"|图像比对函数名称错误。(名称:{fitcompare})", 34)

def auto_func():
    parser = argparse.ArgumentParser(
        description='Auto generation of layer.\n' + \
                    '图块层自动部署。')
    
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

    parser.add_argument('-i', '--imagelayer', 
                        action = "store", metavar = "name", type = str, nargs = "?", 
                        required = False, default = "|", 
                        help='The name of imagelayer.\n' + \
                            '底图名称。')

    parser.add_argument('-l', '--layer', 
                        action = "store", metavar = "name", type = str, nargs = "?", 
                        required = False, default = "Ground", const = "Ground", 
                        help='The name of layer.\n' + \
                            '地层名称。')
    
    parser.add_argument('-c', '--fitcompare', 
                        action = "store", metavar = "name", type = str, nargs = "?", 
                        required = False, default = "func_fit_compare_ave", const = "func_fit_compare_ave", 
                        help='The function of image comparison.\n' + \
                            '图片对比函数。')

    parser.add_argument('-w', '--whitelist', 
                        action = "store", metavar = "name", type = str, nargs = "+", 
                        required = True, 
                        help='White list of tileset.\n' + \
                            '地块集名称白名单')

    args = parser.parse_args()

    input_path = args.map_path

    output_path = args.map_path if args.output == "|" else args.output

    isyes = args.isyes

    isverbose = args.verbose

    language = args.language

    isdebug = args.debug

    ignorewarning = args.ignorewarning

    imagelayer_name = args.imagelayer

    layer_name = args.layer

    fitcompare = args.fitcompare

    white_list = args.whitelist

    language = input_language(isdebug, language)

    standard_out_underline(language, isverbose, "Initialization|初始化")
    standard_out(language, isverbose, "Map data is being imported...|地图数据载入...")
    check_input_output_path(isdebug, language, isyes, input_path, output_path)
    map_now = get_rwmap(isdebug, language, input_path)

    standard_out_underline(language, isverbose, "Automatic processing of layer|图块层自动计算")
    layer_check(map_now, layer_name, language, isyes)
    imagelayer_check(map_now, imagelayer_name, isdebug, language)
    fitcompare_check(fitcompare, isdebug, language)

    tileSet_whiteSet = set(white_list)

    auto_debug = True
    if auto_debug:
        map_now.addTile_auto_quick(layer_name, imagelayer_name, isverbose = isverbose, isdebug = isdebug, tileSet_whiteSet = tileSet_whiteSet)
    try:
        if not auto_debug:
            map_now.addTile_auto_quick(layer_name, imagelayer_name, isverbose = isverbose, isdebug = isdebug, tileSet_whiteSet = tileSet_whiteSet)
    except:
        standard_error(isdebug, language, "Failure of tile auto.|图块自动化失败。", 35)
    map_now.layer_s_ahead(layer_name)

    standard_out_underline(language, isverbose, "Map outputting|地图输出")
    output_rwmap(isdebug, language, map_now, output_path)

if __name__ == "__main__":
    auto_func()        

