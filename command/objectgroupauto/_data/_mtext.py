import os
import sys
from collections import OrderedDict
current_file_path = os.path.abspath(__file__)
current_dir_path = os.path.dirname(current_file_path)
auto_dir_path = os.path.dirname(current_dir_path)
package_dir = os.path.dirname(auto_dir_path)
sys.path.append(package_dir)
import rwmap as rw
from copy import deepcopy

from command.objectgroupauto._core import AUTOKEY
from command.objectgroupauto._data._const import *
from command.objectgroupauto._data._object import *

mtext_info_args_dict = OrderedDict()

mtext_info_args_dict[INFOKEY.prefix] = str
mtext_info_args_dict[INFOKEY.ismtext] = bool
mtext_info_args_dict[INFOKEY.mcolor] = str
mtext_info_args_dict[INFOKEY.mtextsize] = str
mtext_info_args_dict[INFOKEY.mtext] = str
mtext_info_args_dict[INFOKEY.mname] = str
mtext_info_args_dict[INFOKEY.moffset] = (list, int)
mtext_info_args_dict[INFOKEY.moffsetsize] = (list, int)
mtext_info_args_dict[INFOKEY.mgset] = (list, int)
mtext_info_args_dict[INFOKEY.mgsetsize] = (list, int)
mtext_info_args_dict[INFOKEY.malsoActivate] = str
mtext_info_args_dict[INFOKEY.mid] = str
mtext_info_args_dict[INFOKEY.mglobalMessage] = str
mtext_info_args_dict[INFOKEY.mglobalMessage_delayPerChar] = str
mtext_info_args_dict[INFOKEY.mglobalMessage_textColor] = str
mtext_info_args_dict[INFOKEY.mdebugMessage] = str
mtext_info_args_dict[INFOKEY.mallToActivate] = bool
mtext_info_args_dict[INFOKEY.mshowOnMap] = bool

mtext_info_default_args_dict = {
    INFOKEY.ismtext: "true",  
    INFOKEY.mname: "", 
    INFOKEY.moffset: "0 0", 
    INFOKEY.moffsetsize: "0 0"
}

mtext_info_var_dependent_dict = {
    INFOKEY.mcolor: INFOKEY.ismtext, 
    INFOKEY.mtextsize: INFOKEY.ismtext, 
    INFOKEY.mname: INFOKEY.ismtext, 
    INFOKEY.moffset: INFOKEY.ismtext, 
    INFOKEY.moffsetsize: INFOKEY.ismtext, 
    INFOKEY.mgset: INFOKEY.ismtext, 
    INFOKEY.mgsetsize: INFOKEY.ismtext, 
    INFOKEY.mtext: INFOKEY.ismtext, 
    INFOKEY.malsoActivate: INFOKEY.ismtext, 
    INFOKEY.mid: INFOKEY.ismtext, 
    INFOKEY.mglobalMessage: INFOKEY.ismtext, 
    INFOKEY.mglobalMessage_delayPerChar: INFOKEY.ismtext, 
    INFOKEY.mglobalMessage_textColor: INFOKEY.ismtext, 
    INFOKEY.mdebugMessage: INFOKEY.ismtext, 
    INFOKEY.mallToActivate: INFOKEY.ismtext, 
    INFOKEY.mshowOnMap: INFOKEY.ismtext
}

mtext_info_optional_set = {
    INFOKEY.ismtext, INFOKEY.mcolor, INFOKEY.mtextsize, INFOKEY.mname, 
    INFOKEY.moffset, INFOKEY.moffsetsize, INFOKEY.mgset, INFOKEY.mgsetsize, 
    INFOKEY.malsoActivate, INFOKEY.mid, INFOKEY.mglobalMessage, 
    INFOKEY.mglobalMessage_delayPerChar, INFOKEY.mglobalMessage_textColor, 
    INFOKEY.mdebugMessage, INFOKEY.mallToActivate, INFOKEY.mshowOnMap
}

