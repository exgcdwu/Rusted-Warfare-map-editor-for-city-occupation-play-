import os
import sys
from collections import OrderedDict
current_file_path = os.path.abspath(__file__)
current_dir_path = os.path.dirname(current_file_path)
package_dir = os.path.dirname(current_dir_path)
sys.path.append(package_dir)
import rwmap as rw

from auto._core import AUTOKEY

class INFOKEY:
    prefix = "prefix"
    idprefix = "idprefix"
    isprefixseg = "isprefixseg"

    isinadd = "isinadd"
    inaddWarmup = "inaddWarmup"
    isinshowOnMap = "isinshowOnMap"
    inunitAddname = "inunitAddname"
    inunitAddoffset = "inunitAddoffset"
    inunitAddoffsetsize = "inunitAddoffsetsize"

    istext = "istext"
    textColor = "textColor"
    textSize = "textSize"
    mapTextname = "mapTextname"
    mapTextoffset = "mapTextoffset"
    mapTextoffsetsize = "mapTextoffsetsize"

    isteamDetect = "isteamDetect"
    teamDetectreset = "teamDetectreset"
    setTeam = "setTeam"
    setidTeam = "setidTeam"
    teamDetectname = "teamDetectname"
    teamDetectoffset = "teamDetectoffset"
    teamDetectoffsetsize = "teamDetectoffsetsize"

    isteamText = "isteamText"
    teamTextreset = "teamTextreset"
    teamTextcolor = "teamTextcolor"
    teamTextname = "teamTextname"
    teamTextoffset = "teamTextoffset"
    teamTextoffsetsize = "teamTextoffsetsize"

    detectReset = "detectReset"
    addWarmup = "addWarmup"
    addReset  = "addReset"
    unit = "unit"
    isonlybuilding = "isonlybuilding"
    isshowOnMap = "isshowOnMap"

    iscity = "iscity"
    unitAddname = "unitAddname"
    unitAddoffset = "unitAddoffset"
    unitAddoffsetsize = "unitAddoffsetsize"

    unitDetectname = "unitDetectname"
    unitDetectoffset = "unitDetectoffset"
    unitDetectoffsetsize = "unitDetectoffsetsize"



inadd_info_args_dict = OrderedDict()

inadd_info_args_dict[INFOKEY.prefix] = str
inadd_info_args_dict[INFOKEY.isprefixseg] = bool
inadd_info_args_dict[INFOKEY.unit] = str
inadd_info_args_dict[INFOKEY.isinadd] = bool
inadd_info_args_dict[INFOKEY.inaddWarmup] = str
inadd_info_args_dict[INFOKEY.isinshowOnMap] = bool
inadd_info_args_dict[INFOKEY.inunitAddname] = str
inadd_info_args_dict[INFOKEY.inunitAddoffset] = (list, int)
inadd_info_args_dict[INFOKEY.inunitAddoffsetsize] = (list, int)

text_info_args_dict = OrderedDict()

text_info_args_dict[INFOKEY.prefix] = str
text_info_args_dict[INFOKEY.isprefixseg] = bool
text_info_args_dict[INFOKEY.istext] = bool
text_info_args_dict[INFOKEY.textColor] = str
text_info_args_dict[INFOKEY.textSize] = str
text_info_args_dict[INFOKEY.mapTextname] = str
text_info_args_dict[INFOKEY.mapTextoffset] = (list, int)
text_info_args_dict[INFOKEY.mapTextoffsetsize] = (list, int)

teamDetect_info_args_dict = OrderedDict()

teamDetect_info_args_dict[INFOKEY.prefix] = str
teamDetect_info_args_dict[INFOKEY.isprefixseg] = bool
teamDetect_info_args_dict[INFOKEY.isteamDetect] = bool
teamDetect_info_args_dict[INFOKEY.teamDetectreset] = str
teamDetect_info_args_dict[INFOKEY.setTeam] = (list, list, int)
teamDetect_info_args_dict[INFOKEY.setidTeam] = (list, str)
teamDetect_info_args_dict[INFOKEY.teamDetectname] = (list, str)
teamDetect_info_args_dict[INFOKEY.teamDetectoffset] = (list, list, int)
teamDetect_info_args_dict[INFOKEY.teamDetectoffsetsize] = (list, list, int)

teamText_info_args_dict = OrderedDict()

teamText_info_args_dict[INFOKEY.prefix] = str
teamText_info_args_dict[INFOKEY.isprefixseg] = bool
teamText_info_args_dict[INFOKEY.isteamText] = bool
teamText_info_args_dict[INFOKEY.teamTextreset] = str
teamText_info_args_dict[INFOKEY.teamTextcolor] = (list, str)
teamText_info_args_dict[INFOKEY.teamTextname] = (list, str)
teamText_info_args_dict[INFOKEY.teamTextoffset] = (list, list, int)
teamText_info_args_dict[INFOKEY.teamTextoffsetsize] = (list, list, int)

