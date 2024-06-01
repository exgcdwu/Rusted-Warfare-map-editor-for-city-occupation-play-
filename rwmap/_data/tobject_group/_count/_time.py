from copy import deepcopy
from typing import Union

import rwmap._object as object
import rwmap._frame as frame
import rwmap._data.tobject as tobject
import rwmap._data.const as const
import rwmap._exceptions as rwexceptions

import rwmap._util as utility

class TimeDelay(object.TObject_Group):
    def __init__(self, pos: frame.Coordinate, delay:Union[int, float], 
                 id:str, issecond:bool = True, 
                 size:frame.Coordinate = const.COO.SIZE_STANDARD * 2, 
                 name_add:str = None, name_detect:str = None, 
                 units:str = const.UNIT.c_antiAirTurretT3, isacti_delay:bool = True, 
                 reset_detect:int = 1):
        uadd_s = tobject.UnitAdd(pos, -2, spawnUnits = units, size = size, 
                                 name = name_add, warmup = delay, issecond = issecond)
        minUnits = -1 if isacti_delay else 0
        maxUnits = 0 if isacti_delay else -1
        udetect_s = tobject.UnitDetect(pos, size, name = name_detect, team = -2, 
                                       minUnits = minUnits, maxUnits = maxUnits, 
                                       unitType = units, id = id, 
                                       issecond = issecond, reset = reset_detect)
        object.TObject_Group.__init__(self, [uadd_s, udetect_s], [])

    def unitAdd_s(self)->tobject.UnitAdd:
        return self._TObject_One_list[0]
    
    def unitDetect_s(self)->tobject.UnitDetect:
        return self._TObject_One_list[1]

    def idTObject_s(self)->list[object.TObject_One]:
        return self.unitDetect_s().idTObject_s()

