import rwmap._object as object
import rwmap._frame as frame
import rwmap._data.const as const

class MapText(object.TObject_One):
    def __init__(self, pos:frame.Coordinate, text:str, size:frame.Coordinate = const.COO.SIZE_STANDARD, 
                 textColor:str = None, textSize:int = -1, name:str = None,
                 actiBy_s:list[object.TObject_One] = [], deactiBy_s:list[object.TObject_One] = [], 
                 isalltoacti:bool = False, reset:int = 1):
        upos = frame.Rectangle(pos, size)
        object.TObject_One.__init__(self, object.TObject_Type.init_mapText(text, textColor = textColor, textSize = textSize), 
                                    object.TObject_Pos.init_rectangle(upos), name, 
                                    object.TObject_Acti.init_acti(actiBy_s = actiBy_s, deactiBy_s = deactiBy_s, isalltoacti = isalltoacti), 
                                    object.TObject_Time.init_time(reset = reset))

