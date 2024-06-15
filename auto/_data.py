import os
import sys
current_file_path = os.path.abspath(__file__)
current_dir_path = os.path.dirname(current_file_path)
package_dir = os.path.dirname(current_dir_path)
sys.path.append(package_dir)
import rwmap as rw

from auto._core import AUTOKEY

auto_func_arg = {
    "city_info": {
        AUTOKEY.info_args:{
            "prefix": str, 
            "idprefix": str, 
            "isprefixseg": bool, 
            "detectReset": str, 
            "addWarmup": str, 
            "addReset": str, 
            "isinadd": bool, 
            "inaddWarmup":str, 
            "unit": str, 
            "isonlybuilding": bool, 
            "mapTextName": str, 
            "unitAddName": str, 
            "inunitAddName": str, 
            "unitDetectName": str, 
            "isshowOnMap": bool, 
            "isinshowOnMap": bool, 

            "isteamDetect": bool, 
            "setTeam": (list, list, int), 
            "setidTeam": (list, str), 
            "teamDetectoffset": (list, list, int), 
            "teamDetectoffsetsize": (list, list, int), 
            "teamDetectname": (list, str), 
            "teamDetectreset": str, 

            "istext": bool, 
            "textColor": str, 
            "textSize": str, 

            "isteamText": bool, 
            "teamTextcolor": (list, str), 
            "teamTextreset": str
        }, 
        AUTOKEY.default_args:{
            "inaddWarmup": "0s", 
            "mapTextName": "", 
            "unitAddName": "", 
            "inunitAddName": "{team}", 
            "unitDetectName": "检测 {idprefix0}", 
            "teamTextreset": "1s"
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
                "name": "{unitAddName}", 
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
                "offset": "[0, -20]",
                "offsetsize": "[0, 40]", 
                "name": "{inunitAddName}", 
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
                "offset": "[0, -20]",
                "offsetsize": "[0, 40]", 
                "name": "{inunitAddName}", 
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
                "offset": "[-20, 0]",
                "offsetsize": "[40, 0]", 
                "name": "{unitDetectName}", 
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
                "offset": "[-20, 0]",
                "offsetsize": "[40, 0]", 
                "name": "{unitDetectName}", 
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
                "name": "{mapTextName}", 
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
                AUTOKEY.ifvar: "i < len(setidTeam)", 
                AUTOKEY.ifend_tag: "tag_end_text"
            }, 

            {
                AUTOKEY.operation_type:AUTOKEY.typeset_expression, 
                "id_temp": "setidTeam{i}_0"
            }, 

            {
                AUTOKEY.operation_type: AUTOKEY.object, 
                "type": rw.const.OBJECTTYPE.mapText, 
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
                "name": "{mapTextName}", 
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
                AUTOKEY.operation_type: AUTOKEY.typeset_exist, 
                "isteamDetectnameexist": "teamDetectname"
            }, 

            {
                AUTOKEY.operation_type: AUTOKEY.typeif, 
                AUTOKEY.ifvar: "not isteamDetectnameexist", 
                AUTOKEY.ifend_tag: "tag_end_td"
            }, 

            {
                AUTOKEY.operation_type: AUTOKEY.typeset_expression, 
                "teamDetectname": "[\"检测 setid\" + \"Team\" + str(ex) + \"_0\" for ex in range(len(setidTeam))]"
            }, 

            {
                AUTOKEY.operation_type: AUTOKEY.tag, 
                AUTOKEY.tag: "tag_end_td"
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
                AUTOKEY.ifvar: "i < len(setidTeam)", 
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
                "death": ["isi_eq_0"], 
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