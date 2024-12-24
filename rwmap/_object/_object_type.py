import xml.etree.ElementTree as et
from copy import deepcopy
from typing import Union

import rwmap._frame as frame
import rwmap._util as utility

class TObject_Type:
    def __init__(self, default_properties:dict[str, str], optional_properties:dict[str, Union[str, dict[str, str]]] = {}):
        self._default_properties = deepcopy(default_properties)
        self._optional_properties = deepcopy(optional_properties)

    def output_default_properties(self):
        return deepcopy(self._default_properties)
    
    def output_optional_properties(self):
        return deepcopy(self._optional_properties)
    
    def _add_optional(self, name:str, value:str):
        self._optional_properties.update(utility.add_str_pro(name, value))

    @classmethod
    def init_node(cls):
        return cls({"type": "unitAdd"}, {})
    
    @classmethod
    def init_basic(cls):
        return cls({"type": "basic"}, {})

    @classmethod
    def init_unitAdd(cls, team:int, spawnUnits:str, techLevel:int = -1):
        otype = cls({"type": "unitAdd"}, {"team": str(team), "spawnUnits": spawnUnits})
        otype._optional_properties.update(utility.add_time_pro("techLevel", techLevel, False))
        return otype
    
    @classmethod
    def init_unitDetect(cls, team:int = None, minUnits:int = None, maxUnits:int = None, unitType:str = None, onlyList:list[str] = []):
        otype = cls({"type": "unitDetect"}, {})
        otype._add_optional("team", team)
        otype._add_optional("unitType", unitType)
        minUnits = None if minUnits == -1 else minUnits
        maxUnits = None if maxUnits == -1 else maxUnits
        otype._add_optional("minUnits", minUnits)
        otype._add_optional("maxUnits", maxUnits)
        for only in onlyList:
            if only[0:13] == "onlyTechLevel":
                otype._add_optional(only[0:13], only[13])
            else:
                otype._optional_properties.update({only:{"type": "bool", "value": "true"}})
        return otype

    @classmethod
    def init_unitRemove(cls, team:int = None):
        otype = cls({"type": "unitRemove"}, {})
        otype._add_optional("team", team)
        return otype
    
    @classmethod
    def init_mapText(cls, text:str, textColor:str = None, textSize:int = -1):
        otype = cls({"type": "mapText"}, {})
        otype._add_optional("text", text)
        otype._add_optional("textColor", textColor)
        otype._optional_properties.update(utility.add_time_pro("textSize", textSize, False))
        return otype

    @classmethod
    def init_changeCredits(cls, team:int, setCredits:int = None, addCredits:int = None):
        otype = cls({"type": "changeCredits"}, {})
        otype._add_optional("set", setCredits)
        otype._add_optional("add", addCredits)
        otype._add_optional("team", team)
        return otype

    @classmethod
    def init_mapinfo(cls, mapType:str, mapFog:str, winCondition:str, text:str = None):
        otype = cls({"name": "map_info"}, {})
        otype._add_optional("type", mapType)
        otype._add_optional("fog", mapFog)
        otype._add_optional("introText", text)
        otype._add_optional("winCondition", winCondition)
        return otype
    
    @classmethod
    def init_none(cls):
        otype = cls({}, {})
        return otype

    @classmethod
    def init_camera_start(cls):
        otype = cls({"name": "camera_start"}, {})
        return otype

