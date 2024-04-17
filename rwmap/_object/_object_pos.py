import xml.etree.ElementTree as et

import rwmap._frame as frame

class TObject_Pos:
    def __init__(self, default_properties:dict[str, str], other_properties:list[et.Element] = {}):
        self._default_properties = default_properties
        self._other_properties = other_properties

    @classmethod
    def init_rectangle(cls, rect:frame.Rectangle):
        default_properties = {"x": rect.i().x(), "y": rect.i().y(), "width": rect.a().x(), "height": rect.a().y()}
        return cls(default_properties)
    
    def output_default_properties(self):
        return self._default_properties
    
    def output_other_properties(self):
        return self._other_properties