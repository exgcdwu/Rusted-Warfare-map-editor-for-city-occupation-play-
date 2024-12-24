import rwmap._util as utility
from copy import deepcopy

class TObject_Global:
    def __init__(self, optional_properties:dict[str, str] = {}):
        self._optional_properties = deepcopy(optional_properties)

    def output_optional_properties(self):
        return deepcopy(self._optional_properties)
    
    @classmethod
    def init_global(cls, message:str, delayPerChar:float = -1, textColor:str = None, issecond:bool = True):
        op_dict = {}
        op_dict.update({"globalMessage": message})
        op_dict.update(utility.add_time_pro("globalMessage_delayPerChar", delayPerChar, issecond))
        op_dict.update(utility.add_str_pro("globalMessage_textColor", textColor))
        return cls(op_dict)