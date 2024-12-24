from copy import deepcopy
from typing import Union

import rwmap._object as object
import rwmap._frame as frame
import rwmap._data.tobject as tobject
import rwmap._data.const as const
import rwmap._exceptions as rwexceptions

import rwmap._util as utility

class Flash(object.TObject_Group):
    def __init__(self, pos: frame.Coordinate, delay:Union[int, float], 
                 pre_period:Union[int, float], period:Union[int, float], 
                 id:str, issecond:bool = True, 
                 size:frame.Coordinate = const.COO.SIZE_STANDARD * 2, 
                 name_add:str = None, name_detect:str = None, name_remove:str = None, 
                 units:str = const.UNIT.c_antiAirTurretT3, delayisdetect:bool = True, reset_detect = 0.25):
        uadd_s = tobject.UnitAdd(pos, -2, spawnUnits = units, size = size, 
                                 name = name_add, warmup = delay, reset = period, 
                                 isdelay = True, isrepeat = True)
        minUnits = -1 if delayisdetect else 1
        maxUnits = 0 if delayisdetect else -1
        udetect_s = tobject.UnitDetect(pos, size, name = name_detect, team = -2, 
                                       minUnits = minUnits, maxUnits = maxUnits, 
                                       unitType = units, reset = reset_detect, id = id, 
                                       issecond = issecond)

        uremove_s = tobject.UnitRemove(pos, size, name = name_remove, team = -2, 
                                       warmup = delay + pre_period, reset = period, 
                                       isdelay = True, isrepeat = True)
        object.TObject_Group.__init__(self, [uadd_s, uremove_s, udetect_s], [])

    def unitAdd_s(self)->tobject.UnitAdd:
        return self._TObject_One_list[0]
    
    def unitRemove_s(self)->tobject.UnitRemove:
        return self._TObject_One_list[1]
    
    def unitDetect_s(self)->tobject.UnitDetect:
        return self._TObject_One_list[2]

    def idTObject_s(self)->object.TObject_One:
        return self.unitDetect_s().idTObject_s()

