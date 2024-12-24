from copy import deepcopy
from typing import Union

import rwmap._object as object
import rwmap._frame as frame
import rwmap._data.tobject as tobject
import rwmap._data.const as const
import rwmap._exceptions as rwexceptions

import rwmap._util as utility

class Count(object.TObject_Group):
    def __init__(self, pos: frame.Coordinate, reset_detect:Union[int, float], 
                 reset_add:Union[int, float], reset_remove:Union[int, float], 
                 id:str, issecond:bool = True, 
                 size:frame.Coordinate = const.COO.SIZE_STANDARD, 
                 name_add:str = None, name_detect:str = None, name_remove:str = None, 
                 count_num:int = 1, units:str = const.UNIT.c_antiAirTurretT3):
        self._size = size
        self._count_num = count_num
        uadd_s = tobject.UnitAdd(pos, -2, spawnUnits = units + "*" + str(count_num), size = size, 
                                 name = name_add, reset = reset_add, issecond = issecond)

        udetect_s = tobject.UnitDetect(pos, size, name = name_detect, team = -2, 
                                       minUnits = 1, maxUnits = -1, 
                                       unitType = units, reset = reset_detect, id = id, 
                                       issecond = issecond)
        

        uremove_s = tobject.UnitRemove(pos, size, name = name_remove, team = -2, 
                                       reset = reset_remove)
        uadd_s.add_deactiBy_s(udetect_s.idTObject_s())

        object.TObject_Group.__init__(self, [uadd_s, uremove_s, udetect_s], [])

    def size(self)->frame.Coordinate:
        return self._size

    def count_num(self)->int:
        return self._count_num

    def unitAdd_s(self)->tobject.UnitAdd:
        return self._TObject_One_list[0]
    
    def unitRemove_s(self)->tobject.UnitRemove:
        return self._TObject_One_list[1]
    
    def unitDetect_s(self)->tobject.UnitDetect:
        return self._TObject_One_list[2]

    def idTObject_s(self)->list[object.TObject_One]:
        return self.unitDetect_s().idTObject_s()

    def add_actiBy_s(self, actiBy_s:Union[list[object.TObject_One], object.TObject_One]):
        actiBy_s_list = deepcopy(utility.list_variable_s(actiBy_s))
        self.unitRemove_s().add_deactiBy_s(actiBy_s_list)

    def add_deactiBy_s(self, deactiBy_s:list[object.TObject_One]):
        deactiBy_s_list = deepcopy(utility.list_variable_s(deactiBy_s))
        self.unitAdd_s().add_deactiBy_s(deactiBy_s_list)

class ManyCount(object.TObject_Group):
    def __init__(self, pos:frame.Coordinate, num:int, 
                 reset_detect:Union[int, float], 
                 reset_add:Union[int, float], reset_remove:Union[int, float], 
                 id_list:list[str], id_list_count_more:list[str], 
                 id_list_count_less:list[str], issecond:bool = True, 
                 size:frame.Coordinate = const.COO.SIZE_STANDARD * 2, 
                 name_count_more:list[str] = [], name_count_less:list[str] = [],
                 name_add:list[str] = [], name_detect:list[str] = [], name_remove:list[str] = [], 
                 count_num:int = [], units:str = const.UNIT.c_antiAirTurretT3):
        '''
        id_list/name_add/name_detect/name_remove:num
        id_list_count_more/id_list_count_less/name_count_more/name_count_less::sum(count_num) + 1
        '''
        self._site_num = num
        self._count_num_list = count_num + [1 for i in range(num - len(count_num))]
        self._count_total = sum(self._count_num_list)
        self._size = frame.Coordinate(size.x() * self._site_num, size.y())

        many_count = [Count(pos + frame.Coordinate(size.x() * i, 0), reset_detect, reset_add, reset_remove, 
                            id_list[i], issecond = issecond, size = size, name_add = utility.list_get_s(name_add, i), 
                            name_detect = utility.list_get_s(name_detect, i), name_remove = utility.list_get_s(name_remove, i), 
                            count_num = self._count_num_list[i], units = units) for i in range(self._site_num)]

        count_now_more = [tobject.UnitDetect(pos, self._size, 
                                        utility.list_get_s(name_count_more, i), team = -2, 
                                        minUnits = i, maxUnits = -1, 
                                        unitType = units, reset = reset_detect, id = id_list_count_more[i])
                                        for i in range(self._count_total + 1)]
        count_now_less = [tobject.UnitDetect(pos, self._size, 
                                utility.list_get_s(name_count_less, i), team = -2, 
                                minUnits = -1, maxUnits = i, 
                                unitType = units, reset = reset_detect, id = id_list_count_less[i])
                                for i in range(self._count_total + 1)]

        object.TObject_Group.__init__(self, count_now_more + count_now_less, many_count)

    def count_num(self, index:int)->int:
        return self._count_num_list[index]
    
    def site_num(self, index:int)->int:
        return self._site_num[index]

    def size(self)->frame.Coordinate:
        return self._size
    
    def count_total(self)->int:
        return self._count_total

    def Count_geq_idObject_s(self, num:int)->object.TObject_One:
        return self._TObject_One_list[num].idTObject_s()

    def Count_leq_idObject_s(self, num:int)->object.TObject_One:
        return self._TObject_One_list[num + self.count_total() + 1].idTObject_s()

    def Count_s(self, index:int)->Count:
        return self._TObject_Group_list[index]
    

