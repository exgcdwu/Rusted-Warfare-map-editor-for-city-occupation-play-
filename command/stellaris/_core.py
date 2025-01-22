import os
import sys
import argparse
import regex as re

from copy import deepcopy
import numpy as np
from typing import Callable
import time
import math
import subprocess
import warnings

current_file_path = os.path.abspath(__file__)
current_ste_path = os.path.dirname(current_file_path)
command_dir_path = os.path.dirname(current_ste_path)
package_dir = os.path.dirname(command_dir_path)

sys.path.append(package_dir)

import rwmap as rw
from command._util import *

current_file_path = os.path.abspath(__file__)
current_ste_path = os.path.dirname(current_file_path)


def auto_func():
    parser = argparse.ArgumentParser(
        description='Auto generation of stellaris map.\n' + \
                    '群星地图自动产生。')
    
    parser.add_argument('map_dir', action = "store", metavar = 'path', type=str, 
                        help='The output path of RW map dir.\n' + \
                            '铁锈地图文件的输出文件夹。')
    
    parser.add_argument("-f", "--output_file", 
                        action = "store", metavar = "file", type = str, nargs = "?", 
                        required = False, default = "|", 
                        const = "|", 
                        help = "The output file name of RW map.\n" + \
                               "铁锈地图文件的输出文件名。"
                        )
    
    parser.add_argument("-s", "--scope", 
                        action = "store", metavar = "int", type = int, nargs = "+", 
                        required = False, 
                        help = "The suffix scope of Stellaris RW map.\n" + \
                               "群星产生地图的后缀范围。"
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

    parser.add_argument('-jv', '--cversion', 
                        action = "store", metavar = "version", type = str, nargs = "?", 
                        required = False, default = '|', const = '|', 
                        help='The version of Stellaris setting(.json).\n' + \
                            '群星属性设置版本(.json)')

    parser.add_argument('-j', '--config', 
                        action = "store", metavar = "file", type = str, nargs = "?", 
                        required = False, default = '|', const = '|', 
                        help='The Stellaris of setting(.json).\n' + \
                            '群星属性设置(.json)')

    parser.add_argument('-r', '--randseed', 
                        action = "store", metavar = "number", type = int, nargs = "?", 
                        required = False, default = -1, const = -1, 
                        help='random seed(default:-1, time as randseed).\n' + \
                            '随机数种子(默认-1 以时间随机)。')


    args = parser.parse_args()

    output_dir = args.map_dir

    output_file = args.output_file

    scope = args.scope

    if len(scope) == 1:
        scope = [scope[0], scope[0]]
    elif len(scope) == 3:
        raise ValueError("dddd")

    isyes = args.isyes

    isverbose = args.verbose

    language = args.language

    ignorewarning = args.ignorewarning

    isdebug = args.debug

    config = args.config

    randseed = args.randseed

    cversion = args.cversion

    language = input_language(isdebug, language)    

    if cversion != "|":

        cversion_d = re.findall(r'[a-zA-Z0-9]+', cversion)
        cversion_d = ''.join(cversion_d)
        avd, bvd, cvd = split_first_letter(cversion_d)
        suf = bvd + cvd
        suf = "" if suf == "" else "_" + suf
        cversion_s = "stellaris_" + avd + suf + ".json"
        ste_dir = "stellaris_v" + avd 
        config = os.path.join(current_ste_path, ste_dir, "json", cversion_s)

    config_dict = get_config_dict_ex(isdebug, language, config)
    config_list = []
    version = config_get_ex(isdebug, language, config_dict, config_list, "version", config_code = 101, 
                                  error_id = 172, itype = str)
    
    version_d = ''.join(re.findall(r'[a-zA-Z0-9]+', version))

    isyes_list = ["-y"] if isyes else []
    isver_list = ["-v", str(isverbose)] if isverbose else []
    isdebug = ["--debug"] if isdebug else []
    igw = ["--ignorewarning"] if ignorewarning else []

    code_path = os.path.join(current_ste_path, "stellaris_v" +  version_d, "_core.py")
    code_list = ["python", code_path, output_dir, "-f", output_file, "-s", str(scope[0]), str(scope[1]), 
                 "--language", language, "-j", config, "-r", str(randseed)] + isyes_list + isver_list + \
                 isdebug + igw

    subprocess.run(code_list)
    
if __name__ == "__main__":
    auto_func()        

