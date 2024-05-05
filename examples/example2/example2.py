import os
import sys
current_dir_path = os.path.dirname(os.path.abspath(__file__))
example_dir_path = os.path.dirname(current_dir_path)

package_dir = os.path.dirname(example_dir_path)
sys.path.append(package_dir)
#这两项可以省略，如果pip安装（确定包的位置）

from copy import deepcopy
import numpy as np

import rwmap as rw

tileset_map = rw.RWmap.init_mapfile(f'{example_dir_path}\\template\\v3.tmx')
# V3模板
example2 = rw.RWmap.init_mapfile(f'{example_dir_path}\\example-empty\\example-empty.tmx')
# 一个200*200空地图 
example2.add_tileset(tileset_map.get_tileset_s("export_units"))
# V3模板地块集export_units 载入example2

grass = rw.frame.TagCoordinate("Short Grass", rw.frame.Coordinate(0, 0))
# 草地块

export_units_grid = rw.frame.Coordinate(12, 11)
turret = rw.frame.Coordinate(3, 0)
command = rw.frame.Coordinate(0, 0)
team0 = rw.frame.Coordinate(0, 1)
team1 = rw.frame.Coordinate(0, 2)
team2 = rw.frame.Coordinate(1, 0)
team3 = rw.frame.Coordinate(1, 1)
# export_units相对位置

turret0 = rw.frame.TagCoordinate("export_units", team0 * export_units_grid + turret)
turret1 = rw.frame.TagCoordinate("export_units", team1 * export_units_grid + turret)
turret2 = rw.frame.TagCoordinate("export_units", team2 * export_units_grid + turret)
turret3 = rw.frame.TagCoordinate("export_units", team3 * export_units_grid + turret)
# 炮塔地块

command0 = rw.frame.TagCoordinate("export_units", team0 * export_units_grid + command)
command1 = rw.frame.TagCoordinate("export_units", team1 * export_units_grid + command)
command2 = rw.frame.TagCoordinate("export_units", team2 * export_units_grid + command)
command3 = rw.frame.TagCoordinate("export_units", team3 * export_units_grid + command)
# 指挥中心地块

origin = rw.frame.Coordinate(0, 0)
# 原点位置

credit_pos = rw.frame.Coordinate(0, 0)
# 添加资金改动宾语的位置

ground_graph = rw.frame.TagRectangle("Ground", rw.frame.Rectangle(
    rw.frame.Coordinate(0, 0), 
    rw.frame.Coordinate(200, 200)
))
# 整张地图的ground

example2.addTile_square(ground_graph, grass)
# ground被grass覆盖

id_prefix = "acti_tu"
id_now = 1
# 为城市检测提供id

example2.addObject_one(rw.object_useful.Mapinfo(origin, rw.const.MAPTYPE.skirmish, 
                                                rw.const.FOG.los, rw.const.WIN.commandCenter, 
                                                text = 
                                                "本地图宾语完全由宾语自动化完成。此为城夺刷兵地图例子2。\n\
                                                城市名称会根据占领者改变颜色；存在兵力撤退和占领区机制"))
#添加map_info
example2.addObject_one(rw.object_useful.Credit(credit_pos, 0, setCredits = 0, reset = 1))
example2.addObject_one(rw.object_useful.Credit(credit_pos, 1, setCredits = 0, reset = 1))
example2.addObject_one(rw.object_useful.Credit(credit_pos, 2, setCredits = 0, reset = 1))
example2.addObject_one(rw.object_useful.Credit(credit_pos, 3, setCredits = 0, reset = 1))
#添加credit重置

def new_city(cityname:str, id_now:int)->rw.object_group_useful.CityNoTeam:
    building = rw.object_group_useful.RefreshBuildingAllTeamGroup.init_base(
        rw.frame.Coordinate(), id_prefix + str(id_now).zfill(3), 4, "turret", -1, 10, 10, 10)
    city = rw.object_group_useful.CityAllTeamGroup.init_bb(building, [cityname] * 2, 
                                                           textColor = ["green", "red"], 
                                                           textSize = 12)
    return city
#城市建立函数

def new_troopadd(spawnUnits:str, reset:int)->rw.object_group_useful.RefreshTroop:
    return rw.object_group_useful.RefreshTroop(rw.frame.Coordinate(0, 0), -1, spawnUnits, 
                                               5, reset)
#兵力生产函数
city_matrix = []
for x in range(10, 200, 20):
    city_matrix.append([])
    for y in range(10, 200, 20):
        # 循环建立城市
        pos_building = rw.frame.Coordinate(2 * x + 1, 2 * y + 1) * example2.tile_size() / 2
        # 建筑位置
        if x < 100:
            if y < 100:
                example2.addTile(rw.frame.TagCoordinate.init_xy("Units", x, y), turret0)
            else:
                example2.addTile(rw.frame.TagCoordinate.init_xy("Units", x, y), turret1)
        else:
            if y < 100:
                example2.addTile(rw.frame.TagCoordinate.init_xy("Units", x, y), turret3)
            else:
                example2.addTile(rw.frame.TagCoordinate.init_xy("Units", x, y), turret2)
        # 玩家初始炮塔
        city_now = new_city(f"城市({str(int((x - 10) / 20))},{str(int((y - 10) / 20))})", id_now)
        city_matrix[int((x - 10) / 20)].append(city_now)
        example2.addObject_group(city_now, pos_building)
        # 添加城市
        id_now = id_now + 1
        # id变化

