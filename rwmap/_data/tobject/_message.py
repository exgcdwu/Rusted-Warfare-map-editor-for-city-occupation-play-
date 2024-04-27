import rwmap._object as object
import rwmap._frame as frame
import rwmap._data.const as const

class Message(object.TObject_One):
    def __init__(self, pos:frame.Coordinate, message:str, size:frame.Coordinate = const.COO.SIZE_STANDARD, 
                 delayPerChar:int = -1, textColor:str = None, 
                 name:str = None, warmup:int = -1, reset:int = -1, 
                 actiBy_s:list[object.TObject_One] = [], deactiBy_s:list[object.TObject_One] = [], 
                 isalltoacti:bool = False):
        upos = frame.Rectangle(pos - size / 2, size)
        object.TObject_One.__init__(self, object.TObject_Type.init_mapText(None), 
                                    object.TObject_Pos.init_rectangle(upos), 
                                    name, object.TObject_Acti.init_acti(actiBy_s = actiBy_s, deactiBy_s = deactiBy_s, isalltoacti = isalltoacti), 
                                    object.TObject_Time.init_time(warmup = warmup, reset = reset), 
                                    object.TObject_Global.init_global(message = message, 
                                                                      delayPerChar = delayPerChar, textColor = textColor))