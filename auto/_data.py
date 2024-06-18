import os
import sys
from collections import OrderedDict
current_file_path = os.path.abspath(__file__)
current_dir_path = os.path.dirname(current_file_path)
package_dir = os.path.dirname(current_dir_path)
sys.path.append(package_dir)
import rwmap as rw

from auto._core import AUTOKEY

inadd_info_args_dict = OrderedDict()

inadd_info_args_dict["prefix"] = str
inadd_info_args_dict["isinadd"] = bool
inadd_info_args_dict["inaddWarmup"] = str
inadd_info_args_dict["isinshowOnMap"] = bool
inadd_info_args_dict["inunitAddname"] = str
inadd_info_args_dict["inunitAddoffset"] = (list, int)
inadd_info_args_dict["inunitAddoffsetsize"] = (list, int)

text_info_args_dict = OrderedDict()

text_info_args_dict["prefix"] = str
text_info_args_dict["istext"] = bool
text_info_args_dict["textColor"] = str
text_info_args_dict["textSize"] = str
text_info_args_dict["mapTextname"] = str
text_info_args_dict["mapTextoffset"] = (list, int)
text_info_args_dict["mapTextoffsetsize"] = (list, int)

teamDetect_info_args_dict = OrderedDict()

teamDetect_info_args_dict["prefix"] = str
teamDetect_info_args_dict["isteamDetect"] = bool
teamDetect_info_args_dict["teamDetectreset"] = str
teamDetect_info_args_dict["setTeam"] = (list, list, int)
teamDetect_info_args_dict["setidTeam"] = (list, str)
teamDetect_info_args_dict["teamDetectname"] = (list, str)
teamDetect_info_args_dict["teamDetectoffset"] = (list, list, int)
teamDetect_info_args_dict["teamDetectoffsetsize"] = (list, list, int)

teamText_info_args_dict = OrderedDict()

teamText_info_args_dict["prefix"] = str
teamText_info_args_dict["isteamText"] = bool
teamText_info_args_dict["teamTextreset"] = str
teamText_info_args_dict["teamTextcolor"] = (list, str)
teamText_info_args_dict["teamTextname"] = (list, str)
teamText_info_args_dict["teamTextoffset"] = (list, list, int)
teamText_info_args_dict["teamTextoffsetsize"] = (list, list, int)

city_info_args_dict = OrderedDict()
city_info_args_dict["prefix"] = str
city_info_args_dict["idprefix"] = str
city_info_args_dict["detectReset"] = str
city_info_args_dict["addWarmup"] = str
city_info_args_dict["addReset"] = str
city_info_args_dict["unit"] = str

city_info_args_dict["isprefixseg"] = bool
city_info_args_dict["isonlybuilding"] = bool
city_info_args_dict["isshowOnMap"] = bool

city_info_args_dict["unitAddname"] = str
city_info_args_dict["unitAddoffset"] = (list, int)
city_info_args_dict["unitAddoffsetsize"] = (list, int)

city_info_args_dict["unitDetectname"] = str
city_info_args_dict["unitDetectoffset"] = (list, int)
city_info_args_dict["unitDetectoffsetsize"] = (list, int)

city_info_args_dict.update(inadd_info_args_dict)
city_info_args_dict.update(text_info_args_dict)
city_info_args_dict.update(teamDetect_info_args_dict)
city_info_args_dict.update(teamText_info_args_dict)

