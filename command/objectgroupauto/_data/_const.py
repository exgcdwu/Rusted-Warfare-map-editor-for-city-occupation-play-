import inspect
from collections import OrderedDict

import os
import sys
from copy import deepcopy

current_file_path = os.path.abspath(__file__)
current_dir_path = os.path.dirname(current_file_path)
auto_dir_path = os.path.dirname(current_dir_path)
package_dir = os.path.dirname(current_dir_path)
sys.path.append(package_dir)
import rwmap as rw

from command.objectgroupauto._core import AUTOKEY
from command.objectgroupauto._core import MAXTRANSDEPTH

class INFOKEY:
    prefix = "prefix"
    idprefix = "idprefix"
    isprefixseg = "isprefixseg"
    objectType = "objectType"
    name = "name"
    cite_name = "cite_name"
    offset = "offset"
    offsetsize = "offsetsize"
    textsize = "textsize"
    args = "args"
    opargs = "opargs"
    acti = "acti"
    deacti = "deacti"
    brace = "brace"
    exist = "exist"
    neutralindex = "neutralindex"

    object_info = "object_info"
    teamDetect_info = "teamDetect_info"
    multiText_info = "multiText_info"
    teamDetect_cite = "teamDetect_cite"
    isdefaultText = "isdefaultText"
    building_info = "building_info"
    mtext_info = "mtext_info"
    inadd_info = "inadd_info"
    inadd_prefix = "inadd_prefix"
    mtext_prefix = "mtext_prefix"
    time_prefix = "time_prefix"
    numDetect_info = "numDetect_info"
    numDetect_cite = "numDetect_cite"
    dictionary_info = "dictionary_info"
    multiRemove_info = "multiRemove_info"
    tree_info = "tree_info"
    multiAdd_info = "multiAdd_info"
    flash_info = "flash_info"
    building_f_info = "building_f_info"
    idcheck_info = "idcheck_info"
    time_info = "time_info"
    step_info = "step_info"

    setTeam = "setTeam"
    setidTeam = "setidTeam"
    lenidTeam = "lenidTeam"
    aunit = "aunit"
    aunitbrace = "aunitbrace"
    minUnits = "minUnits"
    maxUnits = "maxUnits"
    reset = "reset"
    warmup = "warmup"
    delay = "delay"
    repeat = "repeat"

    color = "color"
    text = "text"
    setNum = "setNum"
    setidNum = "setidNum"
    lenidNum = "lenidNum"
    lenTeam = "lenTeam"
    otherid = "otherid"

    detectReset = "detectReset"
    addWarmup = "addWarmup"
    addReset = "addReset"
    removeReset = "removeReset"
    spawnnum = "spawnnum"
    team = "team"
    addname = "addname"
    addoffset = "addoffset"
    addoffsetsize = "addoffsetsize"
    detectname = "detectname"
    detectoffset = "detectoffset"
    detectoffsetsize = "detectoffsetsize"
    removename = "removename"
    isonlybuilding = "isonlybuilding"
    isshowOnMap = "isshowOnMap"
    isdetectdeacti = "isdetectdeacti"
    basicoffset = "basicoffset"
    basicoffsetsize = "basicoffsetsize"

    ismtext = "ismtext"
    mcolor = "mcolor"
    mtextsize = "mtextsize"
    mname = "mname"
    moffset = "moffset"
    moffsetsize = "moffsetsize"
    mtext = "mtext"
    istime = "istime"
    iscorrectwarmup = "iscorrectwarmup"
    timeratio = "timeratio"

    isinadd = "isinadd"
    inaddunit = "inaddunit"
    inaddspawnnum = "inaddspawnnum"
    inaddteam = "inaddteam"
    inaddwarmup = "inaddwarmup"
    inaddisshowOnMap = "inaddisshowOnMap"
    inaddname = "inaddname"
    inaddoffset = "inaddoffset"
    inaddoffsetsize = "inaddoffsetsize"
    inaddisinitialunit = "inaddisinitialunit"
    inaddaunitbrace = "inaddaunitbrace"

    spawnUnits = "spawnUnits"
    initialtime = "initialtime"
    periodtime = "periodtime"
    initialacti = "initialacti"
    periodacti = "periodacti"
    initialdeacti = "initialdeacti"
    perioddeacti = "perioddeacti"
    steptime = "steptime"
    isactiend = "isactiend"
    stepacti = "stepacti"
    stepdeacti = "stepdeacti"


