import os
import sys
import json
import shutil
import xml.etree.ElementTree as et
from pprint import pprint
from copy import deepcopy
import numpy as np
import math
from typing import Union
import regex as re

current_file_path = os.path.abspath(__file__)
current_dir_path = os.path.dirname(current_file_path)
command_dir_path = os.path.dirname(current_dir_path)
package_dir = os.path.dirname(command_dir_path)

sys.path.append(package_dir)

import rwmap as rw

import command._util._json as cjs

TEMPLATE_RE = "(^.*_info.*$)|(^dd?\\..*$)"

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
    ID = "ID"
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
    tobject_id = "tobject_id"
    tobject_name = "tobject_name"
    brace_exp_depth = "brace_exp_depth"
    errorif = "errorif"
    print = "print"
    left_brace = "007B"
    right_brace = "007D"
    objectGroup_name = "objectGroup_name"

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
    info_name = "info_name"

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
    isnot_cite_check = "isnot_cite_check"
    is_cite_white_list = "is_cite_white_list"

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

    # re.finditer

language_seg = '|'
language_dict = {"eg" : 0, "ch" : 1}
language_set = set(language_dict.keys())

FULL_SCREEN = int(shutil.get_terminal_size().columns / 2) * 2
UNDERLINE_EVEN_NUM = int(FULL_SCREEN * 3 / 8) * 2

cite_object_dict = {}

language_dict = {"eg" : 0, "ch" : 1}
language_set = set(language_dict.keys())

def get_language()->str:
    with open(os.path.join(command_dir_path, 'config.json'), 'r') as f:
        config_dict = json.load(f)
        return config_dict['language']

def debug_pdb(isdebug, thing = ""):
    if isdebug: 
        if isinstance(thing, str):
            print(thing)
        else:
            pprint(thing)
        import pdb;pdb.set_trace()

def str_lang(language:str, info_str:str)->str:
    language_index = language_dict[language]
    info_list = info_str.split(language_seg)
    if len(info_list) != len(language_set):
        debug_pdb(True, "standard print error(language).")
    return info_list[language_index]

def standard_out(language:str, ifdo:bool, info_str)->None:
    if ifdo:
        if isinstance(info_str, str):
            print(str_lang(language, info_str))
        else:
            pprint(info_str)

def weighted_char_count(s):
    weight = 0
    for char in s:
        if '\u4e00' <= char <= '\u9fff':  # 检测汉字的Unicode范围
            weight += 2
        else:
            weight += 1
    return weight

def standard_out_underline(language:str, ifdo:bool, info_str:str)->None:
    info_str_now = str_lang(language, info_str)
    lenstr = weighted_char_count(info_str_now)
    if ifdo:
        if lenstr % 2 != 0:
            info_str_now = info_str_now + "-"
            lenstr = lenstr + 1

        left_bk = int(FULL_SCREEN / 2 - UNDERLINE_EVEN_NUM / 2)
        left_ul = int(UNDERLINE_EVEN_NUM / 2 - lenstr / 2)
        right_ul = left_ul

        print(" " * left_bk + "-" * UNDERLINE_EVEN_NUM)
        print(" " * left_bk + "-" * left_ul + info_str_now + "-" * right_ul)
        print(" " * left_bk + "-" * UNDERLINE_EVEN_NUM)

def langstr_add_str(langstr:str, str_now:str):
    return "|".join([langstr + str_now for langstr in langstr.split("|")])

def langstrlist_add(langstr_list:list):
    if langstr_list == []:
        return '|'
    langstr_matrix = [langstr.split("|") for langstr in langstr_list]
    max_lang = max([len(langstr_list) for langstr_list in langstr_matrix])
    langstr_ans = "|".join([''.join([langstr_matrix[i][j] for i in range(len(langstr_matrix)) if j < len(langstr_matrix[i])]) for j in range(max_lang)])
    return langstr_ans

ISAUTO_PRINT = False

