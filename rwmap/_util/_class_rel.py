import rwmap._frame as frame
from rwmap._frame._element_ori import ElementOri

def get_ElementOri_from_list_by_name_s(ElementOri_list:list[ElementOri], name:str)->ElementOri:
    for elementOri in ElementOri_list:
        if elementOri.name() == name:
            return elementOri
    return None