class OBJECT_ARGS:
    type = "type"
    fog = "fog"
    introText = "introText"
    winCondition = "winCondition"
    loseCondition = "loseCondition"
    survivalWaves = "survivalWaves"

    credits = "credits"
    disabledAI = "disabledAI"
    lockAiDifficulty = "lockAiDifficulty"
    ai = "ai"
    allyGroup = "allyGroup"
    basicAI = "basicAI"

    unitType = "unitType"
    onlyIdle = "onlyIdle"
    onlyBuildings = "onlyBuildings"
    onlyMainBuildings = "onlyMainBuildings"
    onlyEmptyQueue = "onlyEmptyQueue"
    onlyBuilders = "onlyBuilders"
    onlyOnResourcePool = "onlyOnResourcePool"
    onlyAttack = "onlyAttack"
    onlyAttackAir = "onlyAttackAir"
    onlyTechLevel = "onlyTechLevel"
    includeIncomplete = "includeIncomplete"
    minUnits = "minUnits"
    maxUnits = "maxUnits"
    onlyWithTag = "onlyWithTag"

    target = "target"
    unload = "unload"
    dir = "dir"

    addTeamTags = "addTeamTags"
    removeTeamTags = "removeTeamTags"

    teamTag = "teamTag"

    text = "text"
    textColor = "textColor"
    textSize = "textSize"
    textOffsetX = "textOffsetX"
    textOffsetY = "textOffsetY"
    style = "style"
    text_lang = "text_lang"

    set = "set"
    add = "add"
    spawnUnits = "spawnUnits"
    team = "team"
    globalMessage = "globalMessage"
    globalMessage_delayPerChar = "globalMessage_delayPerChar"
    globalMessage_textColor = "globalMessage_textColor"
    debugMessage = "debugMessage"
    warmup = "warmup"
    delay = "delay"
    resetActivationAfter = "resetActivationAfter"
    repeatDelay = "repeatDelay"
    alsoActivate = "alsoActivate"
    id = "id"
    activatedBy = "activatedBy"
    deactivatedBy = "deactivatedBy"
    allToActivate = "allToActivate"
    activateIds = "activateIds"
    whenActivatedIds = "activateIds"
    showOnMap = "showOnMap"

class OBJECT_ARGS_BOOL:
    isprefixseg = "isprefixseg"
    onlyIdle = "onlyIdle"
    onlyBuildings = "onlyBuildings"
    onlyMainBuildings = "onlyMainBuildings"
    onlyEmptyQueue = "onlyEmptyQueue"
    onlyBuilders = "onlyBuilders"
    onlyOnResourcePool = "onlyOnResourcePool"
    onlyAttack = "onlyAttack"
    onlyAttackAir = "onlyAttackAir"
    includeIncomplete = "includeIncomplete"

    allToActivate = "allToActivate"
    showOnMap = "showOnMap"

OBJECT_ARGS_DICT = OrderedDict()
for name, value in inspect.getmembers(OBJECT_ARGS):
    if not inspect.isroutine(value):
        OBJECT_ARGS_DICT[name] = value

OBJECT_ARGS_BOOL_DICT = OrderedDict()
for name, value in inspect.getmembers(OBJECT_ARGS_BOOL):
    if not inspect.isroutine(value):
        OBJECT_ARGS_BOOL_DICT[name] = value  

def operation_cycle_start(var_name:str, var_initial:str, var_condition:str, tag:str):
    return [
        {
            AUTOKEY.operation_type: AUTOKEY.typeset_expression, 
            var_name: var_initial
        }, 

        {
            AUTOKEY.operation_type: AUTOKEY.tag, 
            AUTOKEY.tag: "tag_cycle_" + tag
        }, 

        {
            AUTOKEY.operation_type: AUTOKEY.typeif, 
            AUTOKEY.ifvar: var_condition, 
            AUTOKEY.ifend_tag: "tag_cycle_end_" + tag
        }
    ]

