from typing import Union

import rwmap._object as object
import rwmap._frame as frame
import rwmap.data.tobject._tobject_one as tobject_one



class RefreshBuilding(object.TObject_Group):
    @classmethod
    def init_building(cls, pos: frame.Coordinate, size: frame.Coordinate, spawnUnits:str, id_detect:str, 
                  reset_add:int, reset_detect:int, name_add:str = None, name_detect:str = None, 
                  warmup_add:int = -1, warmup_detect:int = -1, techLevel:int = -1):
        uadd = tobject_one.unitAdd(pos, -1, spawnUnits, name = name_add, warmup = warmup_add, 
                                   reset = reset_add, techLevel = techLevel)
        udetect = tobject_one.unitDetect(pos, size, name = name_detect, maxUnits = 0, 
                                         unitType = spawnUnits, warmup = warmup_detect, reset = reset_detect, 
                                         id = id_detect)
        tobn = udetect.return_idTObject()
        uadd.add_actiBy([tobn])
        return cls([uadd, udetect])
    
    def return_idTObject(self)->Union[object.TObject_One, None]:
        return self._TObject_One_list[1].return_idTObject()
    
    def add_alsoacti(self, add_TObject_One:list[object.TObject_One] = []):
        self._TObject_One_list[1].add_alsoacti(add_TObject_One)

    def add_actiBy(self, add_TObject_One:list[object.TObject_One] = []):
        self._TObject_One_list[0].add_actiBy(add_TObject_One)

    def add_deactiBy(self, add_TObject_One:list[object.TObject_One] = []):
        self._TObject_One_list[0].add_deactiBy(add_TObject_One)