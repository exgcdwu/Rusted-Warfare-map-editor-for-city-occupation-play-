import rwmap._object as object
import rwmap._frame as frame

SIZE_STANDARD = frame.Coordinate(20, 20)

def node(pos:frame.Coordinate, name:str = None, warmup:int = -1, reset:int = -1, 
         id:str = None, alsoacti:list[object.TObject_One] = [], 
         actiBy:list[object.TObject_One] = [], deactiBy:list[object.TObject_One] = [], 
         isalltoacti:bool = False):
    upos = frame.Rectangle(pos - SIZE_STANDARD / 2, SIZE_STANDARD)
    return object.TObject_One(object.TObject_Type.init_node(), 
                              object.TObject_Pos.init_rectangle(upos), 
                              name, object.TObject_Acti.init_acti(id = id, alsoacti = alsoacti, 
                                                                  actiBy = actiBy, deactiBy = deactiBy, 
                                                                  isalltoacti = isalltoacti), 
                              object.TObject_Time.init_time(warmup = warmup, reset = reset))


def unitAdd(pos: frame.Coordinate, team:int, spawnUnits:str, name:str = None, 
            techLevel:int = -1, warmup:int = -1, reset:int = -1, 
            actiBy:list[object.TObject_One] = [], deactiBy:list[object.TObject_One] = [], 
            isalltoacti:bool = False):
    upos = frame.Rectangle(pos - SIZE_STANDARD / 2, SIZE_STANDARD)
    return object.TObject_One(object.TObject_Type.init_unitAdd(team, spawnUnits, techLevel), 
                              object.TObject_Pos.init_rectangle(upos), name, 
                              object.TObject_Acti.init_acti(actiBy = actiBy, deactiBy = deactiBy, isalltoacti = isalltoacti), 
                              object.TObject_Time.init_time(warmup = warmup, reset = reset))

def unitDetect(pos:frame.Coordinate, size:frame.Coordinate, name:str = None,
               team:int = None, minUnits:int = None, maxUnits:int = None, 
               unitType:str = None, onlyList:list[str] = [], warmup:int = -1, reset:int = -1, 
               id:str = None, alsoacti:list[object.TObject_One] = []):
    upos = frame.Rectangle(pos - size / 2, size)
    return object.TObject_One(object.TObject_Type.init_unitDetect(team = team, minUnits = minUnits, maxUnits = maxUnits, 
                                                                  unitType = unitType, onlyList = onlyList), 
                              object.TObject_Pos.init_rectangle(upos), 
                              name, object.TObject_Acti.init_acti(id = id, alsoacti = alsoacti), 
                              object.TObject_Time.init_time(warmup = warmup, reset = reset))
    
def unitRemove(pos:frame.Coordinate, size:frame.Coordinate, name:str = None, team:int = None, 
               warmup:int = -1, reset:int = -1, actiBy:list[object.TObject_One] = [], 
               deactiBy:list[object.TObject_One] = [], isalltoacti:bool = False):
    upos = frame.Rectangle(pos - size / 2, size)
    return object.TObject_One(object.TObject_Type.init_unitRemove(team), 
                              object.TObject_Pos.init_rectangle(upos), 
                              name, object.TObject_Acti.init_acti(actiBy = actiBy, deactiBy = deactiBy, isalltoacti = isalltoacti), 
                              object.TObject_Time.init_time(warmup = warmup, reset = reset))

def mapText(pos:frame.Coordinate, text:str, textColor:str = None, textSize:int = -1, name:str = None,
            actiBy:list[object.TObject_One] = [], deactiBy:list[object.TObject_One] = [], 
            isalltoacti:bool = False):
    upos = frame.Rectangle(pos - SIZE_STANDARD / 2, SIZE_STANDARD)
    return object.TObject_One(object.TObject_Type.init_mapText(text, textColor = textColor, textSize = textSize), 
                              object.TObject_Pos.init_rectangle(upos), name, 
                              object.TObject_Acti.init_acti(actiBy = actiBy, deactiBy = deactiBy, isalltoacti = isalltoacti))

def message(pos:frame.Coordinate, message:str, delayPerChar:int = -1, textColor:str = None, 
            name:str = None, warmup:int = -1, reset:int = -1, 
            actiBy:list[object.TObject_One] = [], deactiBy:list[object.TObject_One] = [], 
            isalltoacti:bool = False):
    upos = frame.Rectangle(pos - SIZE_STANDARD / 2, SIZE_STANDARD)
    return object.TObject_One(object.TObject_Type.init_mapText(None), 
                              object.TObject_Pos.init_rectangle(upos), 
                              name, object.TObject_Acti.init_acti(actiBy = actiBy, deactiBy = deactiBy, isalltoacti = isalltoacti), 
                              object.TObject_Time.init_time(warmup = warmup, reset = reset), 
                              object.TObject_Global.init_global(message = message, 
                                                                delayPerChar = delayPerChar, textColor = textColor))

def credit(pos:frame.Coordinate, setCredits:int = None, addCredits:int = None, 
           name:str = None, warmup:int = -1, reset:int = -1, 
           actiBy:list[object.TObject_One] = [], deactiBy:list[object.TObject_One] = [], 
           isalltoacti:bool = False):
    upos = frame.Rectangle(pos - SIZE_STANDARD / 2, SIZE_STANDARD)
    return object.TObject_One(object.TObject_Type.init_changeCredits(setCredits = setCredits, addCredits = addCredits), 
                              object.TObject_Pos.init_rectangle(upos), name, 
                              object.TObject_Acti.init_acti(actiBy = actiBy, deactiBy = deactiBy, isalltoacti = isalltoacti), 
                              object.TObject_Time.init_time(warmup = warmup, reset = reset))

def mapinfo(pos:frame.Coordinate, mapType:str, mapFog:str, winCondition:str, text:str = None):
    upos = frame.Rectangle(pos - SIZE_STANDARD / 2, SIZE_STANDARD)
    return object.TObject_One(object.TObject_Type.init_mapinfo(mapType = mapType, mapFog = mapFog, 
                                                               winCondition = winCondition, text = text), 
                              object.TObject_Pos.init_rectangle(upos))

def camera(pos:frame.Coordinate):
    upos = frame.Rectangle(pos - SIZE_STANDARD / 2, SIZE_STANDARD)
    return object.TObject_One(object.TObject_Type.init_camera_start(), 
                              object.TObject_Pos.init_rectangle(upos))

