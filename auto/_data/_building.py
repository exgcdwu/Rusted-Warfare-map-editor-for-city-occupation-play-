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
from auto._data._bdtext import *
from auto._data._inadd import *

building_info_args_dict = OrderedDict()

building_info_args_dict[INFOKEY.prefix] = str
building_info_args_dict[INFOKEY.idprefix] = str
building_info_args_dict[INFOKEY.isprefixseg] = bool
building_info_args_dict[INFOKEY.detectReset] = str
building_info_args_dict[INFOKEY.addWarmup] = str
building_info_args_dict[INFOKEY.addReset] = str

building_info_args_dict[INFOKEY.unit] = str
building_info_args_dict[INFOKEY.spawnnum] = str
building_info_args_dict[INFOKEY.team] = str
building_info_args_dict[INFOKEY.addname] = str
building_info_args_dict[INFOKEY.addoffset] = (list, int)
building_info_args_dict[INFOKEY.addoffsetsize] = (list, int)
building_info_args_dict[INFOKEY.detectname] = str
building_info_args_dict[INFOKEY.detectoffset] = (list, int)
building_info_args_dict[INFOKEY.detectoffsetsize] = (list, int)

building_info_args_dict[INFOKEY.inadd_prefix] = str
building_info_args_dict[INFOKEY.bdtext_prefix] = str
building_info_args_dict[INFOKEY.acti] = (list, str)
building_info_args_dict[INFOKEY.deacti] = (list, str)
building_info_args_dict[INFOKEY.isonlybuilding] = bool
building_info_args_dict[INFOKEY.isshowOnMap] = bool
building_info_args_dict[INFOKEY.minUnits] = str
building_info_args_dict[INFOKEY.maxUnits] = str

building_info_args_dict[INFOKEY.cite_name] = str

building_info_args_dict[INFOKEY.args] = (list, list, str)
building_info_args_dict[INFOKEY.opargs] = (list, list, str)
building_info_args_dict[INFOKEY.brace] = (list, str)

building_info_args_dict.update(bdtext_info_args_dict)
building_info_args_dict.update(inadd_info_args_dict)

building_info_default_args_dict = {
    INFOKEY.isonlybuilding: "false", 
    INFOKEY.team: "-1", 
    INFOKEY.maxUnits: "0", 
    INFOKEY.spawnnum: "1", 
    INFOKEY.addname: "", 
    INFOKEY.addoffset: "0 0", 
    INFOKEY.addoffsetsize: "0 0", 
    INFOKEY.detectname: "", 
    INFOKEY.detectoffset: "0 0", 
    INFOKEY.detectoffsetsize: "0 0", 
    INFOKEY.acti: "", 
}
building_info_default_args_dict.update(bdtext_info_default_args_dict)
building_info_default_args_dict.update(inadd_info_default_args_dict)
building_info_default_args_dict[f"{INFOKEY.isbdtext}"] = "false"
building_info_default_args_dict[f"{INFOKEY.isinadd}"] = "false"

building_info_optional_set = {
    INFOKEY.isprefixseg, INFOKEY.minUnits, INFOKEY.args, INFOKEY.opargs, 
    INFOKEY.inadd_prefix, INFOKEY.bdtext_prefix, INFOKEY.isonlybuilding, 
    INFOKEY.isshowOnMap, INFOKEY.cite_name, INFOKEY.brace, INFOKEY.deacti, 
}

building_info_optional_set.update(bdtext_info_optional_set)
building_info_optional_set.update(inadd_info_optional_set)

building_info_var_dependent_dict = {}
building_info_var_dependent_dict.update(bdtext_info_var_dependent_dict)
building_info_var_dependent_dict.update(inadd_info_var_dependent_dict)
#

building_info_initial_brace_dict = {}

building_info_default_brace_set = set()

building_info_operation_pre_list = deepcopy(ARGS_OPARGS_PRE_OPERATION)

building_info_info_prefix_dict = {
    INFOKEY.bdtext_info: INFOKEY.bdtext_prefix, 
    INFOKEY.inadd_info: INFOKEY.inadd_prefix
}