auto_func_arg = {
    "inadd_info": {
        AUTOKEY.info_args:inadd_info_args_dict, 
        AUTOKEY.default_args:{
            "inaddWarmup": "0s", 
            "inunitAddname": "{team}", 
            "isinadd": "true"
        }, 
        AUTOKEY.prefix: "prefix", 
        AUTOKEY.isinfo_sub: True
    }, 
    "text_info": {
        AUTOKEY.info_args:text_info_args_dict, 
        AUTOKEY.default_args:{
            "istext": "true", 
            "mapTextname": "", 
            "mapTextoffset": "0 0", 
            "mapTextoffsetsize": "0 0", 
        }, 
        AUTOKEY.prefix: "prefix", 
        AUTOKEY.isinfo_sub: True
    }, 
    "teamDetect_info": {
        AUTOKEY.info_args:teamDetect_info_args_dict, 
        AUTOKEY.default_args:{
            "isteamDetect": "true", 
            "teamDetectname": "[\"检测 setid\" + \"Team\" + str(ex) + \"_0\" for ex in range(lensetidTeam)]", 
            "teamDetectoffset": "[[-10*ex, -10*lensetidTeam+10*ex] for ex in range(lensetidTeam)]", 
            "teamDetectoffsetsize": "[[20*ex, 10*lensetidTeam-10*ex] for ex in range(lensetidTeam)]"
        }, 
        AUTOKEY.prefix: "prefix", 
        AUTOKEY.isinfo_sub: True, 
        AUTOKEY.initial_brace:{
            "lensetidTeam": "len(setidTeam)"
        }, 
        AUTOKEY.default_brace:{
            "teamDetectname", 
            "teamDetectoffset", 
            "teamDetectoffsetsize"
        }, 
    }, 
    "teamText_info": {
        AUTOKEY.info_args:teamText_info_args_dict, 
        AUTOKEY.default_args:{
            "isteamText": "true", 
            "teamTextreset": "1s", 
            "teamTextname": "[\"\"] * lensetidTeam", 
            "teamTextoffset": "[[0, 0] for i in range(lensetidTeam)]", 
            "teamTextoffsetsize": "[[0, 0] for i in range(lensetidTeam)]", 
        }, 
        AUTOKEY.prefix: "prefix", 
        AUTOKEY.isinfo_sub: True, 
        AUTOKEY.initial_brace:{
            "lensetidTeam": "len(teamTextcolor)"
        }, 
        AUTOKEY.default_brace:{
            "teamTextname", 
            "teamTextoffset", 
            "teamTextoffsetsize"
        }, 
    }, 
    "city_info": {
        AUTOKEY.info_args:city_info_args_dict, 
        AUTOKEY.default_args:{

            "unitAddname": "", 
            "unitAddoffset": "0 0", 
            "unitAddoffsetsize": "0 0", 

            "unitDetectname": "检测 {idprefix0}", 
            "unitDetectoffset": "-10 0", 
            "unitDetectoffsetsize": "20 0", 

            "isinadd": "false", 
            "inaddWarmup": "0s", 
            "inunitAddname": "{team}", 
            "inunitAddoffset": "0 -10", 
            "inunitAddoffsetsize": "0 20", 

            "istext": "false", 
            "mapTextname": "", 
            "mapTextoffset": "0 0", 
            "mapTextoffsetsize": "0 0", 

            "isteamDetect": "false", 
            "teamDetectname": "[\"检测 setid\" + \"Team\" + str(ex) + \"_0\" for ex in range(lensetidTeam)]", 
            "teamDetectoffset": "[\"[-10*ex, -10*lensetidTeam+10*ex]\" for ex in range(lensetidTeam)]", 
            "teamDetectoffsetsize": "[\"[20*ex, 10*lensetidTeam-10*ex]\" for ex in range(lensetidTeam)]", 

            "isteamText": "false", 
            "teamTextreset": "1s", 
            "teamTextname": "[\"\"] * lensetidTeam", 
            "teamTextoffset": "[[0, 0] for i in range(lensetidTeam)]", 
            "teamTextoffsetsize": "[[0, 0] for i in range(lensetidTeam)]", 
        }, 
        AUTOKEY.initial_brace:{
            "lensetidTeam": "len(setidTeam)"
        }, 
        AUTOKEY.default_brace:{
            "teamDetectname", 
            "teamDetectoffset", 
            "teamDetectoffsetsize", 
            "teamTextname", 
            "teamTextoffset", 
            "teamTextoffsetsize"
        }, 
        AUTOKEY.isprefixseg: "isprefixseg", 
        AUTOKEY.prefix: "prefix", 
        AUTOKEY.args: [
            ("cityname", str)
        ], 
        AUTOKEY.seg: ".", 
        AUTOKEY.opargs_prefix_len:1, 
        AUTOKEY.opargs: {
            "t": ("team|-1", str)
        }, 
        AUTOKEY.info_prefix:{
            "inadd_info": "inadd_prefix", 
            "text_info": "text_prefix", 
            "teamDetect_info": "teamDetect_prefix", 
            "teamText_info": "teamText_prefix"
        }, 
        AUTOKEY.var_dependent:{
            "inaddWarmup": "isinadd", 
            "isinshowOnMap": "isinadd", 
            "inunitAddname": "isinadd", 
            "inunitAddoffset": "isinadd", 
            "inunitAddoffsetsize": "isinadd", 
            "textColor": "istext", 
            "textSize": "istext", 
            "mapTextname": "istext", 
            "mapTextoffset": "istext", 
            "mapTextoffsetsize": "istext", 
            "teamDetectreset": "isteamDetect", 
            "setTeam": "isteamDetect", 
            "setidTeam": "isteamDetect", 
            "teamDetectname": "isteamDetect", 
            "teamDetectoffset": "isteamDetect", 
            "teamDetectoffsetsize": "isteamDetect", 
            "isteamText": "istext,isteamDetect", 
            "teamTextreset": "isteamText", 
            "teamTextcolor": "isteamText", 
            "teamTextname": "isteamText", 
            "teamTextoffset": "isteamText", 
            "teamTextoffsetsize": "isteamText"
        }, 
        AUTOKEY.optional:{
            "isprefixseg", 
            "isonlybuilding", 
            "isshowOnMap", 
            "isinadd", 
            "isinshowOnMap", 
            "istext", 
            "isteamDetect", 
            "isteamText"
        }, 
        AUTOKEY.id_operation:[
     
            {
                AUTOKEY.operation_type: AUTOKEY.typeif, 
                AUTOKEY.ifvar: "isteamDetect", 
                AUTOKEY.ifend_tag: "tag_end"
            }, 
            {
                AUTOKEY.operation_type: AUTOKEY.typeset, 
                "i": "0"
            }, 

            {
                AUTOKEY.operation_type: AUTOKEY.tag, 
                AUTOKEY.tag: "tag"
            }, 

            {
                AUTOKEY.operation_type: AUTOKEY.typeif, 
                AUTOKEY.ifvar: "i < len(setidTeam)", 
                AUTOKEY.ifend_tag: "tag_end"
            }, 

            {
                AUTOKEY.operation_type: AUTOKEY.typeset_id, 
                "setidTeam{i}_": "1", 
                AUTOKEY.real_idexp: "{setidTeam[i]}"
            }, 

            {
                AUTOKEY.operation_type: AUTOKEY.typeset_expression, 
                "i": "i + 1"
            }, 

            {
                AUTOKEY.operation_type: AUTOKEY.goto, 
                AUTOKEY.goto_tag: "tag"
            },

            {
                AUTOKEY.operation_type: AUTOKEY.tag, 
                AUTOKEY.tag: "tag_end"
            }
        ], 
        AUTOKEY.opargs_seg: ",", 
        AUTOKEY.ids: [
            ["idprefix", 1]
        ], 
        AUTOKEY.operation: [
            {
                AUTOKEY.operation_type: AUTOKEY.object, 
                "death": ["isshowOnMap"], 
                "offset": "unitAddoffset", 
                "offsetsize": "unitAddoffsetsize",                 
                "name": "{unitAddName}", 
                "type": rw.const.OBJECTTYPE.unitAdd, 
                "optional": {
                    rw.const.OBJECTOP.spawnUnits: "{unit}", 
                    rw.const.OBJECTOP.activatedBy: "{idprefix0}", 
                    rw.const.OBJECTOP.resetActivationAfter: "{addReset}", 
                    rw.const.OBJECTOP.team: "-1", 
                    rw.const.OBJECTOP.warmup: "{addWarmup}"
                }
            }, 
            {
                AUTOKEY.operation_type: AUTOKEY.object, 
                "exist": ["isshowOnMap"], 
                "offset": "unitAddoffset", 
                "offsetsize": "unitAddoffsetsize", 
                "name": "{unitAddname}", 
                "type": rw.const.OBJECTTYPE.unitAdd, 
                "optional": {
                    rw.const.OBJECTOP.spawnUnits: "{unit}", 
                    rw.const.OBJECTOP.activatedBy: "{idprefix0}", 
                    rw.const.OBJECTOP.resetActivationAfter: "{addReset}", 
                    rw.const.OBJECTOP.team: "-1", 
                    rw.const.OBJECTOP.warmup: "{addWarmup}", 
                    rw.const.OBJECTOP.showOnMap: True
                }
            }, 
            {
                AUTOKEY.operation_type: AUTOKEY.object, 
                "exist": ["isinadd"], 
                "death": ["isinshowOnMap"], 
                "offset": "inunitAddoffset", 
                "offsetsize": "inunitAddoffsetsize", 
                "name": "{inunitAddname}", 
                "type": rw.const.OBJECTTYPE.unitAdd, 
                "optional": {
                    rw.const.OBJECTOP.spawnUnits: "{unit}", 
                    rw.const.OBJECTOP.team: "{team}", 
                    rw.const.OBJECTOP.warmup: "{inaddWarmup}"
                }
            }, 
            {
                AUTOKEY.operation_type: AUTOKEY.object, 
                "exist": ["isinadd", "isinshowOnMap"], 
                "offset": "inunitAddoffset", 
                "offsetsize": "inunitAddoffsetsize", 
                "name": "{inunitAddname}", 
                "type": rw.const.OBJECTTYPE.unitAdd, 
                "optional": {
                    rw.const.OBJECTOP.spawnUnits: "{unit}", 
                    rw.const.OBJECTOP.team: "{team}", 
                    rw.const.OBJECTOP.warmup: "{inaddWarmup}", 
                    rw.const.OBJECTOP.showOnMap: True
                }
            }, 
            {
                AUTOKEY.operation_type: AUTOKEY.object, 
                "death": ["isonlybuilding"], 
                "offset": "unitDetectoffset", 
                "offsetsize": "unitDetectoffsetsize", 
                "name": "{unitDetectname}", 
                "type": rw.const.OBJECTTYPE.unitDetect, 
                "optional": {
                    rw.const.OBJECTOP.id: "{idprefix0}", 
                    rw.const.OBJECTOP.maxUnits: "0", 
                    rw.const.OBJECTOP.resetActivationAfter: "{detectReset}", 
                    rw.const.OBJECTOP.unitType: "{unit}"
                }
            }, 
            {
                AUTOKEY.operation_type: AUTOKEY.object, 
                "exist": ["isonlybuilding"], 
                "offset": "unitDetectoffset", 
                "offsetsize": "unitDetectoffsetsize", 
                "name": "{unitDetectname}", 
                "type": rw.const.OBJECTTYPE.unitDetect, 
                "optional": {
                    rw.const.OBJECTOP.id: "{idprefix0}", 
                    rw.const.OBJECTOP.maxUnits: "0", 
                    rw.const.OBJECTOP.resetActivationAfter: "{detectReset}", 
                    rw.const.OBJECTOP.onlyBuildings: True
                }
            }, 

            {
                AUTOKEY.operation_type: AUTOKEY.typeif, 
                AUTOKEY.ifvar: "istext", 
                AUTOKEY.ifend_tag: "tag_end_text"
            }, 

            {
                AUTOKEY.operation_type: AUTOKEY.typeif, 
                AUTOKEY.ifvar: "isteamText", 
                AUTOKEY.ifend_tag: "tag_end_teamtext"
            }, 
##

            {
                AUTOKEY.operation_type: AUTOKEY.typeset_expression, 
                "teamtextids": "[\"setid\" + \"Team\" + str(ex) + \"_0\" for ex in range(len(setidTeam))]"
            }, 

            {
                AUTOKEY.operation_type: AUTOKEY.changetype, 
                AUTOKEY.keyname_list: ["teamtextids"], 
                AUTOKEY.totype: str
            }, 

            {
                AUTOKEY.operation_type: AUTOKEY.object, 
                "name": "{mapTextname}", 
                "offset": "mapTextoffset", 
                "offsetsize": "mapTextoffsetsize", 
                "type": rw.const.OBJECTTYPE.mapText, 
                "optional": {
                    rw.const.OBJECTOP.text: "{cityname}", 
                    rw.const.OBJECTOP.textColor: "{textColor}", 
                    rw.const.OBJECTOP.textSize: "{textSize}", 
                    rw.const.OBJECTOP.deactivatedBy: "{teamtextids}", 
                    rw.const.OBJECTOP.resetActivationAfter: "{teamTextreset}"
                }
            }, 

            {
                AUTOKEY.operation_type: AUTOKEY.typeset, 
                "i": 0
            }, 

            {
                AUTOKEY.operation_type: AUTOKEY.tag, 
                AUTOKEY.tag: "tag_teamtext_cycle"
            }, 

            {
                AUTOKEY.operation_type: AUTOKEY.typeif, 
                AUTOKEY.ifvar: "i < lensetidTeam", 
                AUTOKEY.ifend_tag: "tag_end_text"
            }, 

            {
                AUTOKEY.operation_type:AUTOKEY.typeset_expression, 
                "id_temp": "setidTeam{i}_0"
            }, 
            {
                AUTOKEY.operation_type: AUTOKEY.object, 
                "type": rw.const.OBJECTTYPE.mapText, 
                "name": "{teamTextname[i]}", 
                "offset": "teamTextoffset[i]", 
                "offsetsize": "teamTextoffsetsize[i]", 
                "optional": {
                    rw.const.OBJECTOP.text: "{cityname}", 
                    rw.const.OBJECTOP.textColor: "{teamTextcolor[i]}", 
                    rw.const.OBJECTOP.textSize: "{textSize}", 
                    rw.const.OBJECTOP.activatedBy: "{id_temp}", 
                    rw.const.OBJECTOP.resetActivationAfter: "{teamTextreset}"
                }
            }, 

            {
                AUTOKEY.operation_type: AUTOKEY.typeset_expression, 
                "i": "i + 1"
            }, 


            {
                AUTOKEY.operation_type: AUTOKEY.goto, 
                AUTOKEY.goto_tag: "tag_teamtext_cycle"
            }, 



##
            {
                AUTOKEY.operation_type: AUTOKEY.object, 
                "name": "{mapTextname}", 
                "offset": "mapTextoffset", 
                "offsetsize": "mapTextoffsetsize", 
                "type": rw.const.OBJECTTYPE.mapText, 
                "optional": {
                    rw.const.OBJECTOP.text: "{cityname}", 
                    rw.const.OBJECTOP.textColor: "{textColor}", 
                    rw.const.OBJECTOP.textSize: "{textSize}", 
                }
            }, 

            {
                AUTOKEY.operation_type: AUTOKEY.tag, 
                AUTOKEY.tag: "tag_end_text"
            }, 

            {
                AUTOKEY.operation_type: AUTOKEY.typeif, 
                AUTOKEY.ifvar: "isteamDetect", 
                AUTOKEY.ifend_tag: "tag_end"
            }, 
            {
                AUTOKEY.operation_type: AUTOKEY.typeset, 
                "i": 0
            }, 

            {
                AUTOKEY.operation_type: AUTOKEY.tag, 
                AUTOKEY.tag: "tag"
            }, 

            {
                AUTOKEY.operation_type: AUTOKEY.typeif, 
                AUTOKEY.ifvar: "i < lensetidTeam", 
                AUTOKEY.ifend_tag: "tag_end"
            }, 

            {
                AUTOKEY.operation_type: AUTOKEY.typeset, 
                "j": 0
            }, 

            {
                AUTOKEY.operation_type: AUTOKEY.tag, 
                AUTOKEY.tag: "tag_2"
            }, 

            {
                AUTOKEY.operation_type: AUTOKEY.typeif, 
                AUTOKEY.ifvar: "j < len(setTeam[i])", 
                AUTOKEY.ifend_tag: "tag_end_2"
            }, 

            {
                AUTOKEY.operation_type:AUTOKEY.typeset_expression, 
                "id_temp": "setidTeam{i}_0"
            }, 

            {
                AUTOKEY.operation_type:AUTOKEY.typeset_expression, 
                "isi_eq_0": "j == 0"
            }, 

            {
                AUTOKEY.operation_type: AUTOKEY.object, 
                "exist": ["isi_eq_0"], 
                "death": ["isonlybuilding"], 
                "offset": "teamDetectoffset[i]", 
                "offsetsize": "teamDetectoffsetsize[i]", 
                "name": "{teamDetectname[i]}", 
                "type": rw.const.OBJECTTYPE.unitDetect, 
                "optional": {
                    rw.const.OBJECTOP.id: "{id_temp}", 
                    rw.const.OBJECTOP.minUnits: "1", 
                    rw.const.OBJECTOP.resetActivationAfter: "{teamDetectreset}", 
                    rw.const.OBJECTOP.unitType: "{unit}", 
                    rw.const.OBJECTOP.team: "{setTeam[i][j]}"
                }
            }, 

            {
                AUTOKEY.operation_type: AUTOKEY.object, 
                "death": ["isi_eq_0", "isonlybuilding"], 
                "offset": "teamDetectoffset[i]", 
                "offsetsize": "teamDetectoffsetsize[i]", 
                "type": rw.const.OBJECTTYPE.unitDetect, 
                "optional": {
                    rw.const.OBJECTOP.id: "{id_temp}", 
                    rw.const.OBJECTOP.minUnits: "1", 
                    rw.const.OBJECTOP.resetActivationAfter: "{teamDetectreset}", 
                    rw.const.OBJECTOP.unitType: "{unit}", 
                    rw.const.OBJECTOP.team: "{setTeam[i][j]}"
                }
            }, 

            {
                AUTOKEY.operation_type: AUTOKEY.object, 
                "exist": ["isi_eq_0", "isonlybuilding"], 
                "offset": "teamDetectoffset[i]", 
                "offsetsize": "teamDetectoffsetsize[i]", 
                "name": "{teamDetectname[i]}", 
                "type": rw.const.OBJECTTYPE.unitDetect, 
                "optional": {
                    rw.const.OBJECTOP.id: "{id_temp}", 
                    rw.const.OBJECTOP.minUnits: "1", 
                    rw.const.OBJECTOP.resetActivationAfter: "{teamDetectreset}", 
                    rw.const.OBJECTOP.onlyBuildings: True, 
                    rw.const.OBJECTOP.team: "{setTeam[i][j]}"
                }
            }, 

            {
                AUTOKEY.operation_type: AUTOKEY.object, 
                "death": ["isi_eq_0"], 
                "exist": ["isonlybuilding"], 
                "offset": "teamDetectoffset[i]", 
                "offsetsize": "teamDetectoffsetsize[i]", 
                "type": rw.const.OBJECTTYPE.unitDetect, 
                "optional": {
                    rw.const.OBJECTOP.id: "{id_temp}", 
                    rw.const.OBJECTOP.minUnits: "1", 
                    rw.const.OBJECTOP.resetActivationAfter: "{teamDetectreset}", 
                    rw.const.OBJECTOP.onlyBuildings: True, 
                    rw.const.OBJECTOP.team: "{setTeam[i][j]}"
                }
            }, 

            {
                AUTOKEY.operation_type: AUTOKEY.typeset_expression, 
                "j": "j + 1"
            }, 

            {
                AUTOKEY.operation_type: AUTOKEY.goto, 
                AUTOKEY.goto_tag: "tag_2"
            },

            {
                AUTOKEY.operation_type: AUTOKEY.tag, 
                AUTOKEY.tag: "tag_end_2"
            }, 

            {
                AUTOKEY.operation_type: AUTOKEY.typeset_expression, 
                "i": "i + 1"
            }, 

            {
                AUTOKEY.operation_type: AUTOKEY.goto, 
                AUTOKEY.goto_tag: "tag"
            },

            {
                AUTOKEY.operation_type: AUTOKEY.tag, 
                AUTOKEY.tag: "tag_end"
            }
        ]
    }
}