def question(language:str, condition:bool, tip:str, chosen_list:list, break_list:set, chosen_dict:dict, isauto = False, auto = None)->bool:
    chosen_set = set(chosen_list)
    break_set = set(break_list)
    chosen = "(" +  "/".join(chosen_list) + ")"
    break_n = "(" +  "/".join(break_list) + ")"
    break_langstr = "Otherwise the program will be terminated.|否则程序终止。"
    tip_now = langstr_add_str(tip, chosen)
    if len(break_list) != 0:
        tip_now = langstrlist_add([tip_now, break_langstr])
        tip_now = langstr_add_str(tip_now, break_n)
    error_langstr = "Identification error, please re-enter.|识别错误，请重新输入。"
    error_langstr = langstr_add_str(error_langstr, chosen)
    if len(break_list) != 0:
        error_langstr = langstrlist_add([error_langstr, break_langstr])
        error_langstr = langstr_add_str(error_langstr, break_n)
    isfirst = True
    while(condition):
        if isauto:
            standard_out(language, ISAUTO_PRINT, tip_now)
            standard_out(language, ISAUTO_PRINT, f"Automatically enter {auto}.|自动输入{auto}。")
            ispathsame = auto
        else:
            if isfirst:
                isfirst = False
                ispathsame = input(str_lang(language, tip_now))
            else:
                ispathsame = input(str_lang(language, error_langstr))
        
        if chosen_set.issuperset([ispathsame]):
            if chosen_dict.get(ispathsame) != None:
                standard_out(language, True, chosen_dict[ispathsame])
            if break_set.issuperset([ispathsame]):
                standard_out(language, True, "Termination of Program.|程序终止。")
                exit(0)
            return ispathsame
        
def input_language(isdebug:bool, language:str)->str:
    if not (language_set.issuperset([language]) or language == "default"):
        print(f"Language is not \"ch\" or \"eg\".({language})\n" + 
              f"语言(--language)不是中文(ch)或者英文(eg)({language})", file=sys.stderr)
        if isdebug:
            import pdb;pdb.set_trace()
        exit(23)

    with open(os.path.join(command_dir_path, 'config.json'), 'r') as f:
        config_dict = json.load(f)
    if language != "default":
        config_dict["language"] = language
    else:
        language = config_dict["language"]
    with open(os.path.join(command_dir_path, 'config.json'), 'w') as f:
        json.dump(config_dict, f)
    
    return deepcopy(language)

def get_config_dict(config:str)->dict:
    if config != '|':
        f = open(config, 'r', encoding = 'utf-8')
        config_dict = json.load(f)
        f.close()
    else:
        config_dict = {}
    return config_dict

def get_config_dict_ex(isdebug:bool, language:str, config:str)->dict:
    try:
        config_n = get_config_dict(config)
    except:
        standard_error(isdebug, language, f"{config} is error." + \
                       f"|{config} 读取失败。", error_id = -2)
    if config_n == {}:
        standard_error(isdebug, language, f"There's no json file." + \
                       f"|没有json文件。", error_id = -3)
    return config_n


def standard_error(isdebug:bool, language:str, info_err, error_id:int, sub_info_error = None)->None:
    print(str_lang(language, info_err) + "(" + str(error_id) + ")", file=sys.stderr)
    if sub_info_error != None:
        pprint(sub_info_error)
    if isdebug:
        import pdb;pdb.set_trace()
    exit(error_id)

def standard_warning(isdebug:bool, ignorewarning:bool, language:str, info_warn, warn_id:int, error_id:int, sub_info_warn:str = None)->None:
    print(str_lang(language, info_warn), file=sys.stdout)
    if sub_info_warn != None:
        pprint(sub_info_warn)
    if isdebug:
        import pdb;pdb.set_trace()
    if not ignorewarning:
        exit(error_id)

def get_rwmap(isdebug:bool, language:str, isverbose:bool, rwpath:str)->rw.RWmap:
    try:
        if isverbose:
            standard_out(language, True, f"RW map input({rwpath})" + 
                f"|地图文件导入({rwpath})")
        map_now = rw.RWmap.init_mapfile(f'{rwpath}')
        return map_now
    except FileNotFoundError:
        standard_error(isdebug, language, "RW map file is not found, please check your input path.|铁锈输入地图文件未找到，请仔细检查地图路径。", 24)
    except et.ParseError:
        standard_error(isdebug, language, "File parsing error, the file may not be XML file. Maybe it's not RW map file.|地图文件解析错误，不符合xml格式。也许导入的不是铁锈地图。", 25)

