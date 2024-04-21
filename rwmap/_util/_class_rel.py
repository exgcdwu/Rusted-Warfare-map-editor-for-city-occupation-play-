import rwmap._frame as frame

def get_ElementOri_from_list_by_name(ElementOri_list:list[ElementOri], name:str)->ElementOri:
    for elementOri in ElementOri_list:
        if elementOri._properties.returnDefaultProperty("name") == name:
            return elementOri