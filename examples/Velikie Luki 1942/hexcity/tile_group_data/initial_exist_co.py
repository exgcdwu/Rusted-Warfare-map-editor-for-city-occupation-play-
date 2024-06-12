from copy import deepcopy

import rwmap._frame as frame
import rwmap._tile as tile
import rwmap as rw

EXPORT_UNITS_TEAM_SIZE = frame.Coordinate(12, 11)

UNITCOO = {
    rw.const.UNIT.turret_flamethrower: frame.Coordinate(3, 3), 
    rw.const.UNIT.turret_artillery: frame.Coordinate(3, 4), 
    rw.const.UNIT.turretT2: frame.Coordinate(3, 1), 
    rw.const.UNIT.turret: frame.Coordinate(3, 0), 
    rw.const.UNIT.builder: frame.Coordinate(4, 0), 
    rw.const.UNIT.landFactory: frame.Coordinate(1, 0)
}

def export_units(team:int, unit:str):
    if team == -2:
        team = 10
    team = team + 1
    team_n = frame.Coordinate(int(team / 3), team % 3)
    return frame.TagCoordinate("export_units", team_n * EXPORT_UNITS_TEAM_SIZE + UNITCOO[unit])

export_units_team_to_land = {str(team):export_units(team, rw.const.UNIT.landFactory) for team in range(10)}

def initial_exist_tile(team_list:list[int])->list[tile.TileGroup_One, rw.frame.Coordinate]:
    til_m = tile.TileGroup_Matrix([str(team) for team in team_list])
    return [tile.TileGroup_One.init_tilegroup_matrix(rw.const.NAME.Units, deepcopy(export_units_team_to_land), 
                                             til_m), rw.frame.Coordinate(len(team_list) * rw.const.COO.SIZE_STANDARD.x(), rw.const.COO.SIZE_STANDARD.y())]