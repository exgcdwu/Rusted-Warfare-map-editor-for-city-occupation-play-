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
            pos_l = size_x * 2 * index + pos
            pos_b = size_x * 2 * index + pos + size_y * 2
            uadd_s.append(NormalUnitAddInstant(pos_l, team, "landFactory", size = size, name = name_l))
            uadd_s.append(NormalUnitAddInstant(pos_b, team, "builder", size = size, name = name_b))
        uremove_s = tobject.UnitRemove(pos, size_x * (2 * len(team_list) - 1) + size_y * 3, name = name_remove, actiBy_s = actiBy_s, 
                                       deactiBy_s = deactiBy_s, isalltoacti = isalltoacti)
        object.TObject_Group.__init__(self, [uremove_s], uadd_s)

    def unitRemove_s(self)->tobject.UnitRemove:
        return self._TObject_One_list[0]

    def add_actiBy_s(self, actiBy_s:Union[list[object.TObject_One], object.TObject_One]):
        actiBy_s_list = deepcopy(utility.list_variable_s(actiBy_s))
        self.unitRemove_s().add_actiBy_s(actiBy_s_list)

    def add_deactiBy_s(self, deactiBy_s:Union[list[object.TObject_One], object.TObject_One]):
        deactiBy_s_list = deepcopy(utility.list_variable_s(deactiBy_s))
        self.unitRemove_s().add_deactiBy_s(deactiBy_s_list)

    def add_twoactiBy_s(self, add_TObject_One_two_s:tuple[list[object.TObject_One], 
                                                          list[object.TObject_One]] = ([], [])):
        self.unitRemove_s().add_twoactiBy_s(add_TObject_One_two_s)

    def actiBy_s(self)->list[object.TObject_One]:
        return self.unitRemove_s()._acti._actiBy_s

    def deactiBy_s(self)->list[object.TObject_One]:
        return self.unitRemove_s()._acti._deactiBy_s

    def twoactiBy_s(self)->tuple[list[object.TObject_One], list[object.TObject_One]]:
        return [self.actiBy_s(), self.deactiBy_s()]





