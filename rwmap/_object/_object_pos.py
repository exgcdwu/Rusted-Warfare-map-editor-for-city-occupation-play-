import xml.etree.ElementTree as et
from copy import deepcopy

import rwmap._frame as frame

class TObject_Pos:
    pass

class TObject_Pos:
    def __init__(self, default_properties:dict[str, str], other_properties:list[et.Element] = {}):
        self._default_properties = default_properties
        self._other_properties = other_properties

    @classmethod
    def init_rectangle(cls, rect:frame.Rectangle):
        default_properties = {"x": f"{rect.i().x():.0f}", "y": f"{rect.i().y():.0f}", 
                              "width": f"{rect.a().x():.0f}", "height": f"{rect.a().y():.0f}"}
        return cls(default_properties)
    
    def output_default_properties(self):
        return self._default_properties
    
    def output_other_properties(self):
        return self._other_properties
    
    def offset(self, offset:frame.Coordinate)->TObject_Pos:
        newtp = deepcopy(self)
        try:
            newtp._default_properties["x"] = f"{float(self._default_properties["x"]) + offset.x():.0f}"
            newtp._default_properties["y"] = f"{float(self._default_properties["y"]) + offset.y():.0f}"
        except KeyError:
            raise KeyError("Position: uninitialized")
        return newtp