building_info_operation_list = \
    bdtext_info_operation_list + \
    inadd_info_operation_list + \
    [
        {
            AUTOKEY.operation_type: AUTOKEY.object, 
            AUTOKEY.offset: f"{INFOKEY.detectoffset}", 
            AUTOKEY.offsetsize: f"{INFOKEY.detectoffsetsize}", 
            AUTOKEY.name: "{" + f"{INFOKEY.detectname}" + "}", 
            AUTOKEY.type: rw.const.OBJECTTYPE.unitDetect, 
            AUTOKEY.optional: {
                rw.const.OBJECTOP.resetActivationAfter: "{" + f"{INFOKEY.detectReset}" + "}", 
                rw.const.OBJECTOP.unitType: ("{" + f"{INFOKEY.unit}" + "}", f"{INFOKEY.isonlybuilding} == False", AUTOKEY.brace), 
                rw.const.OBJECTOP.team: ("{" + f"{INFOKEY.team}" + "}", f"{INFOKEY.team} != -1", AUTOKEY.brace), 
                rw.const.OBJECTOP.id: "{" + f"{INFOKEY.idprefix}" + "0}", 
                rw.const.OBJECTOP.onlyBuildings: ("{" + f"{INFOKEY.isonlybuilding}" + "}", f"{INFOKEY.isonlybuilding}", AUTOKEY.brace), 
                rw.const.OBJECTOP.minUnits: ("{" + f"{INFOKEY.minUnits}" + "}", f"{INFOKEY.minUnits}", AUTOKEY.exist), 
                rw.const.OBJECTOP.maxUnits: ("{" + f"{INFOKEY.maxUnits}" + "}", f"{INFOKEY.maxUnits}", AUTOKEY.exist), 
            }
        }
    ] + \
    [
        {
            AUTOKEY.operation_type: AUTOKEY.object, 
            AUTOKEY.offset: f"{INFOKEY.addoffset}", 
            AUTOKEY.offsetsize: f"{INFOKEY.addoffsetsize}", 
            AUTOKEY.name: "{" + f"{INFOKEY.addname}" + "}", 
            AUTOKEY.type: rw.const.OBJECTTYPE.unitAdd, 
            AUTOKEY.optional: {
                rw.const.OBJECTOP.activatedBy: "{" + f"{INFOKEY.idprefix}" + "0}{',' + ','.join(acti) if acti != [''] else ''}", 
                rw.const.OBJECTOP.deactivatedBy: ("{','.join(deacti)}", f"{INFOKEY.deacti}", AUTOKEY.exist), 
                rw.const.OBJECTOP.warmup: "{" + f"{INFOKEY.addWarmup}" + "}", 
                rw.const.OBJECTOP.resetActivationAfter: ("{" + f"{INFOKEY.addReset}" + "}", f"{INFOKEY.addReset}", AUTOKEY.exist), 
                rw.const.OBJECTOP.spawnUnits: "{" + f"{INFOKEY.unit}" + "}*{" + f"{INFOKEY.spawnnum}" + "}", 
                rw.const.OBJECTOP.team: "{" + f"{INFOKEY.team}" + "}", 
                rw.const.OBJECTOP.showOnMap: (True, f"{INFOKEY.isshowOnMap}", AUTOKEY.brace), 
            }
        }
    ] + \
    BRACE_OPERATION_END

building_info = {
    INFOKEY.building_info:{
        AUTOKEY.info_args:building_info_args_dict, 
        AUTOKEY.default_args: building_info_default_args_dict, 
        AUTOKEY.var_dependent: building_info_var_dependent_dict, 
        AUTOKEY.optional:building_info_optional_set, 
        AUTOKEY.initial_brace: building_info_initial_brace_dict, 
        AUTOKEY.default_brace: building_info_default_brace_set, 
        AUTOKEY.info_prefix: building_info_info_prefix_dict, 

        AUTOKEY.ids: [[INFOKEY.idprefix, 1]], 
        AUTOKEY.prefix: AUTOKEY.prefix, 
        AUTOKEY.isprefixseg: AUTOKEY.isprefixseg, 
        AUTOKEY.args: [], 
        AUTOKEY.seg: ".", 
        AUTOKEY.opargs_prefix_len:1, 
        AUTOKEY.opargs: {}, 
        AUTOKEY.opargs_seg: ",", 
        AUTOKEY.operation_pre:building_info_operation_pre_list, 
        AUTOKEY.operation:building_info_operation_list, 
        AUTOKEY.no_check: True
    }
}