troop_add = \
[
    {"spawnUnits":"mechGun", "acti": (0, 4), "reset": 100}, 
    {"spawnUnits":"mechGun", "acti": (0, 3), "deacti": (0, 4), "reset": 150},
    {"spawnUnits":"mechGun", "acti": (0, 2), "deacti": (0, 3), "reset": 200},

    {"spawnUnits":"mechGun", "acti": (1, 4), "reset": 100}, 
    {"spawnUnits":"mechGun", "acti": (1, 3), "deacti": (1, 4), "reset": 150},
    {"spawnUnits":"mechGun", "acti": (1, 2), "deacti": (1, 3), "reset": 200},

    {"spawnUnits":"mechGun", "acti": (2, 4), "reset": 100}, 
    {"spawnUnits":"mechGun", "acti": (2, 3), "deacti": (2, 4), "reset": 150},
    {"spawnUnits":"mechGun", "acti": (2, 2), "deacti": (2, 3), "reset": 200},

    {"spawnUnits":"mechGun", "acti": (3, 4), "reset": 100}, 
    {"spawnUnits":"mechGun", "acti": (1, 2), "deacti": (3, 4), "reset": 200}, 

    {"spawnUnits":"mechGun", "acti": (4, 4), "reset": 100}, 
    {"spawnUnits":"mechGun", "acti": (3, 3), "deacti": (4, 4), "reset": 150},
    {"spawnUnits":"mechGun", "acti": (2, 2), "deacti": (3, 3), "reset": 200},

    {"spawnUnits":"heavyTank", "acti": (0, 2), "reset": 100}, 
    {"spawnUnits":"heavyTank", "acti": (1, 1), "reset": 100}, 

    {"spawnUnits":"heavyArtillery", "acti": (0, 1), "reset": 100}, 

    {"spawnUnits":"bomber", "acti": (0, 0), "reset": 400}
]
# 兵力列表

mid_pos = rw.frame.Coordinate(9, 9)

def pos_list(pos_origin:rw.frame.Coordinate, mid_pos:rw.frame.Coordinate, is4:bool = -1)->list[rw.frame.Coordinate]:
    sub_pos = mid_pos - pos_origin 
    ver_pos = rw.frame.Coordinate(sub_pos.y(), -sub_pos.x())
    pos_list = [mid_pos - sub_pos, mid_pos + sub_pos, mid_pos + ver_pos, mid_pos - ver_pos]
    pos_list_n = []
    if is4 == -1:
        if abs(sub_pos.x()) != abs(sub_pos.y()):
            for pos_n in pos_list:
                pos_list_n.append(rw.frame.Coordinate(pos_n.y(), pos_n.x()))
                pos_list_n.append(pos_n)
        else:
            pos_list_n = pos_list
    elif is4 == 1:
        pos_list_n = pos_list
    else:
        for pos_n in pos_list:
            pos_list_n.append(rw.frame.Coordinate(pos_n.y(), pos_n.x()))
            pos_list_n.append(pos_n)
    return pos_list_n
# 兵力对称复制函数

for troop in troop_add:
    pos_origin = rw.frame.Coordinate(troop["acti"][0], troop["acti"][1]) * 2
    pos_acti_list = pos_list(pos_origin, mid_pos)
    if troop.get("deacti") != None:
        pos_deacti = rw.frame.Coordinate(troop["deacti"][0], troop["deacti"][1]) * 2
        pos_deacti_list = pos_list(pos_deacti, mid_pos, True if len(pos_acti_list) == 4 else False)
    for index, pos_acti in enumerate(pos_acti_list):
        pos_acti_grid = ((pos_acti * example2.tile_size()) + rw.frame.Coordinate(23, 23)) * rw.frame.Coordinate(20, 20) / 2
        new_troop:rw.object_group_useful.RefreshTroop = new_troopadd(troop["spawnUnits"], troop["reset"])
        sub_pos = pos_acti - mid_pos
        if (sub_pos.x() > 0) ^ (sub_pos.y() > 0):
            team = 1
        else:
            team = 0
        new_troop.add_buildingallteamgroup_control\
        (city_matrix[int(pos_acti.x() / 2)][int(pos_acti.y() / 2)], 
                                                   team)
        if troop.get("deacti") != None:
            pos_deacti = pos_deacti_list[index]
            new_troop.add_buildingallteamgroup_control\
            (city_matrix[int(pos_deacti.x() / 2)][int(pos_deacti.y() / 2)], 
                                                   team, isacti = False)
        example2.addObject_group(new_troop, pos_acti_grid)
# 添加兵力

example2.addTile(rw.frame.TagCoordinate("Units", rw.frame.Coordinate(10, 10)), command0)
example2.addTile(rw.frame.TagCoordinate("Units", rw.frame.Coordinate(10, 190)), command1)
example2.addTile(rw.frame.TagCoordinate("Units", rw.frame.Coordinate(190, 190)), command2)
example2.addTile(rw.frame.TagCoordinate("Units", rw.frame.Coordinate(190, 10)), command3)
# 玩家初始指挥中心

example2.write_file(f'{current_dir_path}\\example2.tmx')
# 输出地图到当前文件夹

maps_dir_path = "D:\\Game\\steam\\steamapps\\common\\Rusted Warfare\\mods\\maps"
example2.write_file(f'{maps_dir_path}\\example2.tmx')
# 输出地图到游戏地图文件夹

