import rwmap._object as object
import rwmap._frame as frame
import rwmap._data.const as const

class Auto(object.TObject_One):
    def __init__(self, name:str, pos:frame.Coordinate = const.COO.SIZE_ZERO, size:frame.Coordinate = const.COO.SIZE_STANDARD):
        upos = frame.Rectangle(pos, size)
        object.TObject_One.__init__(self, object.TObject_Type.init_none(), 
                                    object.TObject_Pos.init_rectangle(upos), name = name)