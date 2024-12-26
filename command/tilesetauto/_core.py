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


def auto_func():
    parser = argparse.ArgumentParser(
        description='Auto generation of tileset.\n' + \
                    '地块集自动部署。')
    
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

    parser.add_argument('-ct', '--colortileset', 
                        action = "store", metavar = "name", type = str, nargs = "?", 
                        required = False, default = '|', const = '|', 
                        help='The name of color tileset.(-c)\n' + \
                            '提供纯色地块集名称。(-c)')
    
    parser.add_argument('-c', '--color', 
                        action = "store", metavar = "RGB color", type = str, nargs = "+", 
                        required = False, default = "|",
                        help='The color of tileset.\n' + \
                            '纯色颜色。')
    
    parser.add_argument('--name', '--colorname', 
                        action = "store", metavar = "name", type = str, nargs = "+", 
                        required = False, default = "|",
                        help='The name of color.\n' + \
                            '纯色名称。')
    
    parser.add_argument('-cr', '--colorterrain', 
                        action = "store", metavar = "list[int]", type = int, nargs = "+", 
                        required = False, 
                        help='The terrain of different color.\n' + \
                            '不同颜色之间存在的地形。')
    
    parser.add_argument('-cw', '--colorwidth', 
                        action = "store", metavar = "int", type = int, nargs = "?", 
                        required = False, default = -1, const = -1, 
                        help='The width of color tileset.\n' + \
                            '纯色地块的宽度')
    
    parser.add_argument('-cp', '--delta_lxc', 
                        action = "store", metavar = "list[float]", type = float, nargs = 3, 
                        required = False, 
                        help='delta l,x,c of the terrain.\n' + \
                            '地形的delta_l, delta_x, delta_c')
    
    parser.add_argument('-kt', '--kmeantileset', 
                        action = "store", metavar = "name", type = str, nargs = "?", 
                        required = False, default = '|', const = '|', 
                        help='The name of k-mean tileset.(-k)\n' + \
                            '提供k-mean地块集名称。(-k)')

    parser.add_argument('-s', '--ktilesetsize', 
                        action = "store", metavar = "Coordinate", type = int, nargs = 2, 
                        required = False, default = [0, 0], 
                        help='The size of tileset made by k-mean algorithm.\n' + \
                            'k-mean算法产生地块大小。')
    
    parser.add_argument('-r', '--randseed', 
                        action = "store", metavar = "number", type = int, nargs = "?", 
                        required = False, default = -1, const = -1, 
                        help='random seed.\n' + \
                            '随机数种子。')

    parser.add_argument('--resizediv', 
                        action = "store", metavar = "number", type = int, nargs = "?", 
                        required = False, default = 0, const = 0, 
                        help='coefficient of image reduction for k-mean algorithm.\n' + \
                            'k-mean图像缩放系数。')
    
    parser.add_argument('-m', '--kmeanstopmovenum', 
                        action = "store", metavar = "number", type = int, nargs = "?", 
                        required = False, default = 0, const = 0, 
                        help='move number of stoping for k-mean algorithm.\n' + \
                            'k-mean算法到停止时最小移动限制。')
    
    parser.add_argument('-cy', '--kmeanlimitcycle', 
                        action = "store", metavar = "number", type = int, nargs = "?", 
                        required = False, default = -1, const = -1, 
                        help='maximum cycle of stoping for k-mean algorithm.\n' + \
                            'k-mean算法到停止时最大轮数。')

    parser.add_argument('-j', '--config', 
                        action = "store", metavar = "file", type = str, nargs = "?", 
                        required = False, default = '|', const = '|', 
                        help='Tile properties setting(.json).\n' + \
                            '地块属性设置(.json)')
    
    parser.add_argument('-n', '--noise', 
                        action = "store", metavar = "list[float]", type = float, nargs = '+', 
                        required = False, 
                        help='Noise of tile(h, s, v).\n' + \
                            '地块噪声(h, s, v)')

    # 

    args = parser.parse_args()

    input_path = args.map_path

    output_path = args.map_path if args.output == "|" else args.output

    isyes = args.isyes

    isverbose = args.verbose

    language = args.language

    isdebug = args.debug

    ignorewarning = args.ignorewarning

    imagelayer_name = args.imagelayer

    tileset_name = args.colortileset

    color_list = args.color if args.color != '|' else []

    name_list = args.name if args.name != '|' else []

    ktileset_name = args.kmeantileset

    ktsize = args.ktilesetsize

    ktsize_coo = rw.frame.Coordinate(ktsize[0], ktsize[1])

    randseed = args.randseed

    kmeanstopmovenum = args.kmeanstopmovenum

    kmeanlimitcycle = args.kmeanlimitcycle

    resizediv = args.resizediv

    resizediv_coo = rw.frame.Coordinate(resizediv, resizediv)

    config = args.config

    colorterrain = args.colorterrain

    colorwidth = args.colorwidth

    delta_lxc = args.delta_lxc

    noise = args.noise

    language = input_language(isdebug, language)
    config_dict = get_config_dict(config)

    standard_out_underline(language, isverbose, "Initialization|初始化")
    standard_out(language, isverbose, "Map data is being imported...|地图数据载入...")
    check_input_output_path(isdebug, language, isyes, input_path, output_path)
    map_now = get_rwmap(isdebug, language, input_path)

    standard_out_underline(language, isverbose, "Automatic processing of tileset|地块集自动计算")

    if tileset_name != '|':

        standard_out(language, isverbose, "Add some pure color tilesets...|从参数加入纯色地块集...")

        color_pair = []
        if colorterrain != None:
            for i in range(len(colorterrain) // 2):
                color_pair.append((colorterrain[2 * i], colorterrain[2 * i + 1]))


        color_list_config = config_dict.get("purecolor-name")

        if color_list_config != None:
            color_list_config1 = [color.split(':')[0] for color in color_list_config]
            color_list_config234 = [color.split(':')[1] for color in color_list_config]
            color_list_config23 = [color.split('|')[0] for color in color_list_config234]
            color_list_config2 = [color.split(',')[0] for color in color_list_config23]
            color_list_config3 = [color.split(',')[1] if len(color.split(',')) == 2 else "0" for color in color_list_config23]
            color_list_config4 = [color.split('|')[1] if len(color.split('|')) == 2 else "0" for color in color_list_config234]
            color_list_config4 = [[float(fl) for fl in color.split(';')] + [0, 0, 0] for color in color_list_config4]
            color_list_config4 = [color[0:3] for color in color_list_config4]
            
            color_list_config = [[rw.utility.blanktoNone(color_list_config1[index]), 
                                  rw.utility.blanktoNone(color_list_config2[index]), 
                                  rw.utility.blanktoNone(color_list_config3[index]), 
                                  color_list_config4[index]] for index in range(len(color_list_config))]
            


        if color_list == [] and color_list_config != None:
            color_list = [color[0] for color in color_list_config]
        color_nparr = hex_list_to_rgb_nparr(color_list, tiy = colorwidth)
        color_list_n = []
        for color_str in color_list:
            color_list_n.append(np.array(hex_to_rgb(color_str), np.uint8))

        if name_list == [] and color_list_config != None:
            name_list = [color[1] for color in color_list_config]

        if color_pair == []:
            color_pair = config_dict.get('purecolor-colorpair')
            color_pair = color_pair if color_pair != None else []

        tileproperties_now = []
        if tileproperties_now == [] and color_list_config != None:
            tileproperties_now = [color[2] for color in color_list_config]


        terrain_index_dict = {}
        if terrain_index_dict == {}:
            terrain_index_dict = config_dict.get("purecolor-ntexist")
            terrain_index_dict = terrain_index_dict if terrain_index_dict != None else {}

        if noise == None:
            if color_list_config != None:
                noise = color_list_config4
        else:
            noise = [noise for i in range(len(color_list_config))]

        if delta_lxc == None:
            delta_lxc = config_dict.get("purecolor-delta-lxc")
        else:
            delta_lxc = [delta_lxc for i in range(len(color_pair))]

        if colorwidth == -1:
            colorwidth_n = config_dict.get("purecolor-colorpair-y")
            if colorwidth_n != None:
                colorwidth = colorwidth_n

        if color_pair == []:
            map_now.add_tileset_purecolor(input_path, color_nparr, [], tileset_name + ".png", tileset_name + ".tsx", noise = noise, randseed = randseed)
        else:
            map_now.add_tileset_purecolor_terrain(input_path, name_list, color_list_n, color_pair, tileproperties_now, delta_lxc, tileset_name + ".png", tileset_name + ".tsx", tiy = colorwidth, noise = noise, randseed = randseed, terrain_index_dict = terrain_index_dict)

    if ktileset_name != '|':
        if config != '|':
            tilepro_func_args_dict = deepcopy(config_dict["kmean-tileproperties"])
        else:
            tilepro_func_args_dict = None

        standard_out(language, isverbose, "Add some pure color tilesets by kmeans...|通过k-mean算法加入纯色地块集...")

        map_now.add_tileset_kmean(ktsize_coo, imagelayer_name, input_path, ktileset_name + ".png", ktileset_name + ".tsx", resize_coo = resizediv_coo, tile_properties_args = tilepro_func_args_dict, 
                                stopnum = kmeanstopmovenum, rand_seed = randseed, limit_cycle = kmeanlimitcycle, isverbose = isverbose, isdebug = isdebug, noise = noise, randseed = randseed)

    standard_out_underline(language, isverbose, "Map outputting|地图输出")
    output_rwmap(isdebug, language, map_now, output_path)

if __name__ == "__main__":
    auto_func()        

