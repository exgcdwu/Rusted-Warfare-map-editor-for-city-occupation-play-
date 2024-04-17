import xml.etree.ElementTree as et

import rwmap._frame as frame

class TObject_Pro:
    def __init__(self, default_properties:dict[str, str], optional_properties:dict[str, str] = {}):
        self._default_properties = default_properties
        self._optional_properties = optional_properties

    def output_default_properties(self):
        return self._default_properties
    
    def output_optional_properties(self):
        return self._optional_properties
    
    def add_name(self, name:str)->None:
        name_dict = {"name": name}
        if self._default_properties == None:
            self._default_properties = name_dict
        else:
            self._default_properties.update(name_dict)
