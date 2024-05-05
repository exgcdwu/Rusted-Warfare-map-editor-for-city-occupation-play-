import rwmap._object as object
import rwmap._frame as frame
import rwmap._data.const as const

class Mapinfo(object.TObject_One):
    def __init__(self, pos:frame.Coordinate, mapType:str, mapFog:str, 
                 winCondition:str, size:frame.Coordinate = const.COO.SIZE_STANDARD, 
                 text:str = None):
        upos = frame.Rectangle(pos, size)
        object.TObject_One.__init__(self, object.TObject_Type.init_mapinfo(mapType = mapType, mapFog = mapFog, 
                                                                           winCondition = winCondition, text = text), 
                                    object.TObject_Pos.init_rectangle(upos))