def output_rwmap(isdebug:bool, language:str, isverbose:bool, rwmap:rw.RWmap, output_path:str, ischangemappath:bool = True, isdeletetsxsource:bool = False, isdeleteimgsource:bool = False)->None:
    try:
        standard_out(language, isverbose, f"RW map output({output_path})" + 
            f"|地图文件导出({output_path})")
        rwmap.write_file(output_path, ischangemappath, isdeletetsxsource, isdeleteimgsource)
    except:
        standard_error(isdebug, language, "Error of map outputting.|地图文件输出错误。", 31)

def try_to_deal_id_coincide(language:str, isyes:bool, map_now:rw.RWmap):
    id_now = 1
    id_mapping = {}
    for objectGroup in map_now._objectGroup_list:
        for tobject in objectGroup._object_list:
            tobject_id = tobject.returnDefaultProperty("id")
            if id_mapping.get(tobject_id) == None:
                id_mapping[tobject_id] = [[tobject, id_now]]
            else:
                id_mapping[tobject_id] = id_mapping[tobject_id] + [[tobject, id_now]]
            id_now = id_now + 1
    map_now.resetnextobjectid(isaboutnextobjectid = False)

    id_coincide_num = 0
    id_coincide_dict = {}
    for objectGroup in map_now._objectGroup_list:
        for tobject in objectGroup._object_list:
            tobject_id = tobject.returnDefaultProperty("id")
            IDs = tobject.returnOptionalProperty(AUTOKEY.IDs)
            IDfa = tobject.returnOptionalProperty(AUTOKEY.IDfa)
            id_temp_list = []
            if IDfa != None:
                id_temp_list.append(IDfa)
            if IDs != None:
                ID_list = IDs.split(",")
                for index, ID_now in enumerate(ID_list):
                    new_ID_list = id_mapping.get(ID_now)
                    if new_ID_list == None:
                        continue
                    elif len(new_ID_list) == 1:
                        continue
                    else:
                        id_temp_list.append(ID_now)
            id_coincide_num = id_coincide_num + len(id_temp_list)    
            if id_temp_list != []:
                    id_coincide_dict[tobject_id] = id_temp_list
    if id_coincide_num == 0:
        standard_out(language, True, f"Some confusing IDs are coincident to zero and do not need to be adjusted." + 
            f"|混淆ID重合为0，无需调整，正常重排ID。")
    else:
        standard_out(language, True, f"Some confusing IDs are being outputing." + 
            f"|混淆ID正在输出。")
        for key, value in id_coincide_dict.items():
            print(f"{key}:{value}")
        question(language, True, f"Some confusing IDs have coincidence, the number:{id_coincide_num}(If the number is too large, it is recommended to fix them manually.). Do you want to correct coincidence?" + 
            f"|混淆ID存在重合，数量为{id_coincide_num}（如果数量很多(比如几百个)，建议外部手动修复）。是否开始解决混淆？", ["y", "n"], ["n"], {}, isyes, "y")


    id_coincide_now = 1
    for objectGroup in map_now._objectGroup_list:
        for tobject in objectGroup._object_list:
            IDs = tobject.returnOptionalProperty(AUTOKEY.IDs)
            IDfa = tobject.returnOptionalProperty(AUTOKEY.IDfa)
            ID_list = []
            if IDfa != None:
                ID_list.append(IDfa)
            if IDs != None:
                ID_list = ID_list + IDs.split(",")
            for index, ID_now in enumerate(ID_list):
                new_ID_list = id_mapping.get(ID_now)
                if new_ID_list == None:
                    ID_list[index] = "999999"
                elif len(new_ID_list) == 1:
                    ID_list[index] = str(new_ID_list[0][1])
                else:
                    
                    chosen_set = [str(num + 1) for num in range(len(new_ID_list))] + ["n"]
                    chosen_dict = dict([[chosen_one, f"{chosen_one}th object has been chosen." + \
                                            f"|第{chosen_one}个宾语已选择。"] for chosen_one in chosen_set])
                    standard_out(language, True, "Tagged Objects|标记宾语:")
                    print(tobject)
                    standard_out(language, True, "objects ID Coincide|ID混淆的宾语:")
                    for index_coi in range(len(new_ID_list)):
                        standard_out(language, True, f"{index_coi + 1}th object|第{index_coi + 1}个混淆宾语:")
                        print(new_ID_list[index_coi][0])
                    chosen_one = question(language, True, 
                                    f"({id_coincide_now}/{id_coincide_num})Please choose which object is generated by this tagged object.(ID:{ID_now})" + \
                                    f"|({id_coincide_now}/{id_coincide_num})尝试选择哪一个宾语是该标记宾语产生的宾语。(ID:{ID_now})", 
                                    chosen_set, ["n"], chosen_dict)
                    ID_list[index] = str(new_ID_list[int(chosen_one) - 1][1])
                    id_coincide_now = id_coincide_now + 1

                ID_l = 0
                if IDfa != None:
                    IDfa_now = ID_list[0]
                    tobject.assignOptionalProperty(AUTOKEY.IDfa, IDfa_now)
                    ID_l = 1
                if IDs != None:
                    IDs_now = ",".join(ID_list[ID_l:])
                    tobject.assignOptionalProperty(AUTOKEY.IDs, IDs_now)

    id_now = 1
    for objectGroup in map_now._objectGroup_list:
        for tobject in objectGroup._object_list:
            tobject.assignDefaultProperty("id", str(id_now))
            id_now = id_now + 1

