import rwmap._object as object
import rwmap._frame as frame

class UnitRemove(object.TObject_One):
    def __init__(self, pos:frame.Coordinate, size:frame.Coordinate, name:str = None, team:int = None, 
               warmup:int = -1, reset:int = -1, actiBy:list[object.TObject_One] = [], 
               deactiBy:list[object.TObject_One] = [], isalltoacti:bool = False):
        upos = frame.Rectangle(pos - size / 2, size)
        object.TObject_One.__init__(self, object.TObject_Type.init_unitRemove(team), 
                                    object.TObject_Pos.init_rectangle(upos), 
                                    name, object.TObject_Acti.init_acti(actiBy = actiBy, deactiBy = deactiBy, isalltoacti = isalltoacti), 
                                    object.TObject_Time.init_time(warmup = warmup, reset = reset))