mtext_info_operation_list = \
    operation_if(INFOKEY.ismtext, "mtext_if_ismtext") + \
        [
            {
                AUTOKEY.operation_type: AUTOKEY.object, 
                AUTOKEY.offset: f"{INFOKEY.moffset}", 
                AUTOKEY.offsetsize: f"{INFOKEY.moffsetsize}", 
                AUTOKEY.set_key: f"{INFOKEY.mgset}", 
                AUTOKEY.setsize_key: f"{INFOKEY.mgsetsize}", 
                AUTOKEY.name: "{" + f"{INFOKEY.mname}" + "}", 
                AUTOKEY.type: rw.const.OBJECTTYPE.mapText, 
                AUTOKEY.optional: {
                    rw.const.OBJECTOP.text: "{" + f"{INFOKEY.mtext}" + "}", 
                    rw.const.OBJECTOP.textColor: ("{" + f"{INFOKEY.mcolor}" + "}", "mcolor", AUTOKEY.exist), 
                    rw.const.OBJECTOP.textSize: ("{" + f"{INFOKEY.mtextsize}" + "}", "mtextsize", AUTOKEY.exist), 
                    rw.const.OBJECTOP.alsoActivate: ("{" + f"{INFOKEY.malsoActivate}" + "}", f"{INFOKEY.malsoActivate}", AUTOKEY.exist), 
                    rw.const.OBJECTOP.id: ("{" + f"{INFOKEY.mid}" + "}", f"{INFOKEY.mid}", AUTOKEY.exist), 
                    rw.const.OBJECTOP.globalMessage: ("{" + f"{INFOKEY.mglobalMessage}" + "}", f"{INFOKEY.mglobalMessage}", AUTOKEY.exist), 
                    rw.const.OBJECTOP.globalMessage_delayPerChar: ("{" + f"{INFOKEY.mglobalMessage_delayPerChar}" + "}", f"{INFOKEY.mglobalMessage_delayPerChar}", AUTOKEY.exist), 
                    rw.const.OBJECTOP.globalMessage_textColor: ("{" + f"{INFOKEY.mglobalMessage_textColor}" + "}", f"{INFOKEY.mglobalMessage_textColor}", AUTOKEY.exist), 
                    rw.const.OBJECTOP.debugMessage: ("{" + f"{INFOKEY.mdebugMessage}" + "}", f"{INFOKEY.mdebugMessage}", AUTOKEY.exist), 
                    rw.const.OBJECTOP.allToActivate: (True, f"{INFOKEY.mallToActivate}", AUTOKEY.brace), 
                    rw.const.OBJECTOP.showOnMap: (True, f"{INFOKEY.mshowOnMap}", AUTOKEY.brace), 
                }
            }
        ] + \
    operation_ifend("mtext_if_ismtext")

def mtext_info_sub(info_dict:str)->dict:
    info_dict_ans = deepcopy(info_dict)
    for key, value in info_dict_ans.items():
        value[AUTOKEY.info_args].update(mtext_info_args_dict)
        value[AUTOKEY.info_args][INFOKEY.mtext_prefix] = str
        if value.get(AUTOKEY.operation) == None:
            value[AUTOKEY.operation] = []
        value[AUTOKEY.operation] = mtext_info_operation_list + value[AUTOKEY.operation]
        if value.get(AUTOKEY.default_args) == None:
            value[AUTOKEY.default_args] = {}
        value[AUTOKEY.default_args].update(mtext_info_default_args_dict)
        value[AUTOKEY.default_args][INFOKEY.ismtext] = "false"
        if value.get(AUTOKEY.var_dependent) == None:
            value[AUTOKEY.var_dependent] = {}
        value[AUTOKEY.var_dependent].update(mtext_info_var_dependent_dict)
        if value.get(AUTOKEY.optional) == None:
            value[AUTOKEY.optional] = set()
        value[AUTOKEY.optional].update(mtext_info_optional_set)
        value[AUTOKEY.optional].update({INFOKEY.mtext_prefix,})
        if value.get(AUTOKEY.info_prefix) == None:
            value[AUTOKEY.info_prefix] = {}
        value[AUTOKEY.info_prefix].update({INFOKEY.mtext_info: INFOKEY.mtext_prefix})
    return info_dict_ans

mtext_info = {
    INFOKEY.mtext_info:{
        AUTOKEY.info_args:mtext_info_args_dict, 
        AUTOKEY.default_args:mtext_info_default_args_dict, 
        AUTOKEY.optional: mtext_info_optional_set, 
        AUTOKEY.prefix: INFOKEY.prefix, 
        AUTOKEY.isinfo_sub: True, 
    }
}