def get_id_to_tobject(language:str, isverbose:bool, isyes:bool, rwmap:rw.RWmap, input_path:str, output_path:str, isquestion:bool)->dict:
    id_to_tobject_do = True
    debug_do_num = 0
    while(id_to_tobject_do):
        if debug_do_num == 2:
            print("程序出现bug，请联系作者。")
            exit(0)
        id_to_tobject_do = False
        id_to_tobject:dict[int, rw.case.TObject] = {}
        for tobject in rwmap.iterator_object_s(objectGroup_re = '^.*$'):
            tobid = tobject.returnDefaultProperty("id")
            if id_to_tobject.get(tobid) != None:
                id_to_tobject_do = True
                break
            id_to_tobject[tobid] = tobject
        if id_to_tobject_do:
            isobjectgroupauto = False
            for tobject in rwmap.iterator_object_s(objectGroup_re = '^.*$'):
                if tobject.returnOptionalProperty(AUTOKEY.IDs) != None:
                    isobjectgroupauto = True
                    break

            if not isobjectgroupauto:
                if question:
                    question(language, True, "The IDs are coincident and the mapping cannot be performed. And the map has not executed objectgroupauto. Would you want to rearrange ID?" + \
                            "|宾语ID发生重合，ID映射无法进行。且尚未自动化。是否重排ID？", ["y", "n"], ["n"], {}, 
                            isyes, "y")
                standard_out(language, isverbose, "IDs are arranging in the map...|铁锈地图宾语ID重排中...")
                rwmap.resetobjectid()
            else:
                standard_out(language, True, f"The IDs are coincident and the mapping cannot be performed. And the map has executed objectgroupauto. Maybe object ID adjustment is required." + 
                            f"|宾语ID发生重合，ID映射无法进行。且已经进行过宾语自动化。可能需要手动调整。")
                try_to_deal_id_coincide(language, isyes, rwmap)

            if input_path != output_path:
                isrestore = "n"
                if isquestion:
                    isrestore = question(language, True, "Is the map saved back to the input path after the objects ID is rearranged?" + \
                                            "|宾语ID重排后的地图是否保存回原文件？", ["y", "n"], [], 
                                            {"n": "The map doesn't save in input path. Continue.|原文件未保存，程序继续。"}, 
                                            isyes, "y")
                if isrestore == "y":
                    standard_out(language, isverbose, "The map which objects ID is rearranged is restoring...|ID重排地图正在保存中...")
                    rwmap.write_file(input_path)

        debug_do_num = debug_do_num + 1
    return id_to_tobject

def check_input_output_path(isdebug:bool, language:str, isyes:str, input_path:str, output_path:str):
    question(language, input_path == output_path, "The input path is the same as output path. The source file will be overwritten. Do you want to continue?" + \
             "|输入地图路径和输出地图路径相同。原文件将被覆盖。是否要继续？", ["y", "n"], ["n"], {}, isyes, "y")
    if os.path.isdir(output_path):
        standard_error(isdebug, language, "There's a dir on the output path. " + \
                       "|输出路径是一个目录。", 30)
    elif os.path.isfile(output_path):
        question(language, input_path != output_path, "There's a file on the output path. The source file will be overwritten. Do you want to continue?" + \
                "|输出地图路径有原文件。原文件将被覆盖。是否要继续？", ["y", "n"], ["n"], {}, isyes, "y")
        
