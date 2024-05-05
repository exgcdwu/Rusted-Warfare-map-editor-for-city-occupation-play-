from typing import Union
from copy import deepcopy

import rwmap._object as object
import rwmap._frame as frame
import rwmap._data.tobject as tobject
import rwmap._data.const as const

import rwmap._util as utility

class BuildingDetect(object.TObject_Group):
    def __init__(self, pos:frame.Coordinate, id:Union[str, list[str]], 
                  warmup:int, reset:int, size:frame.Coordinate = const.COO.SIZE_STANDARD, 
                  unitType_andob:Union[str, bool] = True, name:Union[str, list[str]] = [],
                  team:list[Union[int, None]] = [], minUnits:int = None, maxUnits:int = None):
        id_list = deepcopy(utility.list_variable_s(id))
        name_list = deepcopy(utility.list_variable_s(name))
        udetect = []
        for index in range(len(id_list)):
            name = utility.list_get_s(name_list, index)
            teamn = utility.list_get_s(team, index)
            id = id_list[index]
            unitType = unitType_andob if unitType_andob != True else None
            onlyList = ["onlyBuildings"] if unitType_andob == True else []
            udetect.append(tobject.UnitDetect(pos, size, name = name, team = teamn, minUnits = minUnits, 
                                         maxUnits = maxUnits, unitType = unitType, onlyList = onlyList, 
                                         warmup = warmup, reset = reset, id = id))
        return object.TObject_Group.__init__(self, udetect)
    
    def idTObject_s(self)->list[object.TObject_One]:
        return [TObject.idTObject_s() for TObject in self._TObject_One_list]

    def idTObject_s_index(self, index:int)->object.TObject_One:
        return self._TObject_One_list[index].idTObject_s()
    
    def idTObject_s_team(self, team:Union[int, None])->Union[object.TObject_One, None]:
        team = str(team) if isinstance(team, int) else team
        for tobject in self._TObject_One_list:
            if tobject._otype.output_optional_properties().get("team") == team:
                return tobject.idTObject_s()
        return None
    
    def idTObject_s_team_list(self, team_list:list[Union[int, None]])->list[Union[object.TObject_One, None]]:
        return [self.idTObject_s_team(team) for team in team_list]

    def pos(self)->frame.Coordinate:
        return self.idTObject_s_index(0)._pos.pos()

    def size(self)->frame.Coordinate:
        return self.idTObject_s_index(0)._pos.size()
    
    def length(self)->int:
        return len(self._TObject_One_list)

class BuildingDetectNoTeam(BuildingDetect):
    def __init__(self, pos:frame.Coordinate, id:str, 
                  warmup:int, reset:int, size:frame.Coordinate = const.COO.SIZE_STANDARD, 
                  unitType_andob:Union[str, bool] = True, name:str = None, 
                  minUnits:int = None, maxUnits:int = None):
        name = [] if name == None else name
        BuildingDetect.__init__(self, pos, id, warmup, reset, size = size, 
                              unitType_andob = unitType_andob, name = name, 
                              minUnits = minUnits, maxUnits = maxUnits)
    
class BuildingDetectAllTeam(BuildingDetect):
    def __init__(self, pos:frame.Coordinate, id:str, teamnum:int, 
                 warmup:int, reset:int, size:frame.Coordinate = const.COO.SIZE_STANDARD, 
                 unitType_andob:Union[str, bool] = True, 
                 name:str = None, id_group:list[int] = [], minUnits:int = None, 
                 maxUnits:int = None):
        if id_group != []:
            id_list = [f'{id}' + f'{id_group[team]:0>2}' if team < len(id_group) else "" for team in range(teamnum)]
        else:
            id_list = [f'{id}' + f'{team:0>2}' for team in range(teamnum)]
        if name == None:
            name_list = [f'{team:0>2}' for team in range(teamnum)]
        else:
            name_list = [f'{name}{team:0>2}' for team in range(teamnum)]

        id_list = id_list + [f'{id}']
        teamlist = list(range(teamnum)) + [None]
        name_list = name_list + [f'{name}'] if name != None else []
        
        BuildingDetect.__init__(self, pos, id_list, warmup, reset, size = size, 
                              unitType_andob = unitType_andob, name = name_list, 
                              team = teamlist, minUnits = minUnits, 
                              maxUnits = maxUnits)
    
    def idTObject_s_team_list(self, teamnow:int, teamgroupnum:int = 2)->list[object.TObject_One]:
        return self.idTObject_s_team_list([team for team in range(len(self._TObject_One_list))
                                             if team % teamgroupnum == teamnow])
    
    def idTObject_s_id(self, id:str)->list[object.TObject_One]:
        return [self.idTObject_s_index(index) for index in range(len(self._TObject_One_list))
                if self.idTObject_s_index(index)._name == id]

class BuildingDetectAllTeamGroup(BuildingDetectAllTeam):
    def __init__(self, pos:frame.Coordinate, id:str, teamnum:int, 
                 warmup:int, reset:int, unitType_andob:Union[str, bool] = True, 
                 size:frame.Coordinate = const.COO.SIZE_STANDARD, 
                 name:str = None, teamgroup:int = 2, minUnits:int = None, 
                 maxUnits:int = None, isacti_accu:bool = False):
        self._teamgroup = teamgroup
        id_group = [team % teamgroup for team in range(teamnum)]  if isacti_accu else []
        BuildingDetectAllTeam.__init__(self, pos, id, teamnum, warmup, reset, size = size, 
                                       unitType_andob = unitType_andob, name = name, 
                                       id_group = id_group, minUnits = minUnits, maxUnits = maxUnits)
        
    def group(self)->int:
        return self._teamgroup
    
    def team_list(self, teamgroupnow:int)->list[int]:
        return [team for team in range(self.length()) if team % self._teamgroup == teamgroupnow]