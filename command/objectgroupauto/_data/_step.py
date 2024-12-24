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

step_info_args_dict = OrderedDict()

step_info_args_dict[INFOKEY.prefix] = str
step_info_args_dict[INFOKEY.idprefix] = str
step_info_args_dict[INFOKEY.detectReset] = str
step_info_args_dict[INFOKEY.isprefixseg] = bool
step_info_args_dict[INFOKEY.steptime] = (list, str)
step_info_args_dict[INFOKEY.isactiend] = bool
step_info_args_dict[INFOKEY.stepacti] = (list, str)
step_info_args_dict[INFOKEY.stepdeacti] = (list, str)
step_info_args_dict[INFOKEY.aunit] = str
step_info_args_dict[INFOKEY.spawnnum] = str
step_info_args_dict[INFOKEY.team] = str

step_info_args_dict[INFOKEY.cite_name] = str

step_info_default_args_dict = {
    INFOKEY.detectReset: '0.25s', 
    INFOKEY.aunit : "antiAirTurretFlak", 
    INFOKEY.team: "-2", 
    INFOKEY.spawnnum: "1", 
}

step_info_optional_set = {
    INFOKEY.isprefixseg, INFOKEY.cite_name, INFOKEY.stepacti, INFOKEY.stepdeacti
}
step_info_optional_set.update(time_info_optional_set)

step_info_var_dependent_dict = {}
step_info_var_dependent_dict.update(time_info_var_dependent_dict)

step_info_initial_brace_dict = {}

step_info_default_brace_set = set()

step_info_operation_pre_list = []

step_info_info_prefix_dict = {}

step_info_operation_list = \
    operation_cycle_start("i", "0", f"i < len({INFOKEY.steptime})", "step_cycle_initialtime_add") + \
        operation_list_assign(f"{INFOKEY.stepacti}", "i", "stepacti_now", "step") + \
        operation_list_assign(f"{INFOKEY.stepdeacti}", "i", "stepdeacti_now", "step") + \
        operation_typeset_expression("type_now", f"'{rw.const.OBJECTTYPE.unitAdd}' if ((len({INFOKEY.steptime}) - i) % 2 == 1) ^ {INFOKEY.isactiend} else '{rw.const.OBJECTTYPE.unitRemove}'") + \
        [
            {
                AUTOKEY.operation_type: AUTOKEY.object, 
                AUTOKEY.type: br("type_now"), 
                AUTOKEY.optional: {
                    rw.const.OBJECTOP.activatedBy: ("{','.join(stepacti_now)}", "stepacti_now_exist", AUTOKEY.brace), 
                    rw.const.OBJECTOP.deactivatedBy: ("{','.join(stepdeacti_now)}", "stepdeacti_now_exist", AUTOKEY.brace), 
                    rw.const.OBJECTOP.warmup: ("{" + f"{INFOKEY.steptime}[i]" + "}", "steptime[i] != '0s' and steptime[i] != '0.0s'", AUTOKEY.brace), 
                    rw.const.OBJECTOP.spawnUnits: ("{" + f"{INFOKEY.aunit}" + "}*{" + f"{INFOKEY.spawnnum}" + "}", "'type_now' == 'unitAdd'", AUTOKEY.brace), 
                    rw.const.OBJECTOP.team: "{" + f"{INFOKEY.team}" + "}", 
                }
            }
        ] + \
    operation_cycle_end("i", "i + 1", "step_cycle_initialtime_add") + \
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
    ]

step_info = {
    INFOKEY.step_info:{
        AUTOKEY.info_args:step_info_args_dict, 
        AUTOKEY.default_args: step_info_default_args_dict, 
        AUTOKEY.var_dependent: step_info_var_dependent_dict, 
        AUTOKEY.optional:step_info_optional_set, 
        AUTOKEY.initial_brace: step_info_initial_brace_dict, 
        AUTOKEY.default_brace: step_info_default_brace_set, 
        AUTOKEY.info_prefix: step_info_info_prefix_dict, 

        AUTOKEY.ids: [[INFOKEY.idprefix, 1]], 
        AUTOKEY.prefix: AUTOKEY.prefix, 
        AUTOKEY.isprefixseg: AUTOKEY.isprefixseg, 
        AUTOKEY.args: [], 
        AUTOKEY.seg: ".", 
        AUTOKEY.opargs_prefix_len:1, 
        AUTOKEY.opargs: {}, 
        AUTOKEY.opargs_seg: ",", 
        AUTOKEY.operation_pre:step_info_operation_pre_list, 
        AUTOKEY.operation:step_info_operation_list, 
        AUTOKEY.no_check: True
    }
}

step_info = time_info_sub(step_info, [], [INFOKEY.steptime], [], [])
step_info = brace_add_info(step_info)
step_info = args_opargs_add_info(step_info)