def imagelayer_check(map_now:rw.RWmap, imagelayer_name:str, isdebug:str, language:str):
    imagelayer_name_list = [imagelayer.name() for imagelayer in map_now._imageLayer_list]
    if imagelayer_name == '|':
        if len(map_now._imageLayer_list) != 1:
            standard_error(isdebug, language, f"There's no imagelayer name(with the num is less than 1) and can't sure about the imagelayer.(real list:{imagelayer_name_list})" + 
                           f"|没有图像层名称(且图像层数目不为1)，因此无法确定图像层。(实际图像层:{imagelayer_name_list})", 32)

    else:
        if map_now.get_imageLayer_s(imagelayer_name) == None:
            standard_error(isdebug, language, f"The name of imagelayer is wrong.(name:{imagelayer_name}, real list:{imagelayer_name_list})" + 
                           f"|图像层名称错误。(名称:{imagelayer_name}, 实际图像层:{imagelayer_name_list})", 33)
            
def hex_to_rgb(hex_color:str):
    return tuple(int(hex_color[i:i+2], 16) for i in (1, 3, 5))

def hex_list_to_rgb_nparr(hex_color:list, tiy:int = -1):
    tiy = len(hex_color) if tiy == -1 else tiy
    tix = math.ceil(len(hex_color) / tiy)
    nparr = np.ndarray((tix, tiy, 3), np.uint8)
    for index, hex_color_one in enumerate(hex_color):
        ix = index // tiy
        iy = index % tiy
        nparr[ix, iy] = np.array(hex_to_rgb(hex_color_one), np.uint8).reshape([1, 1, 3])
    return nparr

def element_error(isdebug:bool, language:str, name:str, error:KeyError):
    if isinstance(error, rw.rwexceptions.ElementOriNotFoundError):
        standard_error(isdebug, language, f"Element \"{name}\" does not exist. Please add layer/objectgroup/tileset/imagelayer" + \
                     f"|元素 \"{name}\" 不存在。请添加对应图层/宾语层/地块集/图像层...", 36)
    elif isinstance(error, rw.rwexceptions.ElementOriFoundMultiError):
        standard_error(isdebug, language, f"More than one element match \"{name}\" . Please delete one of layer/objectgroup/tileset/imagelayer" + \
                     f"|多于一个元素匹配了 \"{name}\" 。请删除多余的对应图层/宾语层/地块集/图像层...", 37)

def get_rwmap_ele_ex(isdebug:bool, language:str, rwmap:rw.RWmap, RWmap_func, name:str)->rw.frame.ElementOri:
    try:
        return RWmap_func(rwmap, name)
    except KeyError as e:
        element_error(isdebug, language, name, e)


def isvalid_re(pattern:str)->bool:
    try:
        re.compile(pattern)
    except:
        return False
    else:
        return True

def is_intmin_integer(s:str, int_min:int):
    try:
        num = int(s)
        return num >= int_min
    except:
        return False

def is_intmin_integer_t(mt:tuple):
    return is_intmin_integer(mt[0], mt[1])

CONFIG_ERROR_ID_SET = set([i for i in range(-1, 38)] + [156, 241, 242]) 
CONFIG_CODE_SET = set()
MAX_ERROR_TOP_ID = 229
MAX_CONFIG_TOP_ID = 121

def error_id_debug(isdebug, config_code, error_id, error_id_add, strlist_pre, arg, config):
    if isdebug:
        global CONFIG_ERROR_ID_SET

        if config_code != None and (not (config_code in CONFIG_CODE_SET)):
            isde = False
            if error_id != None:
                error_set = set([error_id + i for i in range(error_id_add)])
                if len(error_set.intersection(CONFIG_ERROR_ID_SET)) != 0:
                    print(f"error_id:{error_id} wrong.")
                    isde = True
                else:
                    error_t = (CONFIG_ERROR_ID_SET | error_set)
                    error_z = set([i for i in range(min(error_t), max(error_t) + 1)])
                    error_d = error_z.difference(error_t)
                    if len(error_d) != 0:
                        if len(error_d) > 10:
                            print(f"empty: {set([i for i in error_d][0:10])}...more than 10 | warning.")
                        else:
                            print(f"empty: {error_d} | warning.")
                    CONFIG_ERROR_ID_SET = error_t

            else:
                print(f"error_id:empty")
                isde = True

            if isde:
                print(f"real error_id:{max(CONFIG_ERROR_ID_SET) + 1}")
                print(f"config ID:{config_code}\n")
                print(f"(path:{strlist_pre + ([arg] if config != None else [])})\n")
                print(f"set:{CONFIG_ERROR_ID_SET}\n")
                print(f"config ID set:{CONFIG_CODE_SET}\n")
                import pdb;pdb.set_trace()

            CONFIG_CODE_SET.add(config_code)

