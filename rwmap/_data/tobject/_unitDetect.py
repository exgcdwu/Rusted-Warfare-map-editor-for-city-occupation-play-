import rwmap._object as object
import rwmap._frame as frame
import rwmap._data.const as const

class UnitDetect(object.TObject_One):
    def __init__(self, pos:frame.Coordinate, size:frame.Coordinate, name:str = None,
                 team:int = None, minUnits:int = None, maxUnits:int = None, 
                 unitType:str = None, onlyList:list[str] = [], warmup:int = -1, reset:int = -1, 
                 id:str = None, alsoacti:list[object.TObject_One] = []):
        upos = frame.Rectangle(pos - size / 2, size)
        object.TObject_One.__init__(self, object.TObject_Type.init_unitDetect(team = team, minUnits = minUnits, maxUnits = maxUnits, 
                                                                              unitType = unitType, onlyList = onlyList), 
                                    object.TObject_Pos.init_rectangle(upos), 
                                    name, object.TObject_Acti.init_acti(id = id, alsoacti = alsoacti), 
                                    object.TObject_Time.init_time(warmup = warmup, reset = reset))