def operation_cycle_end(var_name:str, var_step:str, tag:str):
    return [
        {
            AUTOKEY.operation_type: AUTOKEY.typeset_expression, 
            var_name: var_step
        }, 

        {
            AUTOKEY.operation_type: AUTOKEY.goto, 
            AUTOKEY.goto_tag: "tag_cycle_" + tag
        },

        {
            AUTOKEY.operation_type: AUTOKEY.tag, 
            AUTOKEY.tag: "tag_cycle_end_" + tag
        }
    ]

def operation_cycle_continue(tag:str):
    return [
        {
            AUTOKEY.operation_type: AUTOKEY.goto_tag, 
            AUTOKEY.goto_tag: "tag_cycle_" + tag
        }
    ]

def operation_cycle_break(tag:str):
    return [
        {
            AUTOKEY.operation_type: AUTOKEY.goto_tag, 
            AUTOKEY.goto_tag: "tag_cycle_end_" + tag
        }
    ]

def operation_goto(tag:str):
    return [
        {
            AUTOKEY.operation_type: AUTOKEY.goto, 
            AUTOKEY.goto_tag: "tag_goto_" + tag 
        }
    ]

def operation_gototag(tag:str):
    return [
        {
            AUTOKEY.operation_type: AUTOKEY.tag, 
            AUTOKEY.tag: "tag_goto_" + tag 
        }
    ]

def operation_if(condition:str, tag:str, elseif_num:int = 1):
    return [
        {
            AUTOKEY.operation_type: AUTOKEY.typeif, 
            AUTOKEY.ifvar: condition, 
            AUTOKEY.ifend_tag: "tag_ifnext_" + str(elseif_num) + tag
        }
    ]

def operation_errorif(tag:str, elseif_num:int = 1):
    return [
        {
            AUTOKEY.operation_type: AUTOKEY.errorif, 
            AUTOKEY.ifend_tag: "tag_ifnext_" + str(elseif_num) + tag
        }
    ]

def operation_exist_if(key:str, tag:str, elseif_num:int = 1):
    return [
        {
            AUTOKEY.operation_type: AUTOKEY.typeset_exist, 
            "check_exist_temp" + tag + str(elseif_num): key
        }
    ] + \
    operation_if("check_exist_temp" + tag + str(elseif_num), tag, elseif_num)

def operation_elseif(condition:str, tag:str, elseif_num:int):
    return [
        {
            AUTOKEY.operation_type: AUTOKEY.goto, 
            AUTOKEY.goto_tag: "tag_if_end_" + tag
        }, 
        {
            AUTOKEY.operation_type: AUTOKEY.tag, 
            AUTOKEY.tag: "tag_ifnext_" + str(elseif_num - 1) + tag
        }, 
        {
            AUTOKEY.operation_type: AUTOKEY.typeif, 
            AUTOKEY.ifvar: condition, 
            AUTOKEY.ifend_tag: "tag_ifnext_" + str(elseif_num) + tag
        }
    ]

def operation_exist_elseif(key:str, tag:str, elseif_num:int):
    elseif_now = operation_elseif("check_exist_temp" + tag + str(elseif_num), tag, elseif_num)
    exist_now = [
        {
            AUTOKEY.operation_type: AUTOKEY.typeset_exist, 
            "check_exist_temp" + tag + str(elseif_num): key
        }
    ]
    return elseif_now[0:2] + exist_now + elseif_now[2:3]
def operation_else(tag:str, elseif_num:int = 2):
    return [
        {
            AUTOKEY.operation_type: AUTOKEY.goto, 
            AUTOKEY.goto_tag: "tag_if_end_" + tag
        }, 
        {
            AUTOKEY.operation_type: AUTOKEY.tag, 
            AUTOKEY.tag: "tag_ifnext_" + str(elseif_num - 1) + tag
        }, 
    ]

def operation_elseend(tag:str):
    return [
        {
            AUTOKEY.operation_type: AUTOKEY.tag, 
            AUTOKEY.tag: "tag_if_end_" + tag
        }
    ]

