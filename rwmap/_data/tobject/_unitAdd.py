import rwmap._object as object
import rwmap._frame as frame
import rwmap._data.const as const

class UnitAdd(object.TObject_One):
    def __init__(self, pos: frame.Coordinate, team:int, spawnUnits:str, size:frame.Coordinate = const.COO.SIZE_STANDARD, 
                 name:str = None, techLevel:int = -1, warmup:int = -1, reset:int = -1, 
                 actiBy:list[object.TObject_One] = [], deactiBy:list[object.TObject_One] = [], 
                 isalltoacti:bool = False):
        upos = frame.Rectangle(pos - size / 2, size)
        object.TObject_One.__init__(self, object.TObject_Type.init_unitAdd(team, spawnUnits, techLevel), 
                                    object.TObject_Pos.init_rectangle(upos), name, 
                                    object.TObject_Acti.init_acti(actiBy = actiBy, deactiBy = deactiBy, isalltoacti = isalltoacti), 
                                    object.TObject_Time.init_time(warmup = warmup, reset = reset))
