from typing import Union
from copy import deepcopy

import rwmap._object as object
import rwmap._frame as frame
import rwmap._data.tobject as tobject
import rwmap._data.const as const
import rwmap._exceptions as rwexceptions

import rwmap._util as utility

import rwmap._data.tobject_group._city._normal_unit_add as city_add
import rwmap._data.tobject_group._city._city_detect as city_detect
import rwmap._data.tobject_group._city._city_text as city_text

def _make_uadd_s(pos:frame.Coordinate, warmup:int, reset:int, units:str, 
                 team:int = -1, size:frame.Coordinate = const.COO.SIZE_STANDARD, 
                 name:str = None, unitsnum:int = 1)->city_add.NormalUnitAdd:
    return city_add.NormalUnitAdd(pos, team, f'{units}*{unitsnum}', 
                                size = size, name = name, warmup = warmup, 
                                reset = reset)

def _make_udetect_s(pos:frame.Coordinate, id:Union[str, list[str]], units:str, 
                    warmup:int, reset:int, team:list[Union[int, None]] = [], 
                    size:frame.Coordinate = const.COO.SIZE_STANDARD, 
                    isonlybuilding:bool = True, name:Union[str, list[str]] = [], 
                    unitsnum:int = 1, is_detect_acti_add:bool = False)->city_detect.BuildingDetect:
        
        minUnits = unitsnum if not is_detect_acti_add else None
        maxUnits = unitsnum - 1 if is_detect_acti_add else None
        unitType_andob = units if not isonlybuilding else True

        udetect_s = city_detect.BuildingDetect(pos, id, warmup, reset, size = size, 
                                             unitType_andob = unitType_andob, name = name, 
                                             team = team, minUnits = minUnits, 
                                             maxUnits = maxUnits)
        return udetect_s

def _make_udetectnoteam_s(pos:frame.Coordinate, id:str, units:str, 
                    warmup:int, reset:int, 
                    size:frame.Coordinate = const.COO.SIZE_STANDARD, 
                    isonlybuilding:bool = True, name:str = [], 
                    unitsnum:int = 1, is_detect_acti_add:bool = False)->city_detect.BuildingDetectNoTeam:
        
        minUnits = unitsnum if not is_detect_acti_add else None
        maxUnits = unitsnum - 1 if is_detect_acti_add else None
        unitType_andob = units if not isonlybuilding else True

        udetect_s = city_detect.BuildingDetectNoTeam(pos, id, warmup, reset, size = size, 
                                                     unitType_andob = unitType_andob, 
                                                     name = name, minUnits = minUnits, 
                                                     maxUnits = maxUnits)
        return udetect_s

def _make_udetectallteam_s(pos:frame.Coordinate, id:str, teamnum:int, units:str, 
                    warmup:int, reset:int, 
                    size:frame.Coordinate = const.COO.SIZE_STANDARD, 
                    isonlybuilding:bool = True, name:str = [], id_group:list[int] = [], 
                    unitsnum:int = 1, 
                    is_detect_acti_add:bool = False)->city_detect.BuildingDetectAllTeam:
        
        minUnits = unitsnum if not is_detect_acti_add else None
        maxUnits = unitsnum - 1 if is_detect_acti_add else None
        unitType_andob = units if not isonlybuilding else True

        udetect_s = city_detect.BuildingDetectAllTeam(pos, id, teamnum, warmup, reset, size = size, 
                                                      unitType_andob = unitType_andob, name = name, 
                                                      id_group = id_group, minUnits = minUnits, 
                                                      maxUnits = maxUnits)

        return udetect_s

def _make_udetectallteamgroup_s(pos:frame.Coordinate, id:str, teamnum:int, units:str, 
                    warmup:int, reset:int, 
                    size:frame.Coordinate = const.COO.SIZE_STANDARD, 
                    isonlybuilding:bool = True, name:str = [], teamgroup:int = 2, 
                    unitsnum:int = 1, 
                    is_detect_acti_add:bool = False, isacti_accu:bool = False)->city_detect.BuildingDetectAllTeam:
        
        minUnits = unitsnum if not is_detect_acti_add else None
        maxUnits = unitsnum - 1 if is_detect_acti_add else None
        unitType_andob = units if not isonlybuilding else True

        udetect_s = city_detect.BuildingDetectAllTeamGroup(pos, id, teamnum, warmup, reset, size = size, 
                                                      unitType_andob = unitType_andob, name = name, 
                                                      teamgroup = teamgroup, minUnits = minUnits, 
                                                      maxUnits = maxUnits, isacti_accu = isacti_accu)

        return udetect_s

class RefreshBuilding(object.TObject_Group):
    pass