def operation_ifend(tag:str, elseif_num:int = 2):
    return operation_else(tag, elseif_num) + \
    operation_elseend(tag)

def operation_pdb(ID:str = None, name:str = None, print:str = None):
    operation_pdb_now = \
        {
            AUTOKEY.operation_type: AUTOKEY.pdb_pause
        }
    
    if ID != None:
        operation_pdb_now[AUTOKEY.ID] = ID
    if name != None:
        operation_pdb_now[AUTOKEY.name] = name
    if print != None:
        operation_pdb_now[AUTOKEY.print] = print
    return [operation_pdb_now]

def operation_error(error_info:str):
    return [
        {
            AUTOKEY.operation_type: AUTOKEY.error, 
            AUTOKEY.error_info: error_info
        }
    ]

def operation_typeset_expression(key:str, value:str, depth:int = MAXTRANSDEPTH, brace_exp_depth:int = MAXTRANSDEPTH):
    return [
        {
            AUTOKEY.operation_type:AUTOKEY.typeset_expression, 
            AUTOKEY.depth:depth, 
            AUTOKEY.brace_exp_depth: brace_exp_depth, 
            key: value
        }
    ]

def br(str_now:str)->str:
    return "{" + str_now + "}"

def nbr(str_now:str)->str:
    return f"u\'\\u{AUTOKEY.left_brace}\' + \'{str_now}\' + u\'\\u{AUTOKEY.right_brace}\'"

ARGS_OPARGS_PRE_OPERATION = \
    operation_exist_if("args", "args_opargs_pre_if2") + \
        operation_cycle_start("i", "0", "i < len(args)", "args_opargs_pre_cycle1") + \
            operation_if("len(args[i]) >= 3 or len(args[i]) <= 1", "args_opargs_pre_if_argserror") + \
                [
                    {
                        AUTOKEY.operation_type: AUTOKEY.error, 
                        AUTOKEY.error_info: "The number of arguments in {i + 1}-th args must be 2.(args:{args}, reality:{len(args[i])})" + \
                            "|第{i + 1}个必需参数(args)数量必须为2（参数名称、类型(str,bool)）。(args:{args}, 参数数量:{len(args[i])})"
                    },
                ] + \
            operation_ifend("args_opargs_pre_if_argserror") + \
            operation_if("'{args[i][1]}' != 'str' and '{args[i][1]}' != 'bool'", "args_opargs_pre_if_argserror_2") + \
                [
                    {
                        AUTOKEY.operation_type: AUTOKEY.error, 
                        AUTOKEY.error_info: "The 2ed of arguments in {i + 1}-th args must be str or bool.(args:{args}, reality:{args[i][1]})" + \
                        "|第{i + 1}个必需参数的第二个参数必须是str或bool。(args:{args}, 参数类型:{args[i][1]})"
                    },
                ] + \
            operation_ifend("args_opargs_pre_if_argserror_2") + \
            [
                {
                    AUTOKEY.operation_type: AUTOKEY.typeadd_optional, 
                    AUTOKEY.nameadd_optional: "[args[i][0]]"
                }, 
                {
                    AUTOKEY.operation_type: AUTOKEY.typeadd_args, 
                    "{args[i][0]}": "args[i][1]"
                }
            ] + \
        operation_cycle_end("i", "i + 1", "args_opargs_pre_cycle1") + \
    operation_ifend("args_opargs_pre_if2") + \
    operation_exist_if("opargs", "args_opargs_pre_if3") + \
        operation_cycle_start("i", "0", "i < len(opargs)", "args_opargs_pre_cycle2") + \
            operation_if("len(opargs[i]) >= 5 or len(opargs[i]) <= 2", "args_opargs_pre_if_opargserror") + \
                [
                    {
                        AUTOKEY.operation_type: AUTOKEY.error, 
                        AUTOKEY.error_info: "The number of arguments in {i + 1}-th opargs must be 3 or 4.(opargs:{opargs}, reality:{len(opargs[i])})" + \
                        "|第{i + 1}个选填参数(opargs)数量必须在3-4之间。(opargs:{opargs}, 参数数量:{len(opargs[i])})"
                    },
                ] + \
            operation_ifend("args_opargs_pre_if_opargserror") + \
            operation_if("'{opargs[i][2]}' != 'str' and '{opargs[i][2]}' != 'bool'", "args_opargs_pre_if_opargserror_2") + \
                [
                    {
                        AUTOKEY.operation_type: AUTOKEY.error, 
                        AUTOKEY.error_info: "The 3th of arguments in {i + 1}-th opargs must be str or bool.(opargs:{opargs}, reality:{opargs[i][2]})" + \
                            "|第{i + 1}个选填参数的第三个参数必须是str或bool。(opargs:{opargs}, 参数类型:{opargs[i][2]})"
                    },
                ] + \
            operation_ifend("args_opargs_pre_if_opargserror_2") + \
            operation_if("len(opargs[i][0]) != 1", "args_opargs_pre_if_opargserror_3") + \
                [
                    {
                        AUTOKEY.operation_type: AUTOKEY.error, 
                        AUTOKEY.error_info: "The length of first arguments in {i + 1}-th opargs must be 1.(opargs:{opargs}, reality:{len(opargs[i][0])})" + \
                            "|第{i + 1}个选填参数的第一个参数的长度必须为1。(opargs:{opargs}, 参数长度:{len(opargs[i][0])})"
                    },
                ] + \
            operation_ifend("args_opargs_pre_if_opargserror_3") + \
            operation_if("len(opargs[i]) == 3", "args_opargs_pre_if1") + \
                [
                    {
                        AUTOKEY.operation_type: AUTOKEY.typeadd_opargs, 
                        "{opargs[i][0]}&12": "(opargs[i][1], opargs[i][2])"
                    }
                ] + \
            operation_else("args_opargs_pre_if1") + \
                [
                    {
                        AUTOKEY.operation_type: AUTOKEY.typeadd_opargs, 
                        "{opargs[i][0]}&12": "(opargs[i][1] + \'|\' + opargs[i][3], opargs[i][2])"
                    }
                ] + \
            operation_elseend("args_opargs_pre_if1") + \
        operation_cycle_end("i", "i + 1", "args_opargs_pre_cycle2") + \
    operation_ifend("args_opargs_pre_if3")

