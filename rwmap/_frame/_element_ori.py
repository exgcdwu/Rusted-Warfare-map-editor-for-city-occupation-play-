import rwmap._frame._element_property as elepro
from typing import Union
from copy import deepcopy

class ElementOri:
    def __init__(self, properties:elepro.ElementProperties)->None:
        self._properties = deepcopy(properties)
        
    def name(self, name:str)->Union[str, None]:
        return self._properties.returnDefaultProperty(name)