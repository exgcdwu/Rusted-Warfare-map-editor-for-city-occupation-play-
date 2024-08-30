import xml.etree.ElementTree as et
from copy import deepcopy

import rwmap._frame as frame
import rwmap._util as utility

class TObject_Pos:
    pass

class TObject_Pos:
    def __init__(self, default_properties:dict[str, str], other_properties:list[et.Element] = {}):
        self._default_properties = deepcopy(default_properties)
        self._other_properties = deepcopy(other_properties)

    @classmethod
    def init_rectangle(cls, rect:frame.Rectangle):
        default_properties = {"x": f"{rect.i().x():.2f}", "y": f"{rect.i().y():.2f}", 
                              "width": f"{rect.a().x():.2f}", "height": f"{rect.a().y():.2f}"}
        return cls(default_properties)
    
    @classmethod
    def init_polygon(cls, point_list:list[frame.Coordinate], midpos:frame.Coordinate):
        default_properties = {"x": f"{midpos.x():.2f}", "y": f"{midpos.y():.2f}"}
        point_list_str = utility.point_list_to_str(point_list)
        other_properties = [et.Element("polygon", {"points": point_list_str})]
        return cls(default_properties, other_properties)

    def size(self)->frame.Coordinate:
        return frame.Coordinate(int(self._default_properties["width"]),
                                int(self._default_properties["height"]))
    
    def pos(self)->frame.Coordinate:
        return frame.Coordinate(int(self._default_properties["x"]),
                                int(self._default_properties["y"]))
    
    def rectangle(self)->frame.Rectangle:
        return frame.Rectangle(self.pos(), self.size())

    def output_default_properties(self):
        return deepcopy(self._default_properties)
    
    def output_other_properties(self):
        return deepcopy(self._other_properties)
    
    def offset(self, offset:frame.Coordinate)->TObject_Pos:
        newtp = deepcopy(self)
        try:
            newtp._default_properties["x"] = f"{float(self._default_properties['x']) + offset.x():.2f}"
            newtp._default_properties["y"] = f"{float(self._default_properties['y']) + offset.y():.2f}"
        except KeyError:
            raise KeyError("Position: uninitialized")
        return newtp