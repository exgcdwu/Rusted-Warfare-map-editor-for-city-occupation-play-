from typing import Union
from copy import deepcopy

import rwmap._object as object
import rwmap._frame as frame
import rwmap._data.tobject as tobject
import rwmap._data.const as const
import rwmap._util as utility

import rwmap._data.tobject_group as tobject_group_useful

class unitRemoveAllTeam(object.TObject_Group):
    def __init__(self, pos:frame.Coordinate, size:frame.Coordinate, team_list:list[int], name_list:list[str] = [], 
               warmup:int = -1, reset:int = -1, 
               isdelay:bool = False, isrepeat:bool = False, actiBy_s:list[object.TObject_One] = [], 
               deactiBy_s:list[object.TObject_One] = [], isalltoacti:bool = False):
        udetect_s = [tobject.UnitRemove(pos, size, 
                                        name = utility.list_get_s(name_list, team), 
                                        team = team, warmup = warmup, 
                                        reset = reset, isdelay = isdelay, 
                                        isrepeat = isrepeat, actiBy_s = actiBy_s, 
                                        deactiBy_s = deactiBy_s, 
                                        isalltoacti = isalltoacti) for team in team_list]
        return object.TObject_Group.__init__(self, udetect_s)
    
    def unitRemove_s(self)->list[object.TObject_One]:
        return self._TObject_One_list
    
    def unitRemove_s_team(self, team:int)->object.TObject_One:
        for tobject in self._TObject_One_list:
            if int(tobject._otype.output_optional_properties("team")) == team:
                return tobject

    def add_actiBy_s(self, team:int, actiBy_s:Union[list[object.TObject_One], object.TObject_One]):
        actiBy_s_list = deepcopy(utility.list_variable_s(actiBy_s))
        self.unitRemove_s_team(team).add_actiBy_s(actiBy_s_list)

    def add_deactiBy_s(self, team:int, deactiBy_s:list[object.TObject_One]):
        deactiBy_s_list = deepcopy(utility.list_variable_s(deactiBy_s))
        self.unitRemove_s_team(team).add_deactiBy_s(deactiBy_s_list)

    def add_twoactiBy_s(self, team:int, add_TObject_One_two_s:tuple[list[object.TObject_One], 
                                                          list[object.TObject_One]] = ([], [])):
        self.unitRemove_s_team(team).add_actiBy_s(add_TObject_One_two_s[0])
        self.unitRemove_s_team(team).add_deactiBy_s(add_TObject_One_two_s[1])

    def add_actiBy_buildingDetect_s(self, team:int, team_list:list[int], 
                                           building_s:tobject_group_useful.BuildingDetect):
        self.unitRemove_s_team(team).add_actiBy_s(building_s.idTObject_s_team_list(team_list))

    def add_deactiBy_buildingDetect_s(self, team:int, team_list:list[int], 
                                           building_s:tobject_group_useful.BuildingDetect):
        self.unitRemove_s_team(team).add_deactiBy_s(building_s.idTObject_s_team_list(team_list))

    def add_actiBy_list_buildingDetect_s(self, team_remove_list:list[int], team_building_list:list[int], 
                                           building_s:tobject_group_useful.BuildingDetect):
        for team in team_remove_list:
            self.unitRemove_s_team(team).add_actiBy_s(building_s.idTObject_s_team_list(team_building_list))

    def add_deactiBy_list_buildingDetect_s(self, team_remove_list:list[int], team_building_list:list[int], 
                                           building_s:tobject_group_useful.BuildingDetect):
        for team in team_remove_list:
            self.unitRemove_s_team(team).add_deactiBy_s(building_s.idTObject_s_team_list(team_building_list))


        



    