from typing import Union
from copy import deepcopy


def dict_isconflict(a:dict, b:dict)->None:
    for an, av in a.items():
        if b.get(an) != None and av != b[an]:
            return True
    return False

def udictstr_to_dict(input:Union[dict[str, str], str])->Union[dict[str, str], list[dict[str, str], str]]:
    if isinstance(input, str):
        return {"value":input}
    else:
        if input.get("text") != None:
            input_t = deepcopy(input)
            input_t.pop("text")
            return [input_t, input["text"]]
        else:
            return input