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

from auto._core import AUTOKEY
from auto._data._const import *
from auto._data._object import *

inadd_info_args_dict = OrderedDict()

inadd_info_args_dict[INFOKEY.isinadd] = bool
inadd_info_args_dict[INFOKEY.prefix] = str
inadd_info_args_dict[INFOKEY.inaddunit] = str
inadd_info_args_dict[INFOKEY.inaddspawnnum] = str
inadd_info_args_dict[INFOKEY.inaddteam] = str
inadd_info_args_dict[INFOKEY.inaddwarmup] = str
inadd_info_args_dict[INFOKEY.inaddisshowOnMap] = bool
inadd_info_args_dict[INFOKEY.inaddname] = str
inadd_info_args_dict[INFOKEY.inaddoffset] = (list, int)
inadd_info_args_dict[INFOKEY.inaddoffsetsize] = (list, int)

inadd_info_default_args_dict = {
    INFOKEY.isinadd: "true", 
    INFOKEY.inaddspawnnum: "1", 
    INFOKEY.inaddwarmup: "{" + f"{INFOKEY.addWarmup}" + "}", 
    INFOKEY.inaddunit: "{" + f"{INFOKEY.unit}" + "}", 
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
}

inadd_info_optional_set = {
    INFOKEY.isinadd, INFOKEY.inaddname, INFOKEY.inaddisshowOnMap, INFOKEY.inaddspawnnum, 
    INFOKEY.inaddoffset, INFOKEY.inaddoffsetsize
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
                AUTOKEY.optional: {
                    rw.const.OBJECTOP.spawnUnits: "{" + f"{INFOKEY.unit}" + "}*{" + f"{INFOKEY.inaddspawnnum}" + "}", 
                    rw.const.OBJECTOP.team: "{" + f"{INFOKEY.inaddteam}" + "}", 
                    rw.const.OBJECTOP.warmup: "{" + f"{INFOKEY.inaddwarmup}" + "}", 
                    rw.const.OBJECTOP.showOnMap: (True, f"{INFOKEY.inaddisshowOnMap}", AUTOKEY.brace), 
                }
            }
        ] + \
    operation_ifend("inadd_if_isinadd")



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