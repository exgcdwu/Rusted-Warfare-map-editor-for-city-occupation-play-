import os
import sys
import json
import shutil
import xml.etree.ElementTree as et
from pprint import pprint
from copy import deepcopy
import numpy as np
import math

current_file_path = os.path.abspath(__file__)
current_dir_path = os.path.dirname(current_file_path)
command_dir_path = os.path.dirname(current_dir_path)
package_dir = os.path.dirname(command_dir_path)

sys.path.append(package_dir)

import rwmap as rw

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

full_screen = int(shutil.get_terminal_size().columns / 2) * 2
underline_even_num = int(full_screen * 3 / 8) * 2

cite_object_dict = {}

language_dict = {"eg" : 0, "ch" : 1}
language_set = set(language_dict.keys())

full_screen = int(shutil.get_terminal_size().columns / 2) * 2
underline_even_num = int(full_screen * 3 / 8) * 2

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
        debug_pdb("standard print error(language).")
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

        left_bk = int(full_screen / 2 - underline_even_num / 2)
        left_ul = int(underline_even_num / 2 - lenstr / 2)
        right_ul = left_ul

        print(" " * left_bk + "-" * underline_even_num)
        print(" " * left_bk + "-" * left_ul + info_str_now + "-" * right_ul)
        print(" " * left_bk + "-" * underline_even_num)

def langstr_add_str(langstr:str, str_now:str):
    return "|".join([langstr + str_now for langstr in langstr.split("|")])

def langstrlist_add(langstr_list:list):
    if langstr_list == []:
        return '|'
    langstr_matrix = [langstr.split("|") for langstr in langstr_list]
    max_lang = max([len(langstr_list) for langstr_list in langstr_matrix])
    langstr_ans = "|".join([''.join([langstr_matrix[i][j] for i in range(len(langstr_matrix)) if j < len(langstr_matrix[i])]) for j in range(max_lang)])
    return langstr_ans

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
            standard_out(language, True, tip_now)
            standard_out(language, True, f"Automatically enter {auto}.|自动输入{auto}。")
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

def get_rwmap(isdebug:bool, language:str, rwpath:str)->rw.RWmap:
    try:
        standard_out(language, True, f"RW map input({rwpath})..." + 
            f"|地图文件导入({rwpath})...")
        map_now = rw.RWmap.init_mapfile(f'{rwpath}')
        return map_now
    except FileNotFoundError:
        standard_error(isdebug, language, "RW map file is not found, please check your input path.|铁锈输入地图文件未找到，请仔细检查地图路径。", 24)
    except et.ParseError:
        standard_error(isdebug, language, "File parsing error, the file may not be XML file. Maybe it's not RW map file.|地图文件解析错误，不符合xml格式。也许导入的不是铁锈地图。", 25)

def output_rwmap(isdebug:bool, language:str, rwmap:rw.RWmap, output_path:str, ischangemappath:bool = True, isdeletetsxsource:bool = False, isdeleteimgsource:bool = False)->None:
    try:
        standard_out(language, True, f"RW map output({output_path})..." + 
            f"|地图文件导出({output_path})...")
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
                rwmap.resetid()
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
            standard_error(isdebug, language, "There's no imagelayer name(with the num is less than 1) and can't sure about the imagelayer.(real list:{imagelayer_name_list})" + 
                           "|没有图像层名称(且图像层数目不为1)，因此无法确定图像层。(实际图像层:{imagelayer_name_list})", 32)

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