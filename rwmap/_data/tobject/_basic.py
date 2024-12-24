import rwmap._object as object
import rwmap._frame as frame
import rwmap._data.const as const

class Basic(object.TObject_One):
    def __init__(self, pos:frame.Coordinate, name:str, size:frame.Coordinate = const.COO.SIZE_STANDARD, reset:int = 1):
        upos = frame.Rectangle(pos, size)
        object.TObject_One.__init__(self, object.TObject_Type.init_basic(), pos = object.TObject_Pos.init_rectangle(upos), 
                                    name = name, time = object.TObject_Time.init_time(reset = reset))