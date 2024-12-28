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

import rwmap as rw
from command._util import *

def auto_func():
    parser = argparse.ArgumentParser(
        description='The independence of Tilesets.\n' + \
                    '地块集独立化。')
    
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

    parser.add_argument("-di", "--deleteimagelist", 
                        action = "store", metavar = "list[name]", type = str, nargs = "*", 
                        required = False, default = "|", 
                        help = 'The name of imagelayer which would be deleted.\n' +\
                        "被删除图像层的名称")
    
    parser.add_argument('-i', '--imagelayer', 
                        action = "store", metavar = "name", type = str, nargs = "?", 
                        required = False, default = "|", 
                        help='The name of imagelayer.\n' + \
                            '底图名称。')

    args = parser.parse_args()

    input_path = args.map_path

    output_path = args.map_path if args.output == "|" else args.output

    isyes = args.isyes

    isverbose = args.verbose

    language = args.language

    isdebug = args.debug

    ignorewarning = args.ignorewarning

    deleteimagelist = args.deleteimagelist if args.deleteimagelist != '|' else []

    language = input_language(isdebug, language)

    standard_out_underline(language, isverbose, "Initialization|初始化")

    standard_out(language, isverbose, "Map data is being imported...|地图数据载入...")

    check_input_output_path(isdebug, language, isyes, input_path, output_path)

    map_now = get_rwmap(isdebug, language, input_path)

    standard_out_underline(language, isverbose, "Tilesets independence|地块集独立化")

    map_now.tileset_dependent()
    for imagelayer_name in deleteimagelist:
        map_now.delete_imageLayer(imagelayer_name)

    standard_out_underline(language, isverbose, "Map outputting|地图输出")

    output_rwmap(isdebug, language, map_now, output_path, ischangemappath = False, 
                 isdeletetsxsource = True, isdeleteimgsource = False)

if __name__ == "__main__":
    auto_func()        

