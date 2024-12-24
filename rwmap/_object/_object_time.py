from copy import deepcopy
from typing import Union

import rwmap._util as utility

class TObject_Time:
    def __init__(self, optional_properties:dict[str, str] = {}):
        self._optional_properties = deepcopy(optional_properties)

    def output_optional_properties(self):
        return deepcopy(self._optional_properties)
    
    @classmethod
    def init_time(cls, warmup:Union[int, float] = -1, delay:Union[int, float] = -1, 
                  reset:Union[int, float] = -1, repeat:Union[int, float] = -1, 
                  repeatcount:int = -1, issecond:bool = True):
        if repeat == -1 and repeatcount != -1:
            raise ValueError("repeatDelay is none but repeatDelay exists.")
        op_dict = {}
        op_dict.update(utility.add_time_pro("warmup", warmup, issecond = issecond))
        op_dict.update(utility.add_time_pro("delay", delay, issecond = issecond))
        op_dict.update(utility.add_time_pro("resetActivationAfter", reset, issecond = issecond))
        op_dict.update(utility.add_time_pro("repeatDelay", repeat, issecond = issecond))
        op_dict.update(utility.add_time_pro("repeatCount", repeatcount))
        return cls(op_dict)
    
def _make_tobject_time(warmup:Union[int, float] = -1, reset:Union[int, float] = -1, 
                       isdelay:bool = False, isrepeat:bool = False, repeatcount:int = -1, issecond:bool = True):
    warmup_n = -1 if isdelay else warmup
    reset_n = -1 if isrepeat else reset
    delay_n = warmup if isdelay else -1
    repeat_n = reset if isrepeat else -1
    return TObject_Time.init_time(warmup = warmup_n, delay = delay_n, reset = reset_n, repeat = repeat_n, issecond = issecond)
