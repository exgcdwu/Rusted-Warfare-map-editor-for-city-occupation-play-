from copy import deepcopy

import rwmap._frame as frame
import rwmap._tile as tile

EXPORT_UNITS_TEAM_SIZE = frame.Coordinate(12, 11)

def export_units(team:int, coo:frame.Coordinate):
    if team == -2:
        team = 10
    team = team + 1
    team_n = frame.Coordinate(int(team / 3), team % 3)
    return frame.TagCoordinate("export_units", team_n * EXPORT_UNITS_TEAM_SIZE + coo)

land = frame.Coordinate(1, 0)
export_units_team_to_land = {str(team):export_units(team, land) for team in range(10)}

def initial_exist_tile(team_list:list[int]):
    til_m = tile.TileGroup_Matrix([str(team) for team in team_list])
    tile.TileGroup_One.init_tilegroup_matrix("units", deepcopy(export_units_team_to_land), 
                                             til_m)