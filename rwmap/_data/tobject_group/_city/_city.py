from typing import Union
from copy import deepcopy

import rwmap._object as object
import rwmap._frame as frame
import rwmap._data.tobject as tobject
import rwmap._data.const as const

import rwmap._util as utility

import rwmap._data.tobject_group._city._normal_unit_add as city_add
import rwmap._data.tobject_group._city._city_detect as city_detect
import rwmap._data.tobject_group._city._city_text as city_text
import rwmap._data.tobject_group._city._refresh_building as refresh_building

def _make_citytext_s(pos:frame.Coordinate, text:Union[list[str], str], 
                     size:frame.Coordinate = const.COO.SIZE_STANDARD, 
                     textColor:Union[list[str], str] = [], textSize:int = -1, 
                     name:Union[list[str], str] = [])->city_text.CityText:
        maptext = city_text.CityText(pos, text, size = size, textColor = textColor, 
                                     textSize = textSize, name = name)
        return maptext

def _make_citytextnoteam_s(pos:frame.Coordinate, text:str, 
                     size:frame.Coordinate = const.COO.SIZE_STANDARD, 
                     textColor:str = None, textSize:int = -1, 
                     name:str = None)->city_text.CityText:
        maptext = city_text.CityTextNoTeam(pos, text, size = size, textColor = textColor, 
                                           textSize = textSize, name = name)
        return maptext

def _make_citytextallteam_s(pos:frame.Coordinate, text:list[str], 
                     size:frame.Coordinate = const.COO.SIZE_STANDARD, 
                     textColor:list[str] = [], textSize:int = -1, 
                     name:list[str] = [])->city_text.CityText:
        maptext = city_text.CityTextAllTeam(pos, text, size = size, textColor = textColor, 
                                     textSize = textSize, name = name)
        return maptext

class City(refresh_building.RefreshBuilding):
    def __init__(self, building_s:refresh_building.RefreshBuilding, citytext:city_text.CityText, 
                 detect_to_text:list[int] = None):
        self.__dict__ = building_s.__dict__
        self._detect_to_text = deepcopy(detect_to_text)
        if detect_to_text == None:
            minsize = min(building_s.length(), citytext.length())
            detect_to_text = list(range(minsize))
        if citytext.length() == 1:
            pass
        else:
            for index, textindex in enumerate(detect_to_text):
                if textindex >= citytext.length():
                    raise IndexError("The number of city text is less.")
                if building_s._is_detect_acti_add:
                    citytext.maptext(textindex).add_deactiBy_s(building_s.idTObject_s_index(index))
                else:
                    citytext.maptext(textindex).add_actiBy_s(building_s.idTObject_s_index(index))
        self._TObject_Group_list.append(citytext)
    
    def cityText_s(self)->city_text.CityText:
        return self._TObject_Group_list[2]

    @classmethod
    def init_adt(cls, uadd_s:city_add.NormalUnitAdd, udetect_s:city_detect.BuildingDetect, 
                 citytext:city_text.CityText, is_detect_acti_add:bool = True, 
                 detect_to_text:list[int] = None):
        building_s = refresh_building.RefreshBuilding(uadd_s, udetect_s, 
                                                      is_detect_acti_add = is_detect_acti_add)
        return cls(building_s, citytext, detect_to_text)

    @classmethod
    def init_base(cls, pos:frame.Coordinate, id:Union[str, list[str]], 
                  text:Union[list[str], str], warmup_detect:int, warmup_add:int, 
                  reset_detect:int, reset_add:int, units:str = "supplyDepot", 
                  team_add:int = -1, team_detect:list[Union[int, None]] = [], 
                  size:frame.Coordinate = const.COO.SIZE_STANDARD, 
                  isonlybuilding:bool = True, name_detect:Union[str, list[str]] = [], 
                  name_add:str = None, name_text:Union[list[str], str] = [], unitsnum:int = 1, 
                  textColor:Union[list[str], str] = [], textSize:int = -1, 
                  is_detect_acti_add:bool = False, detect_to_text:list[int] = None):
        building_s = refresh_building.RefreshBuilding.init_base\
        (pos, id, units, warmup_detect, warmup_add, reset_detect, reset_add, team_add = team_add, 
         team_detect = team_detect, size = size, isonlybuilding = isonlybuilding, 
         name_detect = name_detect, name_add = name_add, unitsnum = unitsnum, 
         is_detect_acti_add = is_detect_acti_add)
        citytext = _make_citytext_s(pos, text, size = size, textColor = textColor, 
                                    textSize = textSize, name = name_text)
        return cls(building_s, citytext, detect_to_text)
    
    @classmethod
    def init_bb(cls, building_s:refresh_building.RefreshBuilding, 
                text:Union[list[str], str], name_text:Union[list[str], str] = [], 
                textColor:Union[list[str], str] = [], textSize:int = -1, 
                detect_to_text:list[int] = None):
        citytext = city_text.CityText(building_s.pos(), text, building_s.size(), textColor = textColor, 
                                      textSize = textSize, name = name_text)
        return cls(building_s, citytext, detect_to_text = detect_to_text)
    
