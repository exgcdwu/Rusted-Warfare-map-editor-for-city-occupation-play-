from copy import deepcopy
from typing import Union

import rwmap._object as object
import rwmap._frame as frame
import rwmap._data.tobject as tobject
import rwmap._data.const as const
import rwmap._exceptions as rwexceptions

import rwmap._util as utility
from rwmap._data.tobject_group._city._normal_unit_add import NormalUnitAdd
from rwmap._data.tobject_group._city._refresh_building import RefreshBuilding, RefreshBuildingAllTeam, RefreshBuildingAllTeamGroup

class RefreshTroop(NormalUnitAdd):
    def __init__(self, pos:frame.Coordinate, team:int, spawnUnits:str, 
                 warmup:int, reset:int, spawnUnitsnum:int = 1,
                 size:frame.Coordinate = const.COO.SIZE_STANDARD, name:str = None, 
                 actiBy_s:Union[list[object.TObject_One], object.TObject_One] = [], 
                 deactiBy_s:Union[list[object.TObject_One], object.TObject_One] = []):
        nspawnUnits = spawnUnits + '*' + str(spawnUnitsnum)
        NormalUnitAdd.__init__(self, pos, team, nspawnUnits, size = size, name = name, 
                               warmup = warmup, reset = reset, actiBy_s = actiBy_s, 
                               deactiBy_s = deactiBy_s)


