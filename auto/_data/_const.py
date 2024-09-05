import inspect
from collections import OrderedDict

import os
import sys

current_file_path = os.path.abspath(__file__)
current_dir_path = os.path.dirname(current_file_path)
auto_dir_path = os.path.dirname(current_dir_path)
package_dir = os.path.dirname(current_dir_path)
sys.path.append(package_dir)
import rwmap as rw

from auto._core import AUTOKEY
from auto._core import MAXTRANSDEPTH

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

    object_info = "object_info"
    teamDetect_info = "teamDetect_info"
    multiText_info = "multiText_info"
    teamDetect_cite = "teamDetect_cite"
    isdefaultText = "isdefaultText"
    building_info = "building_info"
    bdtext_info = "bdtext_info"
    inadd_info = "inadd_info"
    inadd_prefix = "inadd_prefix"
    bdtext_prefix = "bdtext_prefix"
    numDetect_info = "numDetect_info"
    numDetect_cite = "numDetect_cite"
    dictionary_info = "dictionary_info"
    multiRemove_info = "multiRemove_info"
    tree_info = "tree_info"
    multiAdd_info = "multiAdd_info"
    flash_info = "flash_info"
    building_f_info = "building_f_info"

    setTeam = "setTeam"
    setidTeam = "setidTeam"
    lenidTeam = "lenidTeam"
    unit = "unit"
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

    detectReset = "detectReset"
    addWarmup = "addWarmup"
    addReset = "addReset"
    spawnnum = "spawnnum"
    team = "team"
    addname = "addname"
    addoffset = "addoffset"
    addoffsetsize = "addoffsetsize"
    detectname = "detectname"
    detectoffset = "detectoffset"
    detectoffsetsize = "detectoffsetsize"
    isonlybuilding = "isonlybuilding"
    isshowOnMap = "isshowOnMap"

    isbdtext = "isbdtext"
    bdcolor = "bdcolor"
    bdtextsize = "bdtextsize"
    bdname = "bdname"
    bdoffset = "bdoffset"
    bdoffsetsize = "bdoffsetsize"
    bdtext = "bdtext"

    isinadd = "isinadd"
    inaddunit = "inaddunit"
    inaddspawnnum = "inaddspawnnum"
    inaddteam = "inaddteam"
    inaddwarmup = "inaddwarmup"
    inaddisshowOnMap = "inaddisshowOnMap"
    inaddname = "inaddname"
    inaddoffset = "inaddoffset"
    inaddoffsetsize = "inaddoffsetsize"

    spawnUnits = "spawnUnits"
    initialtime = "initialtime"
    periodtime = "periodtime"


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
            AUTOKEY.operation_type: AUTOKEY.typeset, 
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

def operation_if(condition:str, tag:str, elseif_num:int = 1):
    return [
        {
            AUTOKEY.operation_type: AUTOKEY.typeif, 
            AUTOKEY.ifvar: condition, 
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

def operation_pdb():
    return [
        {
            AUTOKEY.operation_type: AUTOKEY.pdb_pause
        }
    ]

def operation_error(error_info:str):
    return [
        {
            AUTOKEY.operation_type: AUTOKEY.error, 
            AUTOKEY.error_info: error_info
        }
    ]

def operation_typeset_expression(key:str, value:str, depth:int = MAXTRANSDEPTH):
    return [
        {
            AUTOKEY.operation_type:AUTOKEY.typeset_expression, 
            AUTOKEY.depth:depth, 
            key: value
        }
    ]

BRACE_OPERATION_END = \
    operation_exist_if(f"{INFOKEY.brace}", "brace_operation_if_1") + \
        operation_cycle_start("i", "0", f"i < len({INFOKEY.brace})", "brace_operation_cycle_1") + \
            operation_typeset_expression("{" + f"{INFOKEY.brace}[i]" + "}", "{" + f"{INFOKEY.brace}[i]" + "}") + \
        operation_cycle_end("i", "i + 1", "brace_operation_cycle_1") + \
    operation_ifend("brace_operation_if_1")