city_info_args_dict = OrderedDict()
city_info_args_dict[INFOKEY.prefix] = str
city_info_args_dict[INFOKEY.idprefix] = str
city_info_args_dict[INFOKEY.detectReset] = str
city_info_args_dict[INFOKEY.addWarmup] = str
city_info_args_dict[INFOKEY.addReset] = str
city_info_args_dict[INFOKEY.unit] = str

city_info_args_dict[INFOKEY.isprefixseg] = bool
city_info_args_dict[INFOKEY.isonlybuilding] = bool
city_info_args_dict[INFOKEY.isshowOnMap] = bool

city_info_args_dict[INFOKEY.unitAddname] = str
city_info_args_dict[INFOKEY.unitAddoffset] = (list, int)
city_info_args_dict[INFOKEY.unitAddoffsetsize] = (list, int)

city_info_args_dict[INFOKEY.unitDetectname] = str
city_info_args_dict[INFOKEY.unitDetectoffset] = (list, int)
city_info_args_dict[INFOKEY.unitDetectoffsetsize] = (list, int)

city_info_args_dict.update(inadd_info_args_dict)
city_info_args_dict.update(text_info_args_dict)
city_info_args_dict.update(teamDetect_info_args_dict)
city_info_args_dict.update(teamText_info_args_dict)

inadd_info_default_args_dict = {
    "isinadd": "true", 
    "inaddWarmup": "0s", 
    "inunitAddname": "{team}", 
    "inunitAddoffset": "-20 0", 
    "inunitAddoffsetsize": "40 0"
}

text_info_default_args_dict = {
    "istext": "true", 
    "mapTextname": "", 
    "mapTextoffset": "0 0", 
    "mapTextoffsetsize": "0 0"
}

teamDetect_info_default_args_dict = {
    "isteamDetect": "true", 
    "teamDetectname": "[\"检测 setid\" + \"Team\" + str(ex) + \"_0\" for ex in range(lensetidTeam)]", 
    "teamDetectoffset": "[[-10*ex, -10*lensetidTeam+10*ex] for ex in range(lensetidTeam)]", 
    "teamDetectoffsetsize": "[[20*ex, 10*lensetidTeam-10*ex] for ex in range(lensetidTeam)]"
}

teamText_info_default_args_dict = {
    "isteamText": "true", 
    "teamTextreset": "1s", 
    "teamTextname": "[\"\"] * lensetidTeam", 
    "teamTextoffset": "[[0, 0] for i in range(lensetidTeam)]", 
    "teamTextoffsetsize": "[[0, 0] for i in range(lensetidTeam)]"
}

city_info_default_args_dict = {
    "unitAddname": "", 
    "unitAddoffset": "0 0", 
    "unitAddoffsetsize": "0 0", 

    "unitDetectname": "检测 {idprefix0}", 
    "unitDetectoffset": "-10 0", 
    "unitDetectoffsetsize": "20 0"
}
city_info_default_args_dict.update(inadd_info_default_args_dict)
city_info_default_args_dict.update(text_info_default_args_dict)
city_info_default_args_dict.update(teamDetect_info_default_args_dict)
city_info_default_args_dict.update(teamText_info_default_args_dict)
city_info_default_args_dict["isinadd"] = "false"
city_info_default_args_dict["istext"] = "false"
city_info_default_args_dict["isteamDetect"] = "false"
city_info_default_args_dict["isteamText"] = "false"

auto_func_arg = {
    "inadd_info": {
        AUTOKEY.info_args:inadd_info_args_dict, 
        AUTOKEY.default_args:inadd_info_default_args_dict, 
        AUTOKEY.prefix: "prefix", 
        AUTOKEY.isinfo_sub: True
    }, 
    "text_info": {
        AUTOKEY.info_args:text_info_args_dict, 
        AUTOKEY.default_args:text_info_default_args_dict, 
        AUTOKEY.prefix: "prefix", 
        AUTOKEY.isinfo_sub: True
    }, 
    "teamDetect_info": {
        AUTOKEY.info_args:teamDetect_info_args_dict, 
        AUTOKEY.default_args:teamDetect_info_default_args_dict, 
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
        AUTOKEY.default_args:teamText_info_default_args_dict, 
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
        AUTOKEY.default_args:city_info_default_args_dict, 
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
        AUTOKEY.opargs_seg: ",", 
        AUTOKEY.ids: [
            ["idprefix", 1]
        ], 
        AUTOKEY.operation_pre:[
     
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
        AUTOKEY.operation: [
            {
                AUTOKEY.operation_type: AUTOKEY.object, 
                "death": ["isshowOnMap"], 
                "offset": "unitAddoffset", 
                "offsetsize": "unitAddoffsetsize",                 
                "name": "{unitAddname}", 
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

            {
                AUTOKEY.operation_type: AUTOKEY.tag, 
                AUTOKEY.tag: "tag_end_teamtext"
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