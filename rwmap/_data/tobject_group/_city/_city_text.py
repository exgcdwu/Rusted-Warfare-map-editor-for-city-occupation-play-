from typing import Union
from copy import deepcopy

import rwmap._object as object
import rwmap._frame as frame
import rwmap._data.tobject as tobject
import rwmap._data.const as const

import rwmap._util as utility

class CityText(object.TObject_Group):
    def __init__(self, pos:frame.Coordinate, text:Union[list[str], str], 
                 size:frame.Coordinate = const.COO.SIZE_STANDARD, 
                 textColor:Union[list[str], str] = [], textSize:int = -1, 
                 name:Union[list[str], str] = [], 
                 actiBy_s_list:list[Union[list[object.TObject_One], object.TObject_One]] = [], 
                 deactiBy_s_list:list[Union[list[object.TObject_One], object.TObject_One]] = [], 
                 reset:int = 1):
        name_list = deepcopy(utility.list_variable_s(name))
        text_list = deepcopy(utility.list_variable_s(text))
        textColor_list = deepcopy(utility.list_variable_s(textColor))
        if len(textColor_list) > len(text_list):
            raise ValueError("the length of textColor is longer than text")
        maptext = []
        for index in range(len(text_list)):
            name = utility.list_get_s(name_list, index)
            text = utility.list_get_s(text_list, index)
            textColor = utility.list_get_s(textColor_list, index)
            actiBy_s =  deepcopy(utility.list_variable_s(utility.list_get_s(actiBy_s_list, index)))
            deactiBy_s =  deepcopy(utility.list_variable_s(utility.list_get_s(deactiBy_s_list, index)))
            actiBy_s = [] if actiBy_s == None else actiBy_s
            deactiBy_s = [] if deactiBy_s == None else deactiBy_s
            maptext.append(tobject.MapText(pos, text, size = size, textColor = textColor, 
                                           textSize = textSize, name = name, actiBy_s = actiBy_s, 
                                           deactiBy_s = deactiBy_s, reset = reset))
        object.TObject_Group.__init__(self, maptext)
    
    def pos(self)->frame.Coordinate:
        return self._TObject_One_list[0]._pos.pos()

    def size(self)->frame.Coordinate:
        return self._TObject_One_list[0]._pos.size()

    def length(self):
        return len(self._TObject_One_list)

    def maptext(self, index:int)->tobject.MapText:
        return self._TObject_One_list[index]

    def add_actiBy_s(self, actiBy_s_list:list[Union[list[object.TObject_One], object.TObject_One]] = []):
        for index in range(self.size()):
            actiBy_s =  deepcopy(utility.list_variable_s(utility.list_get_s(actiBy_s_list, index)))
            self.maptext(index).add_actiBy_s(actiBy_s)
    
    def add_deactiBy_s(self, deactiBy_s_list:list[Union[list[object.TObject_One], object.TObject_One]] = []):
        for index in range(self.size()):
            deactiBy_s =  deepcopy(utility.list_variable_s(utility.list_get_s(deactiBy_s_list, index)))
            self.maptext(index).add_deactiBy_s(deactiBy_s)

    
class CityTextNoTeam(CityText):
    def __init__(self, pos:frame.Coordinate, text:str, 
                 size:frame.Coordinate = const.COO.SIZE_STANDARD, 
                 textColor:str = None, textSize:int = -1, 
                 name:str = None, reset:int = 1):
        CityText.__init__(self, pos, text, size = size, textColor = textColor, textSize = textSize, 
                        name = name, reset = reset)
    
class CityTextAllTeam(CityText):
    def __init__(self, pos:frame.Coordinate, text:Union[list[str], str], 
                 size:frame.Coordinate = const.COO.SIZE_STANDARD, textColor:Union[list[str], str] = [], \
                 textSize:int = -1, name:Union[list[str], str] = [], actiBy_s_list:list[Union[list[object.TObject_One], object.TObject_One]] = [], 
                 deactiBy_s_list:list[Union[list[object.TObject_One], object.TObject_One]] = [], 
                 reset:int = 1):
        CityText.__init__(self, pos, text, size = size, textColor = textColor, textSize = textSize, 
                        name = name, actiBy_s_list = actiBy_s_list, deactiBy_s_list = deactiBy_s_list, 
                        reset = reset)