BRACE_OPERATION_END = \
    operation_exist_if(f"{INFOKEY.brace}", "brace_operation_if_1") + \
        operation_cycle_start("i", "0", f"i < len({INFOKEY.brace})", "brace_operation_cycle_1") + \
            operation_typeset_expression("{" + f"{INFOKEY.brace}[i]" + "}", "{" + f"{INFOKEY.brace}[i]" + "}") + \
        operation_cycle_end("i", "i + 1", "brace_operation_cycle_1") + \
    operation_ifend("brace_operation_if_1")
    
def args_opargs_add_info(info_dict:str)->dict:
    info_dict_ans = deepcopy(info_dict)
    for key, value in info_dict_ans.items():
        value[AUTOKEY.info_args].update({AUTOKEY.args: (list, list, str), 
                                         AUTOKEY.opargs: (list, list, str)})
        if value.get(AUTOKEY.operation_pre) == None:
            value[AUTOKEY.operation_pre] = []
        value[AUTOKEY.operation_pre] = value[AUTOKEY.operation_pre] + ARGS_OPARGS_PRE_OPERATION
        if value.get(AUTOKEY.default_args) == None:
            value[AUTOKEY.default_args] = {}
        value[AUTOKEY.default_args].update({})
        if value.get(AUTOKEY.var_dependent) == None:
            value[AUTOKEY.var_dependent] = {}
        value[AUTOKEY.var_dependent].update({})
        if value.get(AUTOKEY.optional) == None:
            value[AUTOKEY.optional] = set()
        value[AUTOKEY.optional].update({AUTOKEY.args, AUTOKEY.opargs})
        if value.get(AUTOKEY.info_prefix) == None:
            value[AUTOKEY.info_prefix] = {}
        value[AUTOKEY.info_prefix].update({})
    return info_dict_ans

