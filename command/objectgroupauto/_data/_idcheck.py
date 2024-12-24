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
from command.objectgroupauto._data._mtext import *
from command.objectgroupauto._data._time import *

idcheck_info_args_dict = OrderedDict()

idcheck_info_args_dict[INFOKEY.prefix] = str
idcheck_info_args_dict[INFOKEY.idprefix] = str
idcheck_info_args_dict[INFOKEY.otherid] = str

idcheck_info_args_dict[INFOKEY.detectReset] = str
idcheck_info_args_dict[INFOKEY.removeReset] = str
idcheck_info_args_dict[INFOKEY.addWarmup] = str
idcheck_info_args_dict[INFOKEY.addReset] = str
idcheck_info_args_dict[INFOKEY.isprefixseg] = bool
idcheck_info_args_dict[INFOKEY.aunit] = str
idcheck_info_args_dict[INFOKEY.spawnnum] = str
idcheck_info_args_dict[INFOKEY.team] = str

idcheck_info_args_dict[INFOKEY.addname] = str
idcheck_info_args_dict[INFOKEY.detectname] = str
idcheck_info_args_dict[INFOKEY.removename] = str
idcheck_info_args_dict[INFOKEY.offset] = (list, int)
idcheck_info_args_dict[INFOKEY.offsetsize] = (list, int)

idcheck_info_args_dict[INFOKEY.mtext_prefix] = str

idcheck_info_args_dict[INFOKEY.cite_name] = str

idcheck_info_default_args_dict = {
    INFOKEY.addReset: "0.25s", 
    INFOKEY.detectReset: "0.25s", 
    INFOKEY.removeReset: "0.25s", 
    INFOKEY.addWarmup: "0s", 
    INFOKEY.aunit : "antiAirTurretFlak", 
    INFOKEY.team: "-2", 
    INFOKEY.spawnnum: "1", 
    INFOKEY.addname: "", 
    INFOKEY.detectname: "", 
    INFOKEY.removename: "", 
    INFOKEY.offset: "0 0", 
    INFOKEY.offsetsize: "0 0", 
}

idcheck_info_optional_set = {
    INFOKEY.isprefixseg, 
    INFOKEY.cite_name, 
}

idcheck_info_var_dependent_dict = {}
#

idcheck_info_initial_brace_dict = {}

idcheck_info_default_brace_set = set()

idcheck_info_operation_pre_list = []

idcheck_info_info_prefix_dict = {}

idcheck_info_operation_list = \
    [
        {
            AUTOKEY.operation_type: AUTOKEY.object, 
            AUTOKEY.offset: f"{INFOKEY.offset}", 
            AUTOKEY.offsetsize: f"{INFOKEY.offsetsize}", 
            AUTOKEY.name: "{" + f"{INFOKEY.detectname}" + "}", 
            AUTOKEY.type: rw.const.OBJECTTYPE.unitDetect, 
            AUTOKEY.optional: {
                rw.const.OBJECTOP.resetActivationAfter: "{" + f"{INFOKEY.detectReset}" + "}", 
                rw.const.OBJECTOP.id: "{" + f"{INFOKEY.idprefix}" + "0}", 
                rw.const.OBJECTOP.maxUnits: "0", 
            }
        }
    ] + \
    [
        {
            AUTOKEY.operation_type: AUTOKEY.object, 
            AUTOKEY.offset: f"{INFOKEY.offset}", 
            AUTOKEY.offsetsize: f"{INFOKEY.offsetsize}", 
            AUTOKEY.name: "{" + f"{INFOKEY.addname}" + "}", 
            AUTOKEY.type: rw.const.OBJECTTYPE.unitAdd, 
            AUTOKEY.optional: {
                rw.const.OBJECTOP.activatedBy: "{" + f"{INFOKEY.idprefix}" + "0},{" + f"{INFOKEY.otherid}" + "}", 
                rw.const.OBJECTOP.allToActivate: True, 
                rw.const.OBJECTOP.warmup: ("{" + f"{INFOKEY.addWarmup}" + "}", f"'{INFOKEY.addWarmup}' != '0s'", AUTOKEY.brace), 
                rw.const.OBJECTOP.resetActivationAfter: "{" + f"{INFOKEY.addReset}" + "}", 
                rw.const.OBJECTOP.spawnUnits: "{" + f"{INFOKEY.aunit}" + "}*{" + f"{INFOKEY.spawnnum}" + "}", 
                rw.const.OBJECTOP.team: "{" + f"{INFOKEY.team}" + "}", 
            }
        }
    ] + \
    [
        {
            AUTOKEY.operation_type: AUTOKEY.object, 
            AUTOKEY.offset: f"{INFOKEY.offset}", 
            AUTOKEY.offsetsize: f"{INFOKEY.offsetsize}", 
            AUTOKEY.name: "{" + f"{INFOKEY.addname}" + "}", 
            AUTOKEY.type: rw.const.OBJECTTYPE.unitRemove, 
            AUTOKEY.optional: {
                rw.const.OBJECTOP.deactivatedBy: "{" + f"{INFOKEY.otherid}" + "}", 
                rw.const.OBJECTOP.resetActivationAfter: "{" + f"{INFOKEY.removeReset}" + "}", 
            }
        }
    ]

idcheck_info = {
    INFOKEY.idcheck_info:{
        AUTOKEY.info_args:idcheck_info_args_dict, 
        AUTOKEY.default_args: idcheck_info_default_args_dict, 
        AUTOKEY.var_dependent: idcheck_info_var_dependent_dict, 
        AUTOKEY.optional:idcheck_info_optional_set, 
        AUTOKEY.initial_brace: idcheck_info_initial_brace_dict, 
        AUTOKEY.default_brace: idcheck_info_default_brace_set, 
        AUTOKEY.info_prefix: idcheck_info_info_prefix_dict, 

        AUTOKEY.ids: [[INFOKEY.idprefix, 1]], 
        AUTOKEY.prefix: AUTOKEY.prefix, 
        AUTOKEY.isprefixseg: AUTOKEY.isprefixseg, 
        AUTOKEY.args: [], 
        AUTOKEY.seg: ".", 
        AUTOKEY.opargs_prefix_len:1, 
        AUTOKEY.opargs: {}, 
        AUTOKEY.opargs_seg: ",", 
        AUTOKEY.operation_pre:idcheck_info_operation_pre_list, 
        AUTOKEY.operation:idcheck_info_operation_list, 
        AUTOKEY.no_check: True
    }
}

idcheck_info = mtext_info_sub(idcheck_info)
idcheck_info = time_info_sub(idcheck_info, [INFOKEY.addWarmup], [], [], [])
idcheck_info = brace_add_info(idcheck_info)
idcheck_info = args_opargs_add_info(idcheck_info)