class RefreshBuilding(object.TObject_Group):
    def __init__(self, uadd_s:city_add.NormalUnitAdd, udetect_s:city_detect.BuildingDetect, 
                 is_detect_acti_add:bool = True):
        self._is_detect_acti_add = is_detect_acti_add
        toba = udetect_s.idTObject_s_team(None)
        if is_detect_acti_add:
            uadd_s.add_actiBy_s(toba)
        else:
            uadd_s.add_deactiBy_s(toba)
        object.TObject_Group.__init__(self, [], [uadd_s, udetect_s])
    
    @classmethod
    def init_base(cls, pos:frame.Coordinate, id:Union[str, list[str]], units:str, 
                 warmup_detect:int, warmup_add:int, reset_detect:int, reset_add:int, 
                 team_add:int = -1, team_detect:list[Union[int, None]] = [], 
                 size:frame.Coordinate = const.COO.SIZE_STANDARD, 
                 isonlybuilding:bool = True, name_detect:Union[str, list[str]] = [], 
                 name_add:str = None, unitsnum:int = 1, is_detect_acti_add:bool = False):
        uadd_s = _make_uadd_s(pos, warmup_add, reset_add, units, team = team_add, 
                              size = size, name = name_add, unitsnum = unitsnum)
        
        udetect_s = _make_udetect_s(pos, id, units, warmup_detect, reset_detect, 
                                    team = team_detect, size = size, 
                                    isonlybuilding = isonlybuilding, name = name_detect, 
                                    unitsnum = unitsnum, is_detect_acti_add = is_detect_acti_add)
        return cls(uadd_s, udetect_s, is_detect_acti_add)
    
    def pos(self)->frame.Coordinate:
        return self.unitAdd_s().pos()
    
    def size(self)->frame.Coordinate:
        return self.unitAdd_s().size()
    
    def length(self)->int:
        return self.unitDetect_s().length()

    def unitDetect_s(self)->city_detect.BuildingDetect:
        return self._TObject_Group_list[1]
    
    def unitAdd_s(self)->city_add.NormalUnitAdd:
        return self._TObject_Group_list[0]

    def add_actiBy_s(self, actiBy_s:Union[list[object.TObject_One], object.TObject_One]):
        actiBy_s_list = deepcopy(utility.list_variable_s(actiBy_s))
        self.unitAdd_s().add_actiBy_s(actiBy_s_list)

    def add_deactiBy_s(self, deactiBy_s:list[object.TObject_One]):
        deactiBy_s_list = deepcopy(utility.list_variable_s(deactiBy_s))
        self.unitAdd_s().add_deactiBy_s(deactiBy_s_list)

    def add_twoactiBy_s(self, add_TObject_One_two_s:tuple[list[object.TObject_One], 
                                                          list[object.TObject_One]] = ([], [])):
        self.unitAdd_s().add_twoactiBy_s(add_TObject_One_two_s)

    def _building_control_filter(self):
        if self._is_detect_acti_add:
            raise rwexceptions.BuildingDetectError("is_detect_acti_add of the building is true, \
                                                   then can not support control.")

    def building_control(self, team_num:int, team_list:list[int], isacti:bool = True, 
                         isrelationand:bool = True)->tuple[list[object.TObject_One], list[object.TObject_One]]:
        '''
            [actiBy, deactiBy]
        '''
        self._building_control_filter()
        team_list = deepcopy(team_list)
        if not (isacti ^ isrelationand):
            team_list = utility.team_list_inv(team_num, team_list)
        actiBy = [self.idTObject_s_team(team) for team in team_list]
        if isrelationand:
            return ([], actiBy)
        else:
            return (actiBy, [])
        
    def idTObject_s(self)->list[object.TObject_One]:
        return self.unitDetect_s().idTObject_s()

    def idTObject_s_index(self, index:int)->object.TObject_One:
        return self.unitDetect_s().idTObject_s_index(index)
    
    def idTObject_s_team(self, team:Union[int, None])->Union[object.TObject_One, None]:
        return self.unitDetect_s().idTObject_s_team(team)
    
    def idTObject_s_team_list(self, team_list:list[Union[int, None]])->list[Union[object.TObject_One, None]]:
        return [self.unitDetect_s().idTObject_s_team(team) for team in team_list]
    
class RefreshBuildingNoTeam(RefreshBuilding):
    def __init__(self, uadd_s:city_add.NormalUnitAdd, udetect_s:city_detect.BuildingDetectNoTeam, 
                 is_detect_acti_add:bool = True):
        RefreshBuilding.__init__(self, uadd_s, udetect_s, is_detect_acti_add)
    
    @classmethod
    def init_base(cls, pos:frame.Coordinate, id:str, units:str, 
                 warmup_detect:int, warmup_add:int, reset_detect:int, reset_add:int, 
                 team_add:int = -1, size:frame.Coordinate = const.COO.SIZE_STANDARD, 
                 isonlybuilding:bool = True, name_detect:str = None, 
                 name_add:str = None, unitsnum:int = 1, is_detect_acti_add:bool = False):
        uadd_s = _make_uadd_s(pos, warmup_add, reset_add, units, team = team_add, 
                              size = size, name = name_add, unitsnum = unitsnum)
        
        udetect_s = _make_udetectnoteam_s(pos, id, units, warmup_detect, reset_detect, 
                                          size = size, isonlybuilding = isonlybuilding, 
                                          name = name_detect, unitsnum = unitsnum, 
                                          is_detect_acti_add = is_detect_acti_add)
        return cls(uadd_s, udetect_s, is_detect_acti_add)
    
    def unitDetect_s(self)->city_detect.BuildingDetectNoTeam:
        return self._TObject_Group_list[1]

