import rwmap._util as utility

class TObject_Time:
    def __init__(self, optional_properties:dict[str, str] = {}):
        self._optional_properties = optional_properties

    def output_optional_properties(self):
        return self._optional_properties
    
    @classmethod
    def init_time(cls, warmup:int = -1, delay:int = -1, reset:int = -1, repeat:int = -1, issecond:bool = True):
        op_dict = {}
        op_dict.update(utility.add_time_pro("warmup", warmup))
        op_dict.update(utility.add_time_pro("delay", delay))
        op_dict.update(utility.add_time_pro("resetActivationAfter", reset))
        op_dict.update(utility.add_time_pro("repeatDelay", repeat))
        return cls(op_dict)