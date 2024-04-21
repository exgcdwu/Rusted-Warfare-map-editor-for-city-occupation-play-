import xml.etree.ElementTree as et
from typing import Union

import rwmap._frame as frame
import rwmap._util as utility

from rwmap._object._object_pos import TObject_Pos
from rwmap._object._object_type import TObject_Type
from rwmap._object._object_time import TObject_Time
from rwmap._object._object_global import TObject_Global

from copy import deepcopy

class TObject_One:
    pass

class TObject_Acti:
    def __init__(self, idTObject_One:TObject_One = None, alsoacti:list[TObject_One] = [], 
                 actiBy:list[TObject_One] = [], deactiBy:list[TObject_One] = [], 
                 isalltoacti:bool = False):
        self._idTObject_One = idTObject_One
        self._alsoacti = alsoacti
        self._actiBy = actiBy
        self._deactiBy = deactiBy
        self._isalltoacti = isalltoacti

    @classmethod
    def init_acti(cls, id:str = None, alsoacti:list[TObject_One] = [], 
                 actiBy:list[TObject_One] = [], deactiBy:list[TObject_One] = [], 
                 isalltoacti:bool = False):
        return cls(TObject_One(TObject_Type({}), name = id) if id != None else None, alsoacti, actiBy, deactiBy, isalltoacti)

    def add_alsoacti(self, add_TObject_One:list[TObject_One] = []):
        self._alsoacti = self._alsoacti + add_TObject_One

    def add_actiBy(self, add_TObject_One:list[TObject_One] = []):
        self._actiBy = self._actiBy + add_TObject_One

    def add_deactiBy(self, add_TObject_One:list[TObject_One] = []):
        self._deactiBy = self._deactiBy + add_TObject_One

    def return_idTObject(self)->Union[TObject_One, None]:
        return self._idTObject_One

    def output_optional_properties(self)->dict[str, str]:
        op_dict = {}
        if self._idTObject_One != None:
            op_dict.update({"id": self._idTObject_One._name}) 
        if self._isalltoacti:
            op_dict.update({"allToActivate": "1"}) 
        op_dict.update(utility.add_acti_pro("alsoActivate", self._alsoacti))
        op_dict.update(utility.add_acti_pro("activatedBy", self._actiBy))
        op_dict.update(utility.add_acti_pro("deactivatedBy", self._deactiBy))
        return op_dict

class TObject_One:
    def __init__(self, otype:TObject_Type, pos:TObject_Pos = TObject_Pos({}), name:str = None, 
                 acti:TObject_Acti = TObject_Acti(), time:TObject_Time = TObject_Time(),
                 nglobal:TObject_Global = TObject_Global()):
        self._name = name
        self._pos = pos
        self._otype = otype
        self._acti = acti
        self._time = time
        self._global = nglobal

    def default_properties(self)->dict[str, str]:
        dict_ans = {}
        if self._name != None:
            dict_ans = dict_ans.update({"name": self._name})
        dict_ans = {**self._pos.output_default_properties(), **self._otype.output_default_properties()}
        return dict_ans
    
    def offset(self, offset:frame.Coordinate)->TObject_One:
        ntob = deepcopy(self)
        ntob._pos = ntob._pos.offset(offset)
        return ntob

    def optional_properties(self)->dict[str, str]:
        return {**self._otype.output_optional_properties(), 
                **self._acti.output_optional_properties(),
                **self._time.output_optional_properties(), 
                **self._global.output_optional_properties()}
    
    def other_properties(self)->list[et.Element]:
        return self._pos.output_other_properties()
    
    def return_idTObject(self)->Union[TObject_One, None]:
        return self._acti.return_idTObject()
    
    def add_alsoacti(self, add_TObject_One:list[TObject_One] = []):
        self._acti.add_alsoacti(add_TObject_One)

    def add_actiBy(self, add_TObject_One:list[TObject_One] = []):
        self._acti.add_actiBy(add_TObject_One)

    def add_deactiBy(self, add_TObject_One:list[TObject_One] = []):
        self._acti.add_deactiBy(add_TObject_One)