def some_func_ex(isdebug:bool, language:str, strlist_pre:list, config_code:int, error_id:int, 
                 key, pass_func_ex, info_err:str):

    error_id_add = 1
    config = 1

    if not pass_func_ex(key):
        info_err_now = langstrlist_add([info_err, f"(path:{strlist_pre})|(路径:{strlist_pre})"])
        standard_error(isdebug, language, info_err_now, error_id)

    error_id_debug(isdebug, config_code, error_id, error_id_add, strlist_pre, key, config)


def is_int_min_integer_ex(isdebug, language, s:str, int_min:int, strlist_pre:list, config_code:int, error_id:int = None):
    some_func_ex(isdebug, language, strlist_pre, config_code, error_id, (s, int_min), is_intmin_integer_t, 
                 f"String {s} can not be transtlated into integer.(>={int_min})" + \
                       f"|字符串 {s} 不能被翻译为整数(>={int_min})。")

def isvalid_re_ex(isdebug, language, pattern:str, strlist_pre:list, config_code:int, error_id:int = None):
    some_func_ex(isdebug, language, strlist_pre, config_code, error_id, pattern, isvalid_re, 
                 f"Pattern {pattern} is invalid." + \
                 f"|模式 \"{pattern}\" 不是一个合法的正则表达式。")
    
def istype_minmax(element, itype, int_max = None, int_min = None, index = None)->bool:
    if not isinstance(element, itype):
        return False
    int_min_now = (int_min[index] if index != None else int_min) if int_min != None else None
    int_max_now = (int_max[index] if index != None else int_max) if int_max != None else None
    try:
        if int_min_now != None and element < int_min_now:
            return False
        if int_max_now != None and element > int_max_now:
            return False
    except:
        import pdb;pdb.set_trace()
    return True

def ismatrix(matrix, size:tuple[int, int], itype, int_min = None, int_max = None, islist = False, list_lenmax = None, list_lenmin = None)->bool:
    if (isinstance(matrix, list) and len(matrix) == size[0]):
        for li in matrix:
            if (isinstance(li, list) and len(li) == size[1]):
                for lii in li:
                    if islist and isinstance(lii, list):
                        if list_lenmax != None and len(lii) > list_lenmax:
                            return False
                        if list_lenmin != None and len(lii) < list_lenmin:
                            return False
                        for i, liii in enumerate(lii):
                            if not istype_minmax(liii, itype, int_max, int_min, i):
                                return False
                    else:
                        int_max_0 = (int_max[0] if isinstance(int_max, list) else int_max) if int_max != None else None
                        int_min_0 = (int_min[0] if isinstance(int_min, list) else int_min) if int_min != None else None
                        if not istype_minmax(lii, itype, int_max_0, int_min_0):
                            return False
            else:
                return False
    else:
        return False
    
    return True

def ismatrix_t(mt:tuple):
    return ismatrix(mt[0], mt[1], mt[2], mt[3], mt[4], mt[5], mt[6], mt[7])

def coointileset(coo:list, size:tuple[int, int]):
    if coo[0] >= size[0] or coo[1] >= size[1]:
        return False
    else:
        return True

def coointileset_t(mt:tuple):
    return coointileset(mt[0], mt[1])

def tileidintileset(tileid:int, size:tuple[int, int]):
    if tileid >= size[0] * size[1]:
        return False
    else:
        return True

def tileidintileset_t(mt:tuple):
    return tileidintileset(mt[0], mt[1])

