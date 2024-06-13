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
            "istext": bool, 
            "textColor": str, 
            "textSize": str, 
            "mapTextName": str, 
            "unitAddName": str, 
            "inunitAddName": str, 
            "unitDetectName": str, 
            "isshowOnMap": bool, 
            "isinshowOnMap": bool
        }, 
        AUTOKEY.default_args:{
            "inaddWarmup": "0s", 
            "mapTextName": "", 
            "unitAddName": "", 
            "inunitAddName": "{team}", 
            "unitDetectName": "检测 {idprefix0}"
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
        AUTOKEY.opargs_seg: ",", 
        AUTOKEY.ids: [
            ("idprefix", 1)
        ], 
        AUTOKEY.operation: [
            {
                "death": ["isshowOnMap"], 
                "offset": rw.frame.Coordinate(), 
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
                "exist": ["isshowOnMap"], 
                "offset": rw.frame.Coordinate(), 
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
                "exist": ["isinadd"], 
                "death": ["isinshowOnMap"], 
                "offset": rw.frame.Coordinate(0, -20),
                "offsetsize": rw.frame.Coordinate(0, 40), 
                "name": "{inunitAddName}", 
                "type": rw.const.OBJECTTYPE.unitAdd, 
                "optional": {
                    rw.const.OBJECTOP.spawnUnits: "{unit}", 
                    rw.const.OBJECTOP.team: "{team}", 
                    rw.const.OBJECTOP.warmup: "{inaddWarmup}"
                }
            }, 
            {
                "exist": ["isinadd", "isinshowOnMap"], 
                "offset": rw.frame.Coordinate(0, -20),
                "offsetsize": rw.frame.Coordinate(0, 40), 
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
                "death": ["isonlybuilding"], 
                "offset": rw.frame.Coordinate(-20, 0),
                "offsetsize": rw.frame.Coordinate(40, 0), 
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
                "exist": ["isonlybuilding"], 
                "offset": rw.frame.Coordinate(-20, 0),
                "offsetsize": rw.frame.Coordinate(40, 0), 
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
                "exist": ["istext"], 
                "offset": rw.frame.Coordinate(), 
                "name": "{mapTextName}", 
                "type": rw.const.OBJECTTYPE.mapText, 
                "optional": {
                    rw.const.OBJECTOP.text: "{cityname}", 
                    rw.const.OBJECTOP.textColor: "{textColor}", 
                    rw.const.OBJECTOP.textSize: "{textSize}", 
                }
            }
        ]
    }
}