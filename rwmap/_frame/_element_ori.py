import rwmap._frame._element_property as elepro
from typing import Union
from copy import deepcopy

class ElementOri:
    def __init__(self, tag:str, properties:elepro.ElementProperties)->None:
        self._tag = tag
        self._properties = deepcopy(properties)

    def tag(self)->str:
        return self._tag
    
    '''

    def assignDefaultProperty(self, name:str, value:Union[str, dict[str, str]]):
        self._properties.assignDefaultProperty(name, value)
    
    def assignOptionalProperty(self, name:str, value:Union[str, dict[str, str]]):
        self._properties.assignOptionalProperty(name, value)

    def returnDefaultProperty(self, name:str)->Union[str, dict[str, str]]:
        return self._properties.returnDefaultProperty(name)
    
    def returnOptionalProperty(self, name:str)->Union[str, dict[str, str]]:
        return self._properties.returnOptionalProperty(name)
    
    def deleteDefaultProperty(self, name:str)->None:
        self._properties.deleteDefaultProperty(name)
    
    def deleteOptionalProperty(self, name:str)->None:
        self._properties.deleteOptionalProperty(name)
    
    '''
    