from copy import deepcopy
from typing import Union

import rwmap._object as object
import rwmap._frame as frame
import rwmap._data.tobject as tobject
import rwmap._data.const as const
import rwmap._exceptions as rwexceptions

import rwmap._util as utility

class ScoreText(object.TObject_Group):
    def __init__(self, pos:frame.Coordinate, num:int, textSize:int, 
                 prefix:str = "", 
                 size:frame.Coordinate = const.COO.SIZE_STANDARD, 
                 textColor:str = None, 
                 name:Union[list[str], str] = [], 
                 actiBy_s_list:list[Union[list[object.TObject_One], object.TObject_One]] = [], 
                 deactiBy_s_list:list[Union[list[object.TObject_One], object.TObject_One]] = [], 
                 reset:int = 1):
        name_now = utility.list_filling(name, num + 1, None)
        actiBy_s_list_now = utility.list_filling(actiBy_s_list, num + 1, [], istolist = True)
        deactiBy_s_list_now = utility.list_filling(deactiBy_s_list, num + 1, [], istolist = True)
        maptext = [tobject.MapText(pos, prefix + str(i), size = size, textColor = textColor, 
                                  textSize = textSize, name = name_now[i], actiBy_s = actiBy_s_list_now[i], 
                                  deactiBy_s = deactiBy_s_list_now[i], reset = reset) for i in range(num + 1)]

        object.TObject_Group.__init__(self, maptext)

    def mapText_s(self, index:int)->tobject.MapText:
        return self._TObject_One_list[index]
    
    def add_actiBy_s(self, index:int, actiBy_s:Union[list[object.TObject_One], object.TObject_One]):
        actiBy_s_list = deepcopy(utility.list_variable_s(actiBy_s))
        self.mapText_s(index).add_actiBy_s(actiBy_s_list)

    def add_deactiBy_s(self, index:int, deactiBy_s:list[object.TObject_One]):
        deactiBy_s_list = deepcopy(utility.list_variable_s(deactiBy_s))
        self.mapText_s(index).add_deactiBy_s(deactiBy_s_list)