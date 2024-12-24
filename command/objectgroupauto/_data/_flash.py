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
from command.objectgroupauto._data._multiText import *
from command.objectgroupauto._data._time import *

flash_info_args_dict = OrderedDict()

flash_info_args_dict[INFOKEY.prefix] = str
flash_info_args_dict[INFOKEY.idprefix] = str
flash_info_args_dict[INFOKEY.detectReset] = str
flash_info_args_dict[INFOKEY.isprefixseg] = bool
flash_info_args_dict[INFOKEY.initialtime] = (list, str)
flash_info_args_dict[INFOKEY.periodtime] = (list, str)
flash_info_args_dict[INFOKEY.initialacti] = (list, list, str)
flash_info_args_dict[INFOKEY.initialdeacti] = (list, list, str)
flash_info_args_dict[INFOKEY.periodacti] = (list, list, str)
flash_info_args_dict[INFOKEY.perioddeacti] = (list, list, str)

flash_info_args_dict[INFOKEY.cite_name] = str

flash_info_default_args_dict = {
    INFOKEY.detectReset: '0.25s'
}

flash_info_optional_set = {
    INFOKEY.isprefixseg, INFOKEY.cite_name, INFOKEY.periodtime, INFOKEY.initialacti, INFOKEY.periodacti, 
    INFOKEY.initialdeacti, INFOKEY.perioddeacti
}
flash_info_optional_set.update(time_info_optional_set)

flash_info_var_dependent_dict = {}
flash_info_var_dependent_dict.update(time_info_var_dependent_dict)

flash_info_initial_brace_dict = {}

flash_info_default_brace_set = set()

flash_info_operation_pre_list = []

flash_info_info_prefix_dict = {}

flash_info_operation_list = \
    operation_cycle_start("i", "0", f"i < len({INFOKEY.initialtime})", "flash_cycle_initialtime_add") + \
        operation_list_assign(f"{INFOKEY.initialacti}", "i", "initialacti_now", "flash") + \
        operation_list_assign(f"{INFOKEY.initialdeacti}", "i", "initialdeacti_now", "flash") + \
        [
            {
                AUTOKEY.operation_type: AUTOKEY.object, 
                AUTOKEY.type: rw.const.OBJECTTYPE.unitAdd, 
                AUTOKEY.optional: {
                    rw.const.OBJECTOP.activatedBy: ("{','.join(initialacti_now)}", "initialacti_now_exist", AUTOKEY.brace), 
                    rw.const.OBJECTOP.deactivatedBy: ("{','.join(initialdeacti_now)}", "initialdeacti_now_exist", AUTOKEY.brace), 
                    rw.const.OBJECTOP.warmup: "{" + f"{INFOKEY.initialtime}[i]" + "}", 
                    rw.const.OBJECTOP.spawnUnits: "antiAirTurretFlak*1", 
                    rw.const.OBJECTOP.team: "-2", 
                }
            }
        ] + \
    operation_cycle_end("i", "i + 1", "flash_cycle_initialtime_add") + \
    operation_exist_if(INFOKEY.periodtime, "flash_existif_periodtime_add") + \
        operation_cycle_start("i", "0", f"i < len({INFOKEY.periodtime})", "flash_cycle_periodtime_add") + \
            operation_list_assign(f"{INFOKEY.periodacti}", "i", "periodacti_now", "flash") + \
            operation_list_assign(f"{INFOKEY.perioddeacti}", "i", "perioddeacti_now", "flash") + \
            [
                {
                    AUTOKEY.operation_type: AUTOKEY.object, 
                    AUTOKEY.type: rw.const.OBJECTTYPE.unitAdd, 
                    AUTOKEY.optional: {
                        rw.const.OBJECTOP.activatedBy: ("{','.join(periodacti_now)}", "periodacti_now_exist", AUTOKEY.brace), 
                        rw.const.OBJECTOP.deactivatedBy: ("{','.join(perioddeacti_now)}", "perioddeacti_now_exist", AUTOKEY.brace), 
                        rw.const.OBJECTOP.warmup: "{" + f"float({INFOKEY.initialtime}[len({INFOKEY.initialtime}) - 1][:-1]) + float({INFOKEY.periodtime}[i][:-1])" + "}s", 
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
                        rw.const.OBJECTOP.warmup: "{" + f"float({INFOKEY.initialtime}[len({INFOKEY.initialtime}) - 1][:-1]) + float({INFOKEY.periodtime}[i][:-1])" + "}s", 
                        rw.const.OBJECTOP.resetActivationAfter: "{" + f"{INFOKEY.periodtime}[len({INFOKEY.periodtime}) - 1]" + "}", 
                    }
                }
            ] + \
        operation_cycle_end("i", "i + 1", "flash_cycle_periodtime_remove") + \
    operation_ifend("flash_existif_periodtime_remove")

flash_info = {
    INFOKEY.flash_info:{
        AUTOKEY.info_args:flash_info_args_dict, 
        AUTOKEY.default_args: flash_info_default_args_dict, 
        AUTOKEY.var_dependent: flash_info_var_dependent_dict, 
        AUTOKEY.optional:flash_info_optional_set, 
        AUTOKEY.initial_brace: flash_info_initial_brace_dict, 
        AUTOKEY.default_brace: flash_info_default_brace_set, 
        AUTOKEY.info_prefix: flash_info_info_prefix_dict, 

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

flash_info = time_info_sub(flash_info, [], [INFOKEY.initialtime], [], [INFOKEY.periodtime])
flash_info = brace_add_info(flash_info)
flash_info = args_opargs_add_info(flash_info)