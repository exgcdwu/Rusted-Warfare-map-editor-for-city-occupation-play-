import rwmap._object as object
import rwmap._frame as frame
import rwmap._data.const as const

class Camera(object.TObject_One):
    def __init__(self, pos:frame.Coordinate, size:frame.Coordinate = const.COO.SIZE_STANDARD):
        upos = frame.Rectangle(pos, size)
        object.TObject_One.__init__(self, object.TObject_Type.init_camera_start(), 
                                    object.TObject_Pos.init_rectangle(upos))