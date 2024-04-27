from typing import Union


def dict_isconflict(a:dict, b:dict)->None:
    for an, av in a.items():
        if b.get(an) != None and av != b[an]:
            return True
    return False

def udictstr_to_dict(input:Union[dict[str, str], str])->dict[str, str]:
    if isinstance(input, str):
        return {"value":input}
    else:
        return input