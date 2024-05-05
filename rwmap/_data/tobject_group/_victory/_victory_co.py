from copy import deepcopy
from typing import Union

import rwmap._object as object
import rwmap._frame as frame
import rwmap._data.tobject as tobject
import rwmap._data.const as const
import rwmap._exceptions as rwexceptions

import rwmap._util as utility
from rwmap._data.tobject_group._city._normal_unit_add import NormalUnitAddInstant

class VictoryCO(object.TObject_Group):
    def __init__(self, pos:frame.Coordinate, team_list:list[int], 
                 name_add_b_list:list[str] = [], 
                 name_add_l_list:list[str] = [], 
                 name_remove:str = None, actiBy_s:list[object.TObject_One] = [], 
                 deactiBy_s:list[object.TObject_One] = [], isalltoacti:bool = False):
        size:frame.Coordinate = const.COO.SIZE_STANDARD
        uadd_s = []
        size_x = frame.Coordinate(size.x(), 0)
        size_y = frame.Coordinate(0, size.y())
        for index, team in enumerate(team_list):
            name_l = name_add_l_list[index] if index < len(name_add_l_list) else None
            name_b = name_add_b_list[index] if index < len(name_add_b_list) else None
            pos_l = 2 * index * size_x + pos
            pos_b = 2 * index * size_x + pos + 2 * size_y
            uadd_s.append(NormalUnitAddInstant(pos_l, team, "landFactory", size = size, name = name_l))
            uadd_s.append(NormalUnitAddInstant(pos_b, team, "builder", size = size, name = name_b))
        uremove_s = tobject.UnitRemove(pos, (2 * len(team_list) - 1) * size_x + 3 * size_y, name = name_remove, actiBy_s = actiBy_s, 
                                       deactiBy_s = deactiBy_s, isalltoacti = isalltoacti)
        object.TObject_Group.__init__(self, [], uadd_s + [uremove_s])

    def unitRemove_s(self)->tobject.UnitRemove:
        return self._TObject_Group_list[-1]

    def add_actiBy_s(self, actiBy_s:Union[list[object.TObject_One], object.TObject_One]):
        actiBy_s_list = deepcopy(utility.list_variable_s(actiBy_s))
        self.unitRemove_s().add_actiBy_s(actiBy_s_list)

    def add_deactiBy_s(self, deactiBy_s:Union[list[object.TObject_One], object.TObject_One]):
        deactiBy_s_list = deepcopy(utility.list_variable_s(deactiBy_s))
        self.unitRemove_s().add_deactiBy_s(deactiBy_s_list)

    def add_twoactiBy_s(self, add_TObject_One_two_s:tuple[list[object.TObject_One], 
                                                          list[object.TObject_One]] = ([], [])):
        self.unitRemove_s().add_twoactiBy_s(add_TObject_One_two_s)





