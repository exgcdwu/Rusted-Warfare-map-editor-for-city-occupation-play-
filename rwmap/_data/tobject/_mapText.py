import rwmap._object as object
import rwmap._frame as frame
import rwmap._data.const as const

class MapText(object.TObject_One):
    def __init__(self, pos:frame.Coordinate, text:str, size:frame.Coordinate = const.COO.SIZE_STANDARD, 
                 textColor:str = None, textSize:int = -1, name:str = None,
                 actiBy:list[object.TObject_One] = [], deactiBy:list[object.TObject_One] = [], 
                 isalltoacti:bool = False):
        upos = frame.Rectangle(pos - size / 2, size)
        object.TObject_One.__init__(self, object.TObject_Type.init_mapText(text, textColor = textColor, textSize = textSize), 
                                    object.TObject_Pos.init_rectangle(upos), name, 
                                    object.TObject_Acti.init_acti(actiBy = actiBy, deactiBy = deactiBy, isalltoacti = isalltoacti))

