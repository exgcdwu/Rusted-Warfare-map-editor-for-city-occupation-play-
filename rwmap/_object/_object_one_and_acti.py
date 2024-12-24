import xml.etree.ElementTree as et
from typing import Union
from copy import deepcopy

import rwmap._frame as frame
import rwmap._util as utility
import rwmap._data.const as const

from rwmap._object._object_pos import TObject_Pos
from rwmap._object._object_type import TObject_Type
from rwmap._object._object_time import TObject_Time
from rwmap._object._object_global import TObject_Global

class TObject_One:
    pass

class TObject_Acti:
    def __init__(self, idTObject_One_s:TObject_One = None, alsoacti_s:list[TObject_One] = [], 
                 actiBy_s:list[TObject_One] = [], deactiBy_s:list[TObject_One] = [], 
                 isalltoacti:bool = False):
        self._idTObject_One_s = idTObject_One_s
        self._alsoacti_s = alsoacti_s
        self._actiBy_s = actiBy_s
        self._deactiBy_s = deactiBy_s
        self._isalltoacti = isalltoacti

    @classmethod
    def init_acti(cls, id:str = None, alsoacti_s:list[TObject_One] = [], 
                 actiBy_s:list[TObject_One] = [], deactiBy_s:list[TObject_One] = [], 
                 isalltoacti:bool = False):
        return cls(TObject_One(TObject_Type({}), name = id) if id != None else None, alsoacti_s, actiBy_s, deactiBy_s, isalltoacti)

    def add_alsoacti_s(self, add_TObject_One_s:Union[list[TObject_One], TObject_One] = []):
        add_TObject_One_s_list = utility.list_variable_s(add_TObject_One_s)
        self._alsoacti_s = self._alsoacti_s + add_TObject_One_s_list

    def add_actiBy_s(self, add_TObject_One_s:Union[list[TObject_One], TObject_One] = []):
        add_TObject_One_s_list = utility.list_variable_s(add_TObject_One_s)
        self._actiBy_s = self._actiBy_s + add_TObject_One_s_list

    def add_deactiBy_s(self, add_TObject_One_s:Union[list[TObject_One], TObject_One] = []):
        add_TObject_One_s_list = utility.list_variable_s(add_TObject_One_s)
        self._deactiBy_s = self._deactiBy_s + add_TObject_One_s_list

    def add_twoactiBy_s(self, add_TObject_One_two_s:tuple[list[TObject_One], 
                                                          list[TObject_One]] = ([], [])):
        self.add_actiBy_s(add_TObject_One_two_s[0])
        self.add_deactiBy_s(add_TObject_One_two_s[1])

    def idTObject_s(self)->Union[TObject_One, None]:
        return self._idTObject_One_s

    def output_optional_properties(self)->dict[str, str]:
        op_dict = {}
        if self._idTObject_One_s != None:
            op_dict.update({"id": self._idTObject_One_s._name}) 
        if self._isalltoacti:
            op_dict.update({const.OBJECTOP.allToActivate: {"type": "bool", "value": "true"}}) 
            
        op_dict.update(utility.add_acti_pro(const.OBJECTOP.alsoActivate, self._alsoacti_s))
        op_dict.update(utility.add_acti_pro("activatedBy", self._actiBy_s))
        op_dict.update(utility.add_acti_pro("deactivatedBy", self._deactiBy_s))
        return op_dict

class TObject_One:
    def __init__(self, otype:TObject_Type, pos:TObject_Pos = TObject_Pos({}), name:str = None, 
                 acti:TObject_Acti = TObject_Acti(), time:TObject_Time = TObject_Time(),
                 nglobal:TObject_Global = TObject_Global()):
        self._name = deepcopy(name)
        self._pos = deepcopy(pos)
        self._otype = deepcopy(otype)
        self._acti = deepcopy(acti)
        self._time = deepcopy(time)
        self._global = deepcopy(nglobal)

    def default_properties(self)->dict[str, str]:
        dict_ans = {}
        if self._name != None:
            dict_ans.update({"name": self._name})
        dict_ans.update({**self._pos.output_default_properties(), **self._otype.output_default_properties()})
        return dict_ans
    
    def offset(self, offset:frame.Coordinate)->TObject_One:
        ntob = deepcopy(self)
        ntob._pos = ntob._pos.offset(offset)
        return ntob

    def optional_properties(self)->dict[str, Union[str, dict[str, str]]]:
        return {**self._otype.output_optional_properties(), 
                **self._acti.output_optional_properties(),
                **self._time.output_optional_properties(), 
                **self._global.output_optional_properties()}
    
    def other_properties(self)->list[et.Element]:
        return self._pos.output_other_properties()
    
    def idTObject_s(self)->Union[TObject_One, None]:
        return self._acti.idTObject_s()
    
    def add_alsoacti_s(self, add_TObject_One_s:list[TObject_One] = []):
        self._acti.add_alsoacti_s(add_TObject_One_s)

    def add_actiBy_s(self, add_TObject_One_s:list[TObject_One] = []):
        self._acti.add_actiBy_s(add_TObject_One_s)

    def add_deactiBy_s(self, add_TObject_One_s:list[TObject_One] = []):
        self._acti.add_deactiBy_s(add_TObject_One_s)

    def add_twoactiBy_s(self, add_TObject_One_two_s:tuple[list[TObject_One], 
                                                          list[TObject_One]] = ([], [])):
        self._acti.add_twoactiBy_s(add_TObject_One_two_s)


