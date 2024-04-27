from typing import Union
from copy import deepcopy

import rwmap._object as object
import rwmap._frame as frame
import rwmap._data.tobject as tobject
import rwmap._data.const as const

import rwmap._util as utility

class RefreshBuilding(object.TObject_Group):
    pass

class RefreshBuildingAllTeam(RefreshBuilding):
    pass

class RefreshBuildingAllTeamGroup(RefreshBuildingAllTeam):
    pass

class NormalUnitAdd(object.TObject_Group):
    def __init__(self, pos:frame.Coordinate, team:int, spawnUnits:str, 
                 size:frame.Coordinate = const.COO.SIZE_STANDARD, 
                 name:str = None, warmup:int = -1, reset:int = -1, 
                 actiBy_s:Union[list[object.TObject_One], object.TObject_One] = [], 
                 deactiBy_s:Union[list[object.TObject_One], object.TObject_One] = []):
        actiBy_s_list = deepcopy(utility.list_variable_s(actiBy_s))
        deactiBy_s_list = deepcopy(utility.list_variable_s(deactiBy_s))
        uadd = tobject.UnitAdd(pos, team, spawnUnits, size = size, name = name, 
                               warmup = warmup, reset = reset, actiBy_s = actiBy_s_list, 
                               deactiBy_s = deactiBy_s_list)
        return object.TObject_Group.__init__(self, [uadd])
    
    def unitAdd_s(self)->tobject.UnitAdd:
        return self._TObject_One_list[0]
    
    def pos(self)->frame.Coordinate:
        return self.unitAdd_s()._pos.pos()
    
    def size(self)->frame.Coordinate:
        return self.unitAdd_s()._pos.size()

    def add_actiBy_s(self, actiBy_s:Union[list[object.TObject_One], object.TObject_One]):
        actiBy_s_list = deepcopy(utility.list_variable_s(actiBy_s))
        self.unitAdd_s().add_actiBy_s(actiBy_s_list)

    def add_deactiBy_s(self, deactiBy_s:list[object.TObject_One]):
        deactiBy_s_list = deepcopy(utility.list_variable_s(deactiBy_s))
        self.unitAdd_s().add_deactiBy_s(deactiBy_s_list)

    def add_twoactiBy_s(self, add_TObject_One_two_s:tuple[list[object.TObject_One], 
                                                          list[object.TObject_One]] = ([], [])):
        self.unitAdd_s().add_twoactiBy_s(add_TObject_One_two_s)

    def add_building_control(self, building:RefreshBuilding, team_num:int, team_list:list[int], isacti:bool = True, 
                         isrelationand:bool = True)->None:
        self.add_twoactiBy_s(building.building_control(team_num, team_list, 
                                            isacti = isacti, isrelationand = isrelationand))
        
    def add_buildingallteam_control(self, building:RefreshBuildingAllTeam, teamgroup:int, teamgroup_num:int = 2, 
                             isacti:bool = True, isrelationand:bool = True)->None:
        self.add_twoactiBy_s(building.buildingallteam_control(teamgroup, teamgroup_num = teamgroup_num, 
                                                       isacti = isacti, 
                                                       isrelationand = isrelationand))

    def add_buildingallteamgroup_control(self, building:RefreshBuildingAllTeamGroup, teamgroup:int, isacti:bool = True, 
                         isrelationand:bool = True)->None:
        self.add_twoactiBy_s(building.buildingallteamgroup_control(teamgroup, 
                                            isacti = isacti, isrelationand = isrelationand))

class NormalUnitAddInstant(NormalUnitAdd):
    def __init__(self, pos:frame.Coordinate, team:int, spawnUnits:str, 
                 size:frame.Coordinate = const.COO.SIZE_STANDARD, 
                 name:str = None, warmup:int = -1):
        NormalUnitAdd.__init__(self, pos, team, spawnUnits, size = size, 
                             name = name, warmup = warmup)





