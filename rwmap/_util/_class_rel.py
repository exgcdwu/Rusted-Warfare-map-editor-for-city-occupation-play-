import rwmap._frame as frame
from rwmap._frame._element_ori import ElementOri
from rwmap._exceptions import ElementOriFoundMultiError, ElementOriNotFoundError
import regex as re

def get_ElementOri_from_list_by_name_s(ElementOri_list:list[ElementOri], name:str)->ElementOri:
    for elementOri in ElementOri_list:
        if elementOri.name() == name:
            return elementOri
    return None

def get_ElementOri_from_list_by_name_ex_s(ElementOri_list:list[ElementOri], name:str)->ElementOri:
    ele_list = []
    for elementOri in ElementOri_list:
        if elementOri.name() == name:
            ele_list.append(elementOri)
    if len(ele_list) == 0:
        raise ElementOriNotFoundError(f"Element \"{name}\" does not exist.")
    elif len(ele_list) >= 2:
        raise ElementOriFoundMultiError(f"More than one element match \"{name}\".")
    return ele_list[0]

def get_ElementOri_from_list_by_restr_ex_s(ElementOri_list:list[ElementOri], restr:str)->list[ElementOri]:
    ele_list = []
    for elementOri in ElementOri_list:
        if re.match(restr, elementOri.name()):
            ele_list.append(elementOri)
    if len(ele_list) == 0:
        raise ElementOriNotFoundError(f"Element \"{restr}\" does not exist.")
    elif len(ele_list) >= 2:
        raise ElementOriFoundMultiError(f"More than one element match \"{restr}\".")
    return ele_list[0]