def brace_add_info(info_dict:str)->dict:
    info_dict_ans = deepcopy(info_dict)
    for key, value in info_dict_ans.items():
        value[AUTOKEY.info_args].update({AUTOKEY.brace: (list,  str)})
        if value.get(AUTOKEY.operation_pre) == None:
            value[AUTOKEY.operation_pre] = []
        value[AUTOKEY.operation_pre] = value[AUTOKEY.operation_pre]
        if value.get(AUTOKEY.operation) == None:
            value[AUTOKEY.operation] = []
        value[AUTOKEY.operation] = value[AUTOKEY.operation] + BRACE_OPERATION_END
        if value.get(AUTOKEY.default_args) == None:
            value[AUTOKEY.default_args] = {}
        value[AUTOKEY.default_args].update({})
        if value.get(AUTOKEY.var_dependent) == None:
            value[AUTOKEY.var_dependent] = {}
        value[AUTOKEY.var_dependent].update({})
        if value.get(AUTOKEY.optional) == None:
            value[AUTOKEY.optional] = set()
        value[AUTOKEY.optional].update({AUTOKEY.brace,})
        if value.get(AUTOKEY.info_prefix) == None:
            value[AUTOKEY.info_prefix] = {}
        value[AUTOKEY.info_prefix].update({})
    return info_dict_ans

def check_minmaxUnits_operation(info_tag:str)->list:
    return \
    operation_exist_if(f"{INFOKEY.minUnits}", info_tag + "_existifminUnits_error") + \
        operation_if(f"{INFOKEY.minUnits} <= 0", info_tag + "_if_minUnits_error") + \
            operation_error("minUnits({minUnits}) <= 0, please check your " + info_tag + " or tagged object." + \
                            "|minUnits({minUnits}) <= 0, 请查看对应 " + info_tag + " 和标记宾语是否出错") + \
        operation_ifend(info_tag + "_if_minUnits_error") + \
    operation_ifend(info_tag + "_existifminUnits_error") + \
    operation_exist_if(f"{INFOKEY.maxUnits}", info_tag + "_existifmaxUnits_error") + \
        operation_if(f"{INFOKEY.maxUnits} < 0", info_tag + "_if_maxUnits_error") + \
            operation_error("maxUnits({maxUnits}) < 0, please check your " + info_tag + " or tagged object." + \
                            "|maxUnits({maxUnits}) < 0, 请查看对应 " + info_tag + " 和标记宾语是否出错") + \
        operation_ifend(info_tag + "_if_maxUnits_error") + \
        operation_exist_if(f"{INFOKEY.minUnits}", info_tag + "_existifminUnits_error2") + \
            operation_if(f"{INFOKEY.minUnits} > {INFOKEY.maxUnits}", info_tag + "_if_minmaxUnits_error") + \
                operation_error("minUnits({minUnits}) > maxUnits({maxUnits}), please check your " + info_tag + " or tagged object." + \
                                "|minUnits({minUnits}) > maxUnits({maxUnits}), 请查看对应 " + info_tag + " 和标记宾语是否出错") + \
            operation_ifend(info_tag + "_if_minmaxUnits_error") + \
        operation_ifend(info_tag + "_existifminUnits_error2") + \
    operation_ifend(info_tag + "_existifmaxUnits_error")

def check_aunit_operation(info_tag:str)->list:
    return \
    operation_exist_if(f"{INFOKEY.aunit}", info_tag + "_existifaunit_error") + \
        operation_if(f"'*' in '{INFOKEY.aunit}' or ',' in '{INFOKEY.aunit}'", info_tag + "_if_aunit_error") + \
            operation_error("aunit({aunit}) is not allowed to have '*' or ',', aunit is the name of unit(no number, no variety), please check your " + info_tag + " or tagged object." + \
                            "|aunit({aunit})不许有'*'或',', 没有数目和多种, 请查看对应 " + info_tag + " 和标记宾语是否出错") + \
        operation_ifend(info_tag + "_if_aunit_error") + \
    operation_ifend(info_tag + "_existifaunit_error")

error_brace_index = 0

def error_brace(operation_list:list)->list:
    global error_brace_index
    error_brace_index = error_brace_index + 1
    return operation_errorif("operation_error_if" + str(error_brace_index) + "t") + \
           operation_list + \
           operation_ifend("operation_error_if" + str(error_brace_index) + "t")