class CityNoTeam(refresh_building.RefreshBuildingNoTeam, City):
    def __init__(self, building_s:refresh_building.RefreshBuildingNoTeam, 
                 citytext:city_text.CityTextNoTeam):
        if ((not isinstance(building_s, refresh_building.RefreshBuildingNoTeam)) or \
           (not isinstance(citytext, city_text.CityTextNoTeam))):
            raise TypeError("CityNoTeam.__init__:must be noteam")
        City.__init__(self, building_s, citytext)

    @classmethod
    def init_adt(cls, uadd_s:city_add.NormalUnitAdd, udetect_s:city_detect.BuildingDetectNoTeam, 
                 citytext:city_text.CityTextNoTeam, is_detect_acti_add:bool = True):
        building_s = refresh_building.RefreshBuildingNoTeam(uadd_s, udetect_s, 
                                                      is_detect_acti_add = is_detect_acti_add)
        return cls(building_s, citytext)
    
    @classmethod
    def init_base(cls, pos:frame.Coordinate, id:str, 
                  text:str, warmup_detect:int, warmup_add:int, 
                  reset_detect:int, reset_add:int, units:str = "supplyDepot", 
                  team_add:int = -1, size:frame.Coordinate = const.COO.SIZE_STANDARD, 
                  isonlybuilding:bool = True, name_detect:str = None, 
                  name_add:str = None, name_text:str = None, unitsnum:int = 1, 
                  textColor:str = None, textSize:int = -1, 
                  is_detect_acti_add:bool = False):
        building_s = refresh_building.RefreshBuildingNoTeam.init_base\
        (pos, id, units, warmup_detect, warmup_add, reset_detect, reset_add, team_add = team_add, 
         size = size, isonlybuilding = isonlybuilding, 
         name_detect = name_detect, name_add = name_add, unitsnum = unitsnum, 
         is_detect_acti_add = is_detect_acti_add)
        citytext = _make_citytextnoteam_s(pos, text, size = size, textColor = textColor, 
                                  textSize = textSize, name = name_text)
        return cls(building_s, citytext)
    
    @classmethod
    def init_bb(cls, building_s:refresh_building.RefreshBuildingNoTeam, 
                text:Union[list[str], str], name_text:Union[list[str], str] = [], 
                textColor:Union[list[str], str] = [], textSize:int = -1):
        citytext = city_text.CityTextNoTeam(building_s.pos(), text, building_s.size(), textColor = textColor, 
                                      textSize = textSize, name = name_text)
        return cls(building_s, citytext)
    
class CityAllTeam(refresh_building.RefreshBuildingAllTeam, City):
    def __init__(self, building_s:refresh_building.RefreshBuildingAllTeam, 
                 citytext:city_text.CityTextAllTeam, detect_to_text:list[int] = None):
        if ((not isinstance(building_s, refresh_building.RefreshBuildingAllTeam)) or \
           (not isinstance(citytext, city_text.CityTextAllTeam))):
            raise TypeError("CityAllTeam.__init__:must be allteam")
        
        City.__init__(self, building_s, citytext, detect_to_text = detect_to_text)

    @classmethod
    def init_adt(cls, uadd_s:city_add.NormalUnitAdd, udetect_s:city_detect.BuildingDetectAllTeam, 
                 citytext:city_text.CityTextAllTeam, is_detect_acti_add:bool = True, 
                 detect_to_text:list[int] = None):
        building_s = refresh_building.RefreshBuildingAllTeam(uadd_s, udetect_s, 
                                                      is_detect_acti_add = is_detect_acti_add, 
                                                      detect_to_text = detect_to_text)
        return cls(building_s, citytext, detect_to_text = detect_to_text)
    
    @classmethod
    def init_base(cls, pos:frame.Coordinate, id:str, teamnum:int, 
                  text:Union[str, list[str]], warmup_detect:int, warmup_add:int, 
                  reset_detect:int, reset_add:int, units:str = "supplyDepot", 
                  team_add:int = -1, size:frame.Coordinate = const.COO.SIZE_STANDARD, 
                  isonlybuilding:bool = True, name_detect:str = None, 
                  name_add:str = None, name_text:Union[str, list[str]] = [], unitsnum:int = 1, 
                  id_group:list[int] = [], textColor:Union[str, list[str]] = [], textSize:int = -1, 
                  is_detect_acti_add:bool = False, detect_to_text:list[int] = None):
        building_s = refresh_building.RefreshBuildingAllTeam.init_base\
        (pos, id, teamnum, units, warmup_detect = warmup_detect, warmup_add = warmup_add, 
         reset_detect = reset_detect, reset_add = reset_add, team_add = team_add, size = size, 
         isonlybuilding = isonlybuilding, name_detect = name_detect, name_add = name_add, 
         unitsnum = unitsnum, id_group = id_group, is_detect_acti_add = is_detect_acti_add)
        citytext = _make_citytextallteam_s(pos, text, size = size, textColor = textColor, 
                                  textSize = textSize, name = name_text)
        return cls(building_s, citytext, detect_to_text = detect_to_text)
    
    @classmethod
    def init_bb(cls, building_s:refresh_building.RefreshBuildingAllTeam, 
                text:Union[str, list[str]], name_text:list[str] = [], 
                textColor:Union[str, list[str]] = [], textSize:int = -1, 
                detect_to_text:Union[str, list[str]] = None):
        citytext = city_text.CityTextAllTeam(building_s.pos(), text, building_s.size(), textColor = textColor, 
                                      textSize = textSize, name = name_text)
        return cls(building_s, citytext, detect_to_text = detect_to_text)
    
