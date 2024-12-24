from typing import Union

import rwmap._object as object
import rwmap._frame as frame
import rwmap._data.const as const

from rwmap._object._object_time import _make_tobject_time

class UnitAdd(object.TObject_One):
    def __init__(self, pos: frame.Coordinate, team:int, spawnUnits:str, size:frame.Coordinate = const.COO.SIZE_STANDARD, 
                 name:str = None, techLevel:int = -1, warmup:Union[float, int] = -1, reset:Union[float, int] = -1, 
                 isdelay:bool = False, isrepeat:bool = False, issecond = True, 
                 actiBy_s:list[object.TObject_One] = [], deactiBy_s:list[object.TObject_One] = [], 
                 isalltoacti:bool = False):
        upos = frame.Rectangle(pos, size)
        object.TObject_One.__init__(self, object.TObject_Type.init_unitAdd(team, spawnUnits, techLevel), 
                                    object.TObject_Pos.init_rectangle(upos), name, 
                                    object.TObject_Acti.init_acti(actiBy_s = actiBy_s, deactiBy_s = deactiBy_s, isalltoacti = isalltoacti), 
                                    _make_tobject_time(warmup = warmup, reset = reset, isdelay = isdelay, isrepeat = isrepeat, issecond = issecond))
