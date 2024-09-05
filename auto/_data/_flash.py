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

flash_info_args_dict = OrderedDict()

flash_info_args_dict[INFOKEY.prefix] = str
flash_info_args_dict[INFOKEY.idprefix] = str
flash_info_args_dict[INFOKEY.detectReset] = str
flash_info_args_dict[INFOKEY.isprefixseg] = bool
flash_info_args_dict[INFOKEY.initialtime] = (list, str)
flash_info_args_dict[INFOKEY.periodtime] = (list, str)

flash_info_args_dict[INFOKEY.cite_name] = str

flash_info_args_dict[INFOKEY.args] = (list, list, str)
flash_info_args_dict[INFOKEY.opargs] = (list, list, str)
flash_info_args_dict[INFOKEY.brace] = (list, str)

flash_info_default_args_dict = {
    INFOKEY.detectReset: '0.25s'
}

flash_info_optional_set = {
    INFOKEY.isprefixseg, INFOKEY.args, INFOKEY.opargs, INFOKEY.cite_name, 
    INFOKEY.brace, INFOKEY.periodtime
}

flash_info_var_dependent_dict = {}

flash_info_initial_brace_dict = {}

flash_info_default_brace_set = set()

flash_info_operation_pre_list = \
    deepcopy(ARGS_OPARGS_PRE_OPERATION)

flash_info_operation_list = \
    operation_cycle_start("i", "0", f"i < len({INFOKEY.initialtime})", "flash_cycle_initialtime_add") + \
        [
            {
                AUTOKEY.operation_type: AUTOKEY.object, 
                AUTOKEY.type: rw.const.OBJECTTYPE.unitAdd, 
                AUTOKEY.optional: {
                    rw.const.OBJECTOP.warmup: "{" + f"{INFOKEY.initialtime}[i]" + "}", 
                    rw.const.OBJECTOP.spawnUnits: "antiAirTurretFlak*1", 
                    rw.const.OBJECTOP.team: "-2", 
                }
            }
        ] + \
    operation_cycle_end("i", "i + 1", "flash_cycle_initialtime_add") + \
    operation_exist_if(INFOKEY.periodtime, "flash_existif_periodtime_add") + \
        operation_cycle_start("i", "0", f"i < len({INFOKEY.periodtime})", "flash_cycle_periodtime_add") + \
            [
                {
                    AUTOKEY.operation_type: AUTOKEY.object, 
                    AUTOKEY.type: rw.const.OBJECTTYPE.unitAdd, 
                    AUTOKEY.optional: {
                        rw.const.OBJECTOP.warmup: "{" + f"int({INFOKEY.initialtime}[len({INFOKEY.initialtime}) - 1][:-1]) + int({INFOKEY.periodtime}[i][:-1])" + "}s", 
                        rw.const.OBJECTOP.resetActivationAfter: "{" + f"{INFOKEY.periodtime}[len({INFOKEY.periodtime}) - 1]" + "}", 
                        rw.const.OBJECTOP.spawnUnits: "antiAirTurretFlak*1", 
                        rw.const.OBJECTOP.team: "-2", 
                    }
                }
            ] + \
        operation_cycle_end("i", "i + 1", "flash_cycle_periodtime_add") + \
    operation_ifend("flash_existif_periodtime_add") + \
    [
        {
            AUTOKEY.operation_type: AUTOKEY.object, 
            AUTOKEY.type: rw.const.OBJECTTYPE.unitDetect, 
            AUTOKEY.optional: {
                rw.const.OBJECTOP.resetActivationAfter: "{" + f"{INFOKEY.detectReset}" + "}", 
                rw.const.OBJECTOP.id: "{" + f"{INFOKEY.idprefix}" + "0}", 
                rw.const.OBJECTOP.maxUnits: "0", 
            }
        }
    ] + \
    operation_cycle_start("i", "0", f"i < len({INFOKEY.initialtime})", "flash_cycle_initialtime_remove") + \
        [
            {
                AUTOKEY.operation_type: AUTOKEY.object, 
                AUTOKEY.type: rw.const.OBJECTTYPE.unitRemove, 
                AUTOKEY.optional: {
                    rw.const.OBJECTOP.warmup: "{" + f"{INFOKEY.initialtime}[i]" + "}", 
                }
            }
        ] + \
    operation_cycle_end("i", "i + 1", "flash_cycle_initialtime_remove") + \
    operation_exist_if(INFOKEY.periodtime, "flash_existif_periodtime_remove") + \
        operation_cycle_start("i", "0", f"i < len({INFOKEY.periodtime})", "flash_cycle_periodtime_remove") + \
            [
                {
                    AUTOKEY.operation_type: AUTOKEY.object, 
                    AUTOKEY.type: rw.const.OBJECTTYPE.unitRemove, 
                    AUTOKEY.optional: {
                        rw.const.OBJECTOP.warmup: "{" + f"int({INFOKEY.initialtime}[len({INFOKEY.initialtime}) - 1][:-1]) + int({INFOKEY.periodtime}[i][:-1])" + "}s", 
                        rw.const.OBJECTOP.resetActivationAfter: "{" + f"{INFOKEY.periodtime}[len({INFOKEY.periodtime}) - 1]" + "}", 
                    }
                }
            ] + \
        operation_cycle_end("i", "i + 1", "flash_cycle_periodtime_remove") + \
    operation_ifend("flash_existif_periodtime_remove") + \
    BRACE_OPERATION_END

flash_info = {
    INFOKEY.flash_info:{
        AUTOKEY.info_args:flash_info_args_dict, 
        AUTOKEY.default_args: flash_info_default_args_dict, 
        AUTOKEY.var_dependent: flash_info_var_dependent_dict, 
        AUTOKEY.optional:flash_info_optional_set, 
        AUTOKEY.initial_brace: flash_info_initial_brace_dict, 
        AUTOKEY.default_brace: flash_info_default_brace_set, 

        AUTOKEY.ids: [[INFOKEY.idprefix, 1]], 
        AUTOKEY.prefix: AUTOKEY.prefix, 
        AUTOKEY.isprefixseg: AUTOKEY.isprefixseg, 
        AUTOKEY.args: [], 
        AUTOKEY.seg: ".", 
        AUTOKEY.opargs_prefix_len:1, 
        AUTOKEY.opargs: {}, 
        AUTOKEY.opargs_seg: ",", 
        AUTOKEY.operation_pre:flash_info_operation_pre_list, 
        AUTOKEY.operation:flash_info_operation_list, 
        AUTOKEY.no_check: True
    }
}