class CityAllTeamGroup(refresh_building.RefreshBuildingAllTeamGroup, CityAllTeam):
    def __init__(self, building_s:refresh_building.RefreshBuildingAllTeamGroup, 
                 citytext:city_text.CityTextAllTeam):
        if ((not isinstance(building_s, refresh_building.RefreshBuildingAllTeamGroup)) or \
           (not isinstance(citytext, city_text.CityTextAllTeam))):
            raise TypeError("CityAllTeamGroup.__init__:must be allteamgroup/allteam")
        teamgroupnum = building_s.group()
        detect_to_text = [textn % teamgroupnum for textn in range(building_s.length() - 1)]
        if citytext.length() != teamgroupnum:
            raise ValueError("Length of citytext is not equal to building.")
        City.__init__(self, building_s, citytext, detect_to_text = detect_to_text)

    @classmethod
    def init_adt(cls, uadd_s:city_add.NormalUnitAdd, udetect_s:city_detect.BuildingDetectAllTeamGroup, 
                 citytext:city_text.CityTextAllTeam, is_detect_acti_add:bool = True):
        detect_to_text = list[range(udetect_s.group())]
        building_s = refresh_building.RefreshBuildingAllTeam(uadd_s, udetect_s, 
                                                      is_detect_acti_add = is_detect_acti_add, 
                                                      detect_to_text = detect_to_text)
        return cls(building_s, citytext, detect_to_text = detect_to_text)
    
    @classmethod
    def init_base(cls, pos:frame.Coordinate, id:str, teamnum:int, 
                  text:Union[list[str], str], warmup_detect:int, warmup_add:int, 
                  reset_detect:int, reset_add:int, units:str = "supplyDepot", 
                  team_add:int = -1, size:frame.Coordinate = const.COO.SIZE_STANDARD, 
                  isonlybuilding:bool = True, name_detect:str = None, 
                  name_add:str = None, name_text:Union[list[str], str] = [], unitsnum:int = 1, 
                  teamgroup:int = 2, textColor:Union[list[str], str] = [], textSize:int = -1, 
                  is_detect_acti_add:bool = False, isacti_accu:bool = False):
        
        building_s = refresh_building.RefreshBuildingAllTeamGroup.init_base\
        (pos, id, teamnum, units, warmup_detect = warmup_detect, warmup_add = warmup_add, 
         reset_detect = reset_detect, reset_add = reset_add, team_add = team_add, size = size, 
         isonlybuilding = isonlybuilding, name_detect = name_detect, name_add = name_add, 
         unitsnum = unitsnum,teamgroup = teamgroup, is_detect_acti_add = is_detect_acti_add, 
         isacti_accu = isacti_accu)
        citytext = _make_citytextallteam_s(pos, text, size = size, textColor = textColor, 
                                  textSize = textSize, name = name_text)
        return cls(building_s, citytext, teamgroup = teamgroup)
    
    @classmethod
    def init_bb(cls, building_s:refresh_building.RefreshBuildingAllTeamGroup, 
                text:Union[list[str], str], name_text:Union[list[str], str] = [], 
                textColor:Union[list[str], str] = [], textSize:int = -1):
        citytext = city_text.CityTextAllTeam(building_s.pos(), text, building_s.size(), textColor = textColor, 
                                      textSize = textSize, name = name_text)
        return cls(building_s, citytext)