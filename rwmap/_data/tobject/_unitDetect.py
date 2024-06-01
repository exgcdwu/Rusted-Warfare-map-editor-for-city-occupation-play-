import rwmap._object as object
import rwmap._frame as frame
import rwmap._data.const as const

from rwmap._object._object_time import _make_tobject_time

class UnitDetect(object.TObject_One):
    def __init__(self, pos:frame.Coordinate, size:frame.Coordinate, name:str = None,
                 team:int = None, minUnits:int = None, maxUnits:int = None, 
                 unitType:str = None, onlyList:list[str] = [], warmup:int = -1, reset:int = -1, 
                 isdelay:bool = False, isrepeat:bool = False, 
                 id:str = None, alsoacti_s:list[object.TObject_One] = [], issecond:bool = True):
        upos = frame.Rectangle(pos, size)
        object.TObject_One.__init__(self, object.TObject_Type.init_unitDetect(team = team, minUnits = minUnits, maxUnits = maxUnits, 
                                                                              unitType = unitType, onlyList = onlyList), 
                                    object.TObject_Pos.init_rectangle(upos), 
                                    name, object.TObject_Acti.init_acti(id = id, alsoacti_s = alsoacti_s), 
                                    _make_tobject_time(warmup = warmup, reset = reset, isdelay = isdelay, isrepeat = isrepeat, issecond = issecond))