'''
            {
                AUTOKEY.operation_type: AUTOKEY.typeset, 
                "i": 0
            }, 

            {
                AUTOKEY.operation_type: AUTOKEY.tag, 
                AUTOKEY.tag: "tag"
            }, 

            {
                AUTOKEY.operation_type: AUTOKEY.typeif, 
                AUTOKEY.ifvar: "i < 1", 
                AUTOKEY.ifend_tag: "tag_end"
            }, 

            {
                AUTOKEY.operation_type: AUTOKEY.object, 
                "name": "{unitAddName}{i} 标记", 
                "type": rw.const.OBJECTTYPE.unitAdd, 
                "optional": {
                    rw.const.OBJECTOP.spawnUnits: "{unit}", 
                    rw.const.OBJECTOP.activatedBy: "{idprefix0}", 
                    rw.const.OBJECTOP.resetActivationAfter: "{addReset}", 
                    rw.const.OBJECTOP.team: "-1", 
                    rw.const.OBJECTOP.warmup: "{addWarmup}"
                }
            }, 

            {
                AUTOKEY.operation_type: AUTOKEY.typeset_expression, 
                "i": "i + 1"
            }, 

            {
                AUTOKEY.operation_type: AUTOKEY.typeset_exist, 
                "i": "i"
            }, 

            {
                AUTOKEY.operation_type: AUTOKEY.goto, 
                AUTOKEY.goto_tag: "tag"
            },

            {
                AUTOKEY.operation_type: AUTOKEY.tag, 
                AUTOKEY.tag: "tag_end"
            }, 

            {
                AUTOKEY.operation_type: AUTOKEY.changetype, 
                AUTOKEY.keyname_list: ["addWarmup"], 
                AUTOKEY.totype: bool
            }, 

    info_prefix-info内,提供导入数据方位
'''