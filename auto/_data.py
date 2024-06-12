import os
import sys
current_file_path = os.path.abspath(__file__)
current_dir_path = os.path.dirname(current_file_path)
package_dir = os.path.dirname(current_dir_path)
sys.path.append(package_dir)
import rwmap as rw

class AUTOKEY:
    info_args = "info_args"
    prefix = "prefix"
    info = "info"
    args = "args"
    seg = "seg"
    opargs = "opargs"
    opargs_seg = "opargs_seg"
    opargs_prefix_len = "opargs_prefix_len"
    ids = "ids"
    operation = "operation"

    offset = "offset", 
    size = "size", 
    name = "name", 
    type = "type", 
    optional = "optional"

auto_func_arg = {
    "city_info": {
        AUTOKEY.info_args:{
            "prefix": str, 
            "idprefix": str, 
            "detectReset": str, 
            "addWarmup": str, 
            "addReset": str, 
            "isinadd": bool, 
            "inaddWarmup":str, 
            "unit": str, 
            "isonlybuilding": bool, 
            "istext": bool, 
            "textColor": str, 
            "textSize": str
        }, 
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
                "offset": rw.frame.Coordinate(), 
                "name": "{cityname}刷新", 
                "type": rw.const.OBJECTTYPE.unitAdd, 
                "optional": {
                    rw.const.OBJECTOP.spawnUnits: "{unit}", 
                    rw.const.OBJECTOP.activatedBy: "{ids0}", 
                    rw.const.OBJECTOP.resetActivationAfter: "{addReset}", 
                    rw.const.OBJECTOP.team: "-1", 
                    rw.const.OBJECTOP.warmup: "{addWarmup}"
                }
            }, 
            {
                "exist": "isinadd", 
                "offset": rw.frame.Coordinate(), 
                "name": "{cityname}初始添加({team})", 
                "type": rw.const.OBJECTTYPE.unitAdd, 
                "optional": {
                    rw.const.OBJECTOP.spawnUnits: "{unit}", 
                    rw.const.OBJECTOP.team: "{team}", 
                    rw.const.OBJECTOP.warmup: "{inaddWarmup}"
                }
            }, 
            {
                "death": "isonlybuilding", 
                "offset": rw.frame.Coordinate(), 
                "name": "{cityname}检测", 
                "type": rw.const.OBJECTTYPE.unitDetect, 
                "optional": {
                    rw.const.OBJECTOP.id: "{ids0}", 
                    rw.const.OBJECTOP.maxUnits: "0", 
                    rw.const.OBJECTOP.resetActivationAfter: "{detectReset}", 
                    rw.const.OBJECTOP.unitType: "{unit}"
                }
            }, 
            {
                "exist": "isonlybuilding", 
                "offset": rw.frame.Coordinate(), 
                "name": "{cityname}检测", 
                "type": rw.const.OBJECTTYPE.unitDetect, 
                "optional": {
                    rw.const.OBJECTOP.id: "{ids0}", 
                    rw.const.OBJECTOP.maxUnits: "0", 
                    rw.const.OBJECTOP.resetActivationAfter: "{detectReset}", 
                    rw.const.OBJECTOP.onlyBuildings: {"type":"bool", "value":"true"}
                }
            }, 
            {
                "exist": "istext", 
                "offset": rw.frame.Coordinate(), 
                "name": "{cityname}文本", 
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