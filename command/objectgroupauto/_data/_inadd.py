import os
import sys
from collections import OrderedDict
from copy import deepcopy
current_file_path = os.path.abspath(__file__)
current_dir_path = os.path.dirname(current_file_path)
auto_dir_path = os.path.dirname(current_dir_path)
package_dir = os.path.dirname(auto_dir_path)
sys.path.append(package_dir)
import rwmap as rw

from command.objectgroupauto._core import AUTOKEY
from command.objectgroupauto._data._const import *
from command.objectgroupauto._data._object import *

inadd_info_args_dict = OrderedDict()

inadd_info_args_dict[INFOKEY.isinadd] = bool
inadd_info_args_dict[INFOKEY.prefix] = str
inadd_info_args_dict[INFOKEY.inaddunit] = str
inadd_info_args_dict[INFOKEY.inaddisinitialunit] = bool
inadd_info_args_dict[INFOKEY.inaddspawnnum] = str
inadd_info_args_dict[INFOKEY.inaddteam] = str
inadd_info_args_dict[INFOKEY.inaddaunitbrace] = str
inadd_info_args_dict[INFOKEY.inaddwarmup] = str
inadd_info_args_dict[INFOKEY.inaddisshowOnMap] = bool
inadd_info_args_dict[INFOKEY.inaddname] = str
inadd_info_args_dict[INFOKEY.inaddoffset] = (list, int)
inadd_info_args_dict[INFOKEY.inaddoffsetsize] = (list, int)

inadd_info_default_args_dict = {
    INFOKEY.isinadd: "true", 
    INFOKEY.inaddisinitialunit: "false", 
    INFOKEY.inaddspawnnum: "1", 
    INFOKEY.inaddwarmup: "{" + f"{INFOKEY.addWarmup}" + "}", 
    INFOKEY.inaddunit: "{" + f"{INFOKEY.aunit}" + "}", 
    INFOKEY.inaddaunitbrace: "{" + f"{INFOKEY.aunitbrace}" + "}",
    INFOKEY.inaddname: "", 
    INFOKEY.inaddoffset: "0 0", 
    INFOKEY.inaddoffsetsize: "0 0"
}

inadd_info_var_dependent_dict = {
    INFOKEY.inaddunit: INFOKEY.isinadd, 
    INFOKEY.inaddspawnnum: INFOKEY.isinadd, 
    INFOKEY.inaddteam: INFOKEY.isinadd, 
    INFOKEY.inaddwarmup: INFOKEY.isinadd, 
    INFOKEY.inaddisshowOnMap: INFOKEY.isinadd, 
    INFOKEY.inaddname: INFOKEY.isinadd, 
    INFOKEY.inaddoffset: INFOKEY.isinadd, 
    INFOKEY.inaddoffsetsize: INFOKEY.isinadd, 
    INFOKEY.inaddisinitialunit: INFOKEY.isinadd, 
    INFOKEY.inaddaunitbrace: INFOKEY.isinadd
}

inadd_info_optional_set = {
    INFOKEY.isinadd, INFOKEY.inaddname, INFOKEY.inaddisshowOnMap, INFOKEY.inaddspawnnum, 
    INFOKEY.inaddoffset, INFOKEY.inaddoffsetsize, INFOKEY.inaddaunitbrace
}

inadd_info_operation_list = \
    operation_if(INFOKEY.isinadd, "inadd_if_isinadd") + \
        [
            {
                AUTOKEY.operation_type: AUTOKEY.object, 
                AUTOKEY.offset: f"{INFOKEY.inaddoffset}", 
                AUTOKEY.offsetsize: f"{INFOKEY.inaddoffsetsize}", 
                AUTOKEY.name: "{" + f"{INFOKEY.inaddname}" + "}", 
                AUTOKEY.type: rw.const.OBJECTTYPE.unitAdd, 
                AUTOKEY.objectGroup_name: (rw.const.NAME.UnitObject, f"{INFOKEY.inaddisinitialunit}", AUTOKEY.brace), 
                AUTOKEY.optional: {
                    rw.const.OBJECTOP.spawnUnits: (br(f"{INFOKEY.inaddunit}") + "*" + br(f"{INFOKEY.inaddspawnnum}") + br(f"{INFOKEY.inaddaunitbrace}"), f"not {INFOKEY.inaddisinitialunit}", AUTOKEY.brace), 
                    rw.const.OBJECTOP.unit: ("{" + f"{INFOKEY.inaddunit}" + "}", f"{INFOKEY.inaddisinitialunit}", AUTOKEY.brace), 
                    rw.const.OBJECTOP.team: "{" + f"{INFOKEY.inaddteam}" + "}", 
                    rw.const.OBJECTOP.warmup: ("{" + f"{INFOKEY.inaddwarmup}" + "}", f"('{INFOKEY.inaddwarmup}' != '0s' and '{INFOKEY.inaddwarmup}' != '0.0s') and not({INFOKEY.inaddisinitialunit})", AUTOKEY.brace), 
                    rw.const.OBJECTOP.showOnMap: (True, f"{INFOKEY.inaddisshowOnMap} and not({INFOKEY.inaddisinitialunit})", AUTOKEY.brace), 
                }
            }
        ] + \
    operation_ifend("inadd_if_isinadd")

def inadd_info_sub(info_dict:str)->dict:
    info_dict_ans = deepcopy(info_dict)
    for key, value in info_dict_ans.items():
        value[AUTOKEY.info_args].update(inadd_info_args_dict)
        value[AUTOKEY.info_args][INFOKEY.inadd_prefix] = str
        if value.get(AUTOKEY.operation) == None:
            value[AUTOKEY.operation] = []
        value[AUTOKEY.operation] = inadd_info_operation_list + value[AUTOKEY.operation]
        if value.get(AUTOKEY.default_args) == None:
            value[AUTOKEY.default_args] = {}
        value[AUTOKEY.default_args].update(inadd_info_default_args_dict)
        value[AUTOKEY.default_args][INFOKEY.isinadd] = "false"
        if value.get(AUTOKEY.var_dependent) == None:
            value[AUTOKEY.var_dependent] = {}
        value[AUTOKEY.var_dependent].update(inadd_info_var_dependent_dict)
        if value.get(AUTOKEY.optional) == None:
            value[AUTOKEY.optional] = set()
        value[AUTOKEY.optional].update(inadd_info_optional_set)
        value[AUTOKEY.optional].update({INFOKEY.inadd_prefix,})
        if value.get(AUTOKEY.info_prefix) == None:
            value[AUTOKEY.info_prefix] = {}
        value[AUTOKEY.info_prefix].update({INFOKEY.inadd_info: INFOKEY.inadd_prefix})
    return info_dict_ans

inadd_info = {
    INFOKEY.inadd_info:{
        AUTOKEY.info_args:inadd_info_args_dict, 
        AUTOKEY.default_args:inadd_info_default_args_dict, 
        AUTOKEY.optional: inadd_info_optional_set, 
        AUTOKEY.prefix: INFOKEY.prefix, 
        AUTOKEY.isinfo_sub: True, 
        AUTOKEY.no_check: True
    }
}