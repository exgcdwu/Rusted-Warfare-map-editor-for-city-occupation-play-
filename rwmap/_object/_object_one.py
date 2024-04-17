import xml.etree.ElementTree as et

from rwmap._object._object_pos import TObject_Pos
from rwmap._object._object_pro import TObject_Pro

class TObjectOri:
    pass

class TObject_One(TObjectOri):
    def __init__(self, pos:TObject_Pos, pro:TObject_Pro):
        self._pos = pos
        self._pro = pro

    def default_properties(self)->dict[str, str]:
        dict_ans = {**self._pos.output_default_properties(), **self._pro.output_default_properties}
        return dict_ans
    
    def optional_properties(self)->dict[str, str]:
        return self._pro.output_optional_properties()
    
    def other_properties(self)->list[et.Element]:
        return self._pos.output_other_properties()