class RefreshBuildingAllTeam(RefreshBuilding):
    pass

class RefreshBuildingAllTeam(RefreshBuilding):
    def __init__(self, uadd_s:city_add.NormalUnitAdd, udetect_s:city_detect.BuildingDetectAllTeam, 
                 is_detect_acti_add:bool = True):
        RefreshBuilding.__init__(self, uadd_s, udetect_s, is_detect_acti_add)
    
    @classmethod
    def init_base(cls, pos:frame.Coordinate, id:str, teamnum:int, units:str, 
                 warmup_detect:int, warmup_add:int, reset_detect:int, reset_add:int, 
                 team_add:int = -1, size:frame.Coordinate = const.COO.SIZE_STANDARD, 
                 isonlybuilding:bool = True, name_detect:str = None, 
                 name_add:str = None, unitsnum:int = 1, id_group:list[int] = [], 
                 is_detect_acti_add:bool = False):

        uadd_s = _make_uadd_s(pos, warmup_add, reset_add, units, team = team_add, 
                              size = size, name = name_add, unitsnum = unitsnum)
        
        udetect_s = _make_udetectallteam_s(pos, id, teamnum, units, warmup_detect, reset_detect, 
                                           size = size, isonlybuilding = isonlybuilding, 
                                           name = name_detect, id_group = id_group, 
                                           unitsnum = unitsnum, is_detect_acti_add = is_detect_acti_add)
        return cls(uadd_s, udetect_s, is_detect_acti_add)
    
    def unitDetect_s(self)->city_detect.BuildingDetectAllTeam:
        return self._TObject_Group_list[1]
    
    def buildingallteam_control(self, teamgroup:int, teamgroup_num:int = 2, isacti:bool = True, 
                         isrelationand:bool = True)->tuple[list[object.TObject_One], 
                                                           list[object.TObject_One]]:
        team_num = self.length() - 1
        team_list = [team for team in range(team_num) if team % teamgroup_num == teamgroup]
        return RefreshBuilding.building_control(self, team_num, team_list, isacti = isacti, 
                                                isrelationand = isrelationand)


class RefreshBuildingAllTeamGroup(RefreshBuildingAllTeam):
    pass

class RefreshBuildingAllTeamGroup(RefreshBuildingAllTeam):
    def __init__(self, uadd_s:city_add.NormalUnitAdd, udetect_s:city_detect.BuildingDetectAllTeamGroup, 
                 is_detect_acti_add:bool = True):
        RefreshBuildingAllTeam.__init__(self, uadd_s, udetect_s, is_detect_acti_add)
    
    @classmethod
    def init_base(cls, pos:frame.Coordinate, id:str, teamnum:int, units:str, 
                 warmup_detect:int, warmup_add:int, reset_detect:int, reset_add:int, 
                 team_add:int = -1, size:frame.Coordinate = const.COO.SIZE_STANDARD, 
                 isonlybuilding:bool = True, name_detect:str = None, 
                 name_add:str = None, unitsnum:int = 1, teamgroup:int = 2, 
                 is_detect_acti_add:bool = False, isacti_accu:bool = False):

        uadd_s = _make_uadd_s(pos, warmup_add, reset_add, units, team = team_add, 
                              size = size, name = name_add, unitsnum = unitsnum)
        
        udetect_s = _make_udetectallteamgroup_s(pos, id, teamnum, units, warmup_detect, reset_detect, 
                                           size = size, isonlybuilding = isonlybuilding, 
                                           name = name_detect, teamgroup = teamgroup,
                                           unitsnum = unitsnum, is_detect_acti_add = is_detect_acti_add, 
                                           isacti_accu = isacti_accu)

        return cls(uadd_s, udetect_s, is_detect_acti_add)
    
    def unitDetect_s(self)->city_detect.BuildingDetectAllTeamGroup:
        return self._TObject_Group_list[1]
    
    def group(self)->int:
        return self.unitDetect_s().group()

    def idTObject_s_teamgroup(self, teamgroupnow:int)->list[object.TObject_One]:
        return [self.unitDetect_s().idTObject_s_team(team) 
                for team in range(self.unitDetect_s().size()) 
                if team % self.group() == teamgroupnow]
    
    def buildingallteamgroup_control(self, teamgroup:int, isacti:bool = True, 
                         isrelationand:bool = True)->tuple[list[object.TObject_One], 
                                                           list[object.TObject_One]]:
        teamgroup_num = self.group()
        return RefreshBuildingAllTeam.buildingallteam_control(self, teamgroup, 
                                                       teamgroup_num = teamgroup_num, 
                                                       isacti = isacti, 
                                                       isrelationand = isrelationand)