def coointileset_ex(isdebug, language, tileset_name:str, coo:list, size:tuple[int, int], strlist_pre:list, config_code:int, error_id:int = None):
    mt = (coo, size)
    some_func_ex(isdebug, language, strlist_pre, config_code, error_id, mt, coointileset_t, 
                 f"The tile of {coo} in tileset \"{tileset_name}\" out of range({size})。" + \
                 f"|地块集 \"{tileset_name}\" 提取 {coo} 的地块超过边界({size})。")

def tileidintileset_ex(isdebug, language, tileset_name:str, tileid:int, size:tuple[int, int], strlist_pre:list, config_code:int, error_id:int = None):
    mt = (tileid, size)
    some_func_ex(isdebug, language, strlist_pre, config_code, error_id, mt, tileidintileset_t, 
                 f"The tileid of {tileid} in tileset \"{tileset_name}\" out of range({size})。" + \
                 f"|地块集 \"{tileset_name}\" 提取 {tileid} 的地块超过边界({size})。")

def ismatrix_ex(isdebug, language, strlist_pre:list, matrix, size:tuple[int, int], itype, config_code:int, int_min = None, int_max = None, islist = False, list_lenmax = None, list_lenmin = None, error_id:int = None):
    mt = (matrix, size, itype, int_min, int_max, islist, list_lenmax, list_lenmin)
    some_func_ex(isdebug, language, strlist_pre, config_code, error_id, mt, ismatrix_t, 
                 f"Variable {cjs.config_element_str_n(mt[0])} is not a matrix with type {f"{mt[2]}/list[{mt[2]}]" if mt[5] else f"{mt[2]}"} and size {mt[1]}.{f"(length: {list_lenmin}-{list_lenmax})" if islist else ""}(min:{mt[3] if mt[3] != None else "no"}, max: {mt[4] if mt[4] != None else "no"})" + \
                       f"|变量 {cjs.config_element_str_n(mt[0])} 不是一个元素类型为{f"{mt[2]}/{mt[2]}的列表" if mt[5] else f"{mt[2]}"}{f" (长度: {list_lenmin}-{list_lenmax})" if islist else ""}, 形状为 {mt[1]} 的矩阵。(最小值:{mt[3] if mt[3] != None else "无"}, 最大值: {mt[4] if mt[4] != None else "无"})")

def re_inset_len(pattern:str, mset:set[str]):
    matching_items = [item for item in mset if re.match(pattern, item)]
    matching_count = len(matching_items)
    return (matching_items, matching_count)

def re_inset_ex(isdebug, language, pattern:str, mset:set[str], strlist_pre:list, config_code:int, error_id:int, isinvalueset:bool = True):
    isvalid_re_ex(isdebug, language, pattern, strlist_pre, config_code, error_id)
    ml, mc = re_inset_len(pattern, mset)
    if isinvalueset:
        if mc == 0:
            standard_error(isdebug, language, f"Pattern {pattern} can not match the set {mset}(path:{strlist_pre})" + \
                    f"|模式 \"{pattern}\" 无法与 {mset} 匹配。(路径:{strlist_pre})", error_id + 1)

        elif mc >= 2:
            standard_error(isdebug, language, f"The match number of the pattern {pattern} for the set {mset} is larger than 1(path:{strlist_pre})" + \
                        f"|模式 \"{pattern}\" 匹配 {mset} 的匹配数目大于1。(路径:{strlist_pre})", error_id + 2)
        return ml[0]
    else:
        if mc != 0:
            standard_error(isdebug, language, f"The match number of the pattern {pattern} for the set {mset} is not zero.(path:{strlist_pre})" + \
                        f"|模式 \"{pattern}\" 匹配 {mset} 的匹配数目不为0。(路径:{strlist_pre})", error_id + 1)
        return None

    

def config_get_ex(isdebug:bool, language:str, config:Union[list, dict, None], strlist_pre:list, 
                  key, config_code:int, error_id:int = None, itype:Union[type, tuple[type]] = None, value_set:set = None, 
                  islist_add:bool = False, simplify:dict = None, default = None, islist = False, 
                  int_min:int = None, int_max:int = None, len_max:int = None, len_min:int = None, isinvalueset = True):

    if error_id == None:
        error_id = 38

    error_id_add = 0
                
    if config != None:
            if islist:
                if key >= len(config):
                    if default == None:
                        standard_error(isdebug, language, f"Index {key} exceeds.(len:{len(config)}, path:{strlist_pre})" + \
                                    f"|索引 {key} 超出列表长度.(列表长度:{len(config)}, 路径:{strlist_pre})", error_id + error_id_add)
                    else:
                        ck = default
                ck = config[key]
            else:
                ck = config.get(key)
                if ck == None:
                    if default == None:
                        standard_error(isdebug, language, f"Key {key} is empty(path:{strlist_pre})" + \
                                    f"|键 {key} 是空的(路径:{strlist_pre})", error_id + error_id_add)
                    else:
                        ck = default
            if default == None:
                error_id_add = error_id_add + 1
    else:
        if default == None:
            ck = key
        else:
            ck = default

    if simplify != None:
        ckg = simplify.get(ck)
        ck = f"^{re.escape(ck)}$" if ckg == None else ckg
        isre = True
    else:
        isre = False
    if itype != None:
        if not isinstance(ck, itype):
            standard_error(isdebug, language, f"The type {type(ck)} of value {cjs.config_element_str_n(ck)} translated by {key} can not match correct type {itype}.(path:{strlist_pre})" + \
                        f"|键 {key} 的值 {cjs.config_element_str_n(ck)} 的类型 {type(ck)} 与正确类型 {itype} 不匹配。(路径:{strlist_pre})", error_id + error_id_add)
        error_id_add = error_id_add + 1

    if len_max != None:
        if (type(ck) in set([dict, list])):
            if len(ck) > len_max:
                standard_error(isdebug, language, f"The length {len(ck)} of value {cjs.config_element_str_n(ck)} translated by {key} is larger than {len_max}.(path:{strlist_pre})" + \
                        f"|键 {key} 的值 {cjs.config_element_str_n(ck)} 的长度 {len(ck)} 大于 {len_max}。(路径:{strlist_pre})", error_id + error_id_add)
        error_id_add = error_id_add + 1

    if len_min != None:
        if (type(ck) in set([dict, list])):
            if len(ck) < len_min:
                standard_error(isdebug, language, f"The length {len(ck)} of value {cjs.config_element_str_n(ck)} translated by {key} is less than {len_min}.(path:{strlist_pre})" + \
                        f"|键 {key} 的值 {cjs.config_element_str_n(ck)} 的长度 {len(ck)} 小于 {len_min}。(路径:{strlist_pre})", error_id + error_id_add)
        error_id_add = error_id_add + 1

        


    
    if value_set != None:
        if isre:
            ck = re_inset_ex(isdebug, language, ck, value_set, strlist_pre + ([key] if config != None else []), None, error_id + error_id_add, isinvalueset = isinvalueset)
            error_id_add = error_id_add + 2 + (isinvalueset)
        else:
            if isinvalueset ^ (ck in value_set):
                standard_error(isdebug, language, f"Value {cjs.config_element_str_n(ck)} translated by {key} is not in set {value_set}.(path:{strlist_pre})" + \
                            f"|键 {key} 的值 {cjs.config_element_str_n(ck)} 不在集合内 {value_set}。(路径:{strlist_pre})", error_id + error_id_add)
            error_id_add = error_id_add + 1

    if int_min != None:
        if (type(ck) in set([int, float])):
            if ck < int_min:
                standard_error(isdebug, language, f"Value {cjs.config_element_str_n(ck)} translated by {key} is less than {int_min}.(path:{strlist_pre})" + \
                            f"|键 {key} 的值 {cjs.config_element_str_n(ck)} 小于 {int_min}。(路径:{strlist_pre})", error_id + error_id_add)
        error_id_add = error_id_add + 1
    if int_max != None:
        if (type(ck) in set([int, float])):
            if ck > int_max:
                standard_error(isdebug, language, f"Value {cjs.config_element_str_n(ck)} translated by {key} is larger than {int_max}.(path:{strlist_pre})" + \
                            f"|键 {key} 的值 {cjs.config_element_str_n(ck)} 大于 {int_max}。(路径:{strlist_pre})", error_id + error_id_add)
        error_id_add = error_id_add + 1

    error_id_debug(isdebug, config_code, error_id, error_id_add, strlist_pre, key, config)

    if islist_add:
        strlist_pre.append(key)

    return ck