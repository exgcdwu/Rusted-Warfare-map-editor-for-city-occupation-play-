import os
import sys
current_dir_path = os.path.dirname(os.path.abspath(__file__))
great_war_dir_path = os.path.dirname(current_dir_path)
example_dir_path = os.path.dirname(great_war_dir_path)

package_dir = os.path.dirname(example_dir_path)
sys.path.append(package_dir)
#这两项可以省略，如果pip安装（确定包的位置）

sys.path.append(great_war_dir_path)
#hexcity 包位置

sys.path.append(current_dir_path)
# 地图数据文件

from copy import deepcopy
import numpy as np

import rwmap as rw
import hexcity

RWMAP_GROUND_VERSION = "1.0"
RWMAP_CITY_VERSION = "1.0"
RWMAP_VERSION = RWMAP_GROUND_VERSION + '.' + RWMAP_CITY_VERSION

project_hex_x_to_cart = np.array([[1, -0.5], [0, 1]], dtype = np.float32)
project_cart_to_tobject_coo = np.array([[1, 0], [0, -1]])
project_cart_to_layer_coo = np.array([[0, -1], [1, 0]])

origin_square = rw.frame.Coordinate(0.5, -0.5, dtype = np.float32)
tile_size = rw.const.COO.SIZE_STANDARD
square_size_tile = rw.frame.Coordinate(28, 24)
hex_size_tile = rw.frame.Coordinate(28, 32)
map_size_square = rw.frame.Coordinate(17, 5)

square_size_pixel = square_size_tile * tile_size
hex_size_pixel = hex_size_tile * tile_size

map_size_tile = map_size_square * square_size_tile

hex_x_shape = [
    rw.frame.Coordinate(0, -hex_size_pixel.y() / 2), 
    rw.frame.Coordinate(square_size_pixel.x() / 2, -(2 * square_size_pixel.y() - hex_size_pixel.y()) / 2), 
    rw.frame.Coordinate(square_size_pixel.x() / 2, (2 * square_size_pixel.y() - hex_size_pixel.y()) / 2), 
    rw.frame.Coordinate(0, hex_size_pixel.y() / 2), 
    rw.frame.Coordinate(-square_size_pixel.x() / 2, (2 * square_size_pixel.y() - hex_size_pixel.y()) / 2), 
    rw.frame.Coordinate(-square_size_pixel.x() / 2, -(2 * square_size_pixel.y() - hex_size_pixel.y()) / 2), 
]

hex_topleft_origin_layer_tile = rw.frame.Coordinate(-16, -14)

city_origin_layer_tile = rw.frame.Coordinate(-1, -1)
city_origin_object_pixel = rw.frame.Coordinate(-10, -10)

export_ground = "export_ground"

city_occu_tile_name_180b = "巴巴罗萨计划（1.80beta版）地块byXs"
city_occu_tile_name_160b = "巴巴罗萨计划（1.60beta版）地块byXs"
city_occu_tile_name_150 = "巴巴罗萨计划（1.50版）地块byXs"
city_occu_tile_name_B3 = "巴巴罗萨计划（B3版）地块byXs"
city_occu_sup_tile_name_12 = '辅助地块（1.2版）byXs'

terrain_b = {
    "w": rw.frame.TagCoordinate.init_xy(export_ground, 13, 7), 
    "s": rw.frame.TagCoordinate.init_xy(city_occu_tile_name_150, 5, 3), 
    "p": rw.frame.TagCoordinate.init_xy(city_occu_tile_name_180b, 5, 5), 
    "c": rw.frame.TagCoordinate.init_xy(city_occu_tile_name_B3, 6, 2)
}
terrain_p = {
    "w": rw.frame.TagCoordinate.init_xy(city_occu_tile_name_160b, 4, 1), 
    "s": rw.frame.TagCoordinate.init_xy(city_occu_tile_name_150, 4, 3), 
    "p": rw.frame.TagCoordinate.init_xy(city_occu_tile_name_180b, 4, 4), 
    "c": rw.frame.TagCoordinate.init_xy(city_occu_tile_name_B3, 4, 1)
}


tilegroup_wood = rw.tile.TileGroup_One.init_tilegroup_addlayer(
    {
        "b": terrain_b["w"], 
        "p": terrain_p["w"]
    }, 
    hexcity.tgroup.tile_group_addlayer_ground_hex28_32_fill_barrier_terrain
)
# 树林地块组

tilegroup_swamp = rw.tile.TileGroup_One.init_tilegroup_addlayer(
    {
        "b": terrain_b["s"], 
        "p": terrain_p["s"]
    }, 
    hexcity.tgroup.tile_group_addlayer_ground_hex28_32_fill_barrier_terrain
)
# 沼泽地块组

tilegroup_plane = rw.tile.TileGroup_One.init_tilegroup_addlayer(
    {
        "b": terrain_b["p"], 
        "p": terrain_p["p"]
    }, 
    hexcity.tgroup.tile_group_addlayer_ground_hex28_32_fill_light_barrier
)
# 平原地块组

tilegroup_cliff = rw.tile.TileGroup_One.init_tilegroup_addlayer(
    {
        "b": terrain_b["c"], 
        "p": terrain_p["c"]
    }, 
    hexcity.tgroup.tile_group_addlayer_ground_hex28_32_fill_barrier_terrain
)
# 山脉地块组

line_tile = rw.frame.TagCoordinate.init_xy(city_occu_tile_name_180b, 4, 1)

core_rect = rw.frame.Rectangle(rw.frame.Coordinate(0, 0), rw.frame.Coordinate(2, 2))
tilegroup_core_ground2 = rw.tile.TileGroup_One.init_tilegroup_matrix(
    rw.const.NAME.Ground, 
    {"ic": line_tile}, 
    hexcity.tgroup.tile_group_building_tile.part(core_rect).map({"r":"ic", "c":"ic"})
)
tilegroup_city_item2 = rw.tile.TileGroup_One.init_tilegroup_matrix(
    rw.const.NAME.Items, 
    {"ic": rw.frame.TagCoordinate.init_xy(city_occu_tile_name_180b, 3, 13)}, 
    hexcity.tgroup.tile_group_building_tile.part(core_rect).map({"r":"ic", "c":"ic"})
)
tilegroup_fort_item2 = rw.tile.TileGroup_One.init_tilegroup_matrix(
    rw.const.NAME.Items, 
    {"ic": rw.frame.TagCoordinate.init_xy(city_occu_tile_name_180b, 4, 13)}, 
    hexcity.tgroup.tile_group_building_tile.part(core_rect).map({"r":"ic", "c":"ic"})
)
tilegroup_fort_item3 = rw.tile.TileGroup_One.init_tilegroup_matrix(
    rw.const.NAME.Items, 
    {"ic": rw.frame.TagCoordinate.init_xy(city_occu_tile_name_180b, 4, 13)}, 
    hexcity.tgroup.tile_group_building_tile.map({"r":"ic", "c":"ic"})
)
tilegroup_city_PathingOverride = rw.tile.TileGroup_One.init_tilegroup_matrix(
    rw.const.NAME.PathingOverride, 
    {"iec": rw.frame.TagCoordinate.init_xy(city_occu_sup_tile_name_12, 9, 4)}, 
    hexcity.tgroup.tile_group_building_tile.map({"r":"iec"})
)
# 核心地块
def tilegroup_core_expand(ring:int):
    return [rw.tile.TileGroup_AddLayer.init_tilegroup_matrix(
        rw.const.NAME.Ground, 
        rw.tile.TileGroup_Matrix([["p"] * (2 * ring) for i in range(2 * ring)])
    ), -rw.frame.Coordinate(ring, ring)]
# 扩展外环

tilegroup_core_expand1 = tilegroup_core_expand(6)
tilegroup_core_expand0 = tilegroup_core_expand(3)


terrain = [
    ["s,N", "w"], 
    ["s", "w,N", "w", "p", "s,E"], 
    ["w", "w", "w,N", "p", "w,E", "s"], 
    ["p", "w", "p", "p", "p-N,NSE", "s-NE", "s"],  
    ["s,N", "w", "c", "w", "w,E", "p-ES", "p,S"], 
    ["w", "p,NES", "p", "p,E", "w,S", "c", "w-S"], 
    ["s", "p,N", "p,N", "p,E", "w", "w", "w"], 
    ["w-E", "s", "p,E", "p,E", "p-N,S", "p-S,SN", "p"], 
    ["w", "s-NES", "p-NE,N", "p-E,E", "p", "s-ES", "p"], 
    ["w", "p", "p", "p,E", "s-ES", "s", "w-ES"], 
    ["s", "w", "p,E", "p,ES", "p,", "s-NES", "w-E"], 
    ["w", "w,E", "p,S", "p,E", "w", "s", "s"], 
    ["w-ES", "w,E", "c,NS", "p,E", "p", "w", "w"], 
    ["s", "p-ES,E", "c", "w,E", "w", "w", "w"],
    ["w", "p,E", "w-ES", "w,E", "c", "w", "w"],
    ["w-NES", "p-E,E", "w", "w-ES,N", "w", "w", "w"],
    ["p", "p,S", "p-S", "p", "w-NES,N", "w-NE", "c"],
    ["e", "w", "w", "w", "w", "w,N", "w"],
    ["e", "e", "e", "w", "w", "w", "w"],
    ["e", "e", "e", "e", "e", "w", "w"],
]
# 地形-河流,铁路
'''
地形防御:
树林:喷火
山脉:机枪
沼泽:火炮
平原:炮塔
'''

for x, terrain_y_list in enumerate(terrain):
    for y, terrain_now in enumerate(terrain_y_list):
        
        terrain_now_templist = hexcity.sutility.get_str_end_split(terrain_now, ",")
        terrain_railway = terrain_now_templist[1]

        terrain_now_templist = hexcity.sutility.get_str_end_split(terrain_now_templist[0], "-")
        terrain_river = terrain_now_templist[1]

        terrain_tile = terrain_now_templist[0]

        terrain[x][y] = [terrain_tile, terrain_river, terrain_railway]

default_id_prefix = "acti_tu"
id_now = 1
team_num = 4
team_group = 2

team_list = [[team for team in range(team_num) if team % team_group == i] for i in range(team_group)]

explore_warmup_and_initial = 3
explore_delete = 5
building_add_warmup = 10
explore_team_warmup = 12
explore_team_delete = 15
troop_add_warmup = 20

building_detect_reset = 10

building_detectallteam_reset = 1

troop_add_acti_time_for_period = 1
troop_add_acti_time_for_period_loose = 2

def getid()->str:
    global id_now
    idn = default_id_prefix + str(id_now).zfill(4)
    id_now = id_now + 1
    return idn

def getid_num(num:int)->list[str]:
    return [getid() for i in range(num)]

def refreshbuilding(building_name:str, offset_pixel:rw.frame.Coordinate = rw.frame.Coordinate(), 
                    warmup_add = building_add_warmup, 
                    reset_detect = building_detect_reset)->rw.object_group_useful.RefreshBuildingNoTeam:
    building = rw.object_group_useful.RefreshBuildingNoTeam\
    .init_base(offset_pixel, getid(), building_name, warmup_detect = -1, warmup_add = warmup_add, 
               reset_detect = reset_detect, reset_add = -1, 
               isonlybuilding = False)
    return building

troop_name_dict = {
    "lb": rw.const.UNIT.builder, 
    "lha": rw.const.UNIT.heavyArtillery, 
    "mg": rw.const.UNIT.mechGun, 
    "mb": rw.const.UNIT.mechBunker, 
    "md": rw.const.UNIT.mechBunkerDeployed, 
    "mm": rw.const.UNIT.mechMissile, 
    "bm": rw.const.UNIT.bugMeleeLarge, 
    "shc": rw.const.UNIT.hovercraft, 
    "ce": rw.const.UNIT.combatEngineer, 
    "me": rw.const.UNIT.mechEngineer
}

def troopstr_to_dict(troop_str:str)->dict[str, int]:
    if troop_str == '':
        return {}
    troop_list = troop_str.split(".")
    troop_dict = {}
    for troop in troop_list:
        troop_name = ''.join([troop_s for troop_s in troop if troop_s.isalpha()])
        troop_int = ''.join([troop_s for troop_s in troop if troop_s.isdigit()])
        troop_int = 1 if troop_int == '' else int(troop_int)
        troop_dict[troop_name_dict[troop_name]] = troop_int
    return troop_dict

troop_period = 60
troop_phase_num = 8

troop_add =[
    "A,13mg.lha.2shc.mm/1-0:7,3:5,1:1,1", 
    "A,3mg.3bm.2shc/1-2:7,3:5,4:3,4", 
    "S,24mg.3lha.3shc.2mm/1-1:7,3:9,3:13,3", 
    "S,6mg.6bm.4shc/1-3:7,3:9,3:13,3", 
]
# 阵营,兵力/相位-队伍:x,y...(撤退方向)
# 阵营,兵力/队伍*刷新时间+推迟时间-结束时间:x,y...(撤退方向)|所需城市(尚未执行)

for i, troop_now in enumerate(troop_add):
        
    troop_templist = troop_now.split(":")
    troop_pos_list = troop_templist[1:]
    for j, troop_pos_now in enumerate(troop_pos_list):
        troop_pos_xy = troop_pos_now.split(",")
        troop_pos_list[j] = rw.frame.Coordinate(int(troop_pos_xy[0]), 
                                                    int(troop_pos_xy[1]))

    troop_templist = hexcity.sutility.get_str_end_split(troop_templist[0], "-")
    troop_team = int(troop_templist[1]) if troop_templist[1] != "" else -1

    troop_templist = hexcity.sutility.get_str_end_split(troop_templist[0], "/")
    troop_phase_start = int(troop_templist[1])

    troop_templist = hexcity.sutility.get_str_end_split(troop_templist[0], ",")
    troop_dict = troopstr_to_dict(troop_templist[1])

    troop_teamgroup = 0 if troop_templist[0] == "A" else 1

    troop_add[i] = [troop_pos_list, troop_team, troop_phase_start, troop_dict, troop_teamgroup]

AV_need = 2
#SV_need = 12
is_SV_advance = True
is_AV_advance = False
victory_time = 480

city = {
    (3, 4): "Idritsa/伊德里察(1),1-V", 
    (1, 1): "Stanislavovo/斯坦尼斯拉夫沃(1),1-V", 
    (5, 1): "Nevel/涅维尔(1),1-V",
    (5, 4): "Pustoshka/普斯托什卡(1),1-V", 
    (7, 3): "Novosokolniki/新索科利尼基(2),1+2-V2",
    (9, 3): "Velikie Luki/大卢基(5),2+4-V5", 
    (9, 1): "+1", 
    (10, 2): "+1", 
    (11, 3): "+1", 
    (11, 4): "+1", 
    (13, 3): "Toropets/托罗佩茨(1),1-V", 
    (13, 1): "Zapadnaya Dvina/西德维纳(1),1-V", 
    (16, 4): "Adreapol/阿德雷波尔(1),1-V"
}

victory_text_size = 15
victory_text_offset_tile_x = 20
victory_text_offset_tile_y = 10

city_text_color = ["#000088", "#CC0033"]
city_text_size = list(range(8, 50, 6))

city_victory_chname = []
count_total_v = 0

for name, value in city.items():
        
    city_now_templist = hexcity.sutility.get_str_end_split(value, "-")
    city_victory = city_now_templist[1]

    city_now_templist = hexcity.sutility.get_str_end_split(city_now_templist[0], "+")
    city_fort_level = city_now_templist[1]

    city_now_templist = hexcity.sutility.get_str_end_split(city_now_templist[0], ",")
    city_level = city_now_templist[1] 
    city_name = city_now_templist[0]

    if city_victory != "":
        city_victory_chname.append(city_name.split("/")[1])
        count_total_v = count_total_v + (int(city_victory[1:]) if city_victory[1:] != "" else 1)

    city[name] = [city_name, city_level, city_fort_level, city_victory]

SV_need = count_total_v - AV_need + 1

building2_pos_tile_offset = [
    rw.frame.Coordinate(-1, -1), 

    rw.frame.Coordinate(-1, -5), 
    rw.frame.Coordinate(3, 1), 

    rw.frame.Coordinate(-2, -7), 
    rw.frame.Coordinate(0, -7), 
    rw.frame.Coordinate(4, -6), 
    rw.frame.Coordinate(5, 1), 
    rw.frame.Coordinate(4, 3), 

    rw.frame.Coordinate(-3, -9), 
    rw.frame.Coordinate(-1, -9), 
    rw.frame.Coordinate(1, -9), 
    rw.frame.Coordinate(5, -8), 
    rw.frame.Coordinate(6, -6), 
    rw.frame.Coordinate(7, 1), 
    rw.frame.Coordinate(6, 3), 
    rw.frame.Coordinate(5, 5), 
]

troop1_pos_tile_offset_h = [
    rw.frame.Coordinate(1, 0), 
    #rw.frame.Coordinate(1, -1), 
    rw.frame.Coordinate(1, -2), 
    #rw.frame.Coordinate(0, -2), 
    rw.frame.Coordinate(-1, -2), 
    #rw.frame.Coordinate(-2, -2), 

    #rw.frame.Coordinate(2, 0), 
    #rw.frame.Coordinate(1, -3), 
    rw.frame.Coordinate(-2, -3), 

    rw.frame.Coordinate(3, 0), 
    rw.frame.Coordinate(1, -4), 
    #rw.frame.Coordinate(-2, -4), 

    #rw.frame.Coordinate(4, 0), 
    #rw.frame.Coordinate(2, -4), 
    rw.frame.Coordinate(-3, -4), 

    rw.frame.Coordinate(5, 0), 
    rw.frame.Coordinate(2, -5), 
    #rw.frame.Coordinate(-3, -5), 
    
    #rw.frame.Coordinate(2, -6), 
    rw.frame.Coordinate(-3, -6), 

    rw.frame.Coordinate(3, -6), 
    #rw.frame.Coordinate(-4, -6), 
    
    #rw.frame.Coordinate(3, -7), 
    rw.frame.Coordinate(-4, -7),  
]
troop1_pos_tile_offset = []
for troop_pos in troop1_pos_tile_offset_h:
    troop1_pos_tile_offset.append(troop_pos)
    troop1_pos_tile_offset.append(-troop_pos - rw.frame.Coordinate(1, 1))

building3_pos_tile_offset = [
    rw.frame.Coordinate(3, -4), 
    rw.frame.Coordinate(6, -4)
]

building3_index = [1, 4]

city_level_to_reset = [10, 13, 17, 22, 28]

fort_reset = 40
# 1 2 3 4 5

terrain_operation = {
    "w":{"0": rw.const.UNIT.turret_flamethrower}, 
    "s":{"0": rw.const.UNIT.turret_artillery}, 
    "p":{"0": rw.const.UNIT.turret}, 
    "c":{"0": rw.const.UNIT.turretT2}
}

citylevel_operation = [
    {"0":rw.const.UNIT.turretT2}, 
    {"0":rw.const.UNIT.supplyDepot, 
     "2":rw.const.UNIT.supplyDepot, "1":rw.const.UNIT.turret, "1r":rw.const.UNIT.turret}, 
    {"0":rw.const.UNIT.supplyDepot, "2r":rw.const.UNIT.supplyDepot, 
     "2":rw.const.UNIT.supplyDepot, "3":rw.const.UNIT.supplyDepot, 
     "1":rw.const.UNIT.turret_flamethrower, 
     "1r":rw.const.UNIT.turretT2, 
     "t0":rw.const.UNIT.repairbay
     }, 
    {"0":rw.const.UNIT.supplyDepot, "2":rw.const.UNIT.supplyDepot, 
     "2r":rw.const.UNIT.supplyDepot, "3":rw.const.UNIT.supplyDepot, 
     "3r":rw.const.UNIT.supplyDepot, "1":rw.const.UNIT.turret_flamethrower, 
     "1r":rw.const.UNIT.turretT2, "t0":rw.const.UNIT.repairbay, 
     "4":rw.const.UNIT.turret_artillery, 
     "4r":rw.const.UNIT.antiAirTurret, "t1":rw.const.UNIT.outpostT1, 
     "5":rw.const.UNIT.turret_artillery, "5r":rw.const.UNIT.antiAirTurret
     }
]
'''
cityname,level:城市及名字,城市等级
1:1机枪
2:补给站+2炮塔
3:3补给站+1修复湾+1火焰+1机枪
4:6补给站+1修复湾+1瞭望塔+1火焰+1机枪+1火炮+1防空
5:10补给站+2修复湾+1瞭望塔+1火焰+1机枪+1火炮+4炮塔+1防空+1二级防空
-V 胜利点 
'''
'''
+fort level:额外防御等级
+几级填几个炮塔
'''

squareteam_troop = [
    ["0", "0"], 
    ["0", "0", "0", "2", "2"], 
    ["0", "0", "0", "2", "2", "2"], 
    ["0", "0", "0", "0", "2,6bm.2shc", "2", "2"],  
    ["0", "0", "0", "0", "0", "2", "2"], 
    ["0", "0", "0", "0", "0", "0", "0"], 
    ["0", "0", "0", "0", "0", "0", "0"], 
    ["0", "0", "0", "0,11mg.1mm.2shc-2", "0", "0", "0"], 
    ["0", "0", "0", "0", "0", "0", "0"], 
    ["0", "0,4mg", "0", "0,16mg.1mm.2shc.1me", "0", "0", "0"], 
    ["1", "1,14mg.2shc", "0,4mg.1shc", "0", "0", "0", "0"], 
    ["1", "1", "1,28mg.3lha.3shc.1me", "0,4mg", "0,4mg.1shc", "0", "0"], 
    ["1", "1", "1,20mg.3shc.1me", "3,28mg.2lha.1mm.3shc-1", "3,14mg.1mm.2shc", "3,3mg.1shc", "3"],
    ["1", "1", "1", "3,15bm.5shc.1me", "3,16mg.2shc", "3", "3"],
    ["1", "1", "1", "3", "3", "3", "3"],
    ["1", "1", "1", "3", "3", "3", "3"],
    ["1", "1", "1", "3", "3", "3", "3"],
    ["1", "1", "1", "3", "3", "3", "3"],
    ["1", "1", "1", "3", "3", "3", "3"],
    ["1", "1", "1", "3", "3", "3", "3"],
]
# 队伍
'''
,(number)name(-team).(...)
一次性单位
'''
squareteam = deepcopy([deepcopy(i) for i in squareteam_troop])
squaretroop = deepcopy([deepcopy(i) for i in squareteam_troop])
squaretroop_t = deepcopy([deepcopy(i) for i in squareteam_troop])

for x, squareteam_troop_y_list in enumerate(squareteam_troop):
    for y, squareteam_troop_now in enumerate(squareteam_troop_y_list):
        
        squareteam_troop_now_templist = hexcity.sutility.get_str_end_split(squareteam_troop_now, "-")
        squaretroop_t[x][y] = squareteam_troop_now_templist[1]

        squareteam_troop_now_templist = hexcity.sutility.get_str_end_split(squareteam_troop_now_templist[0], ",")
        squaretroop[x][y] = troopstr_to_dict(squareteam_troop_now_templist[1])

        squareteam[x][y] = int(squareteam_troop_now_templist[0])

        squaretroop_t[x][y] = squareteam[x][y] if squaretroop_t[x][y] == '' else int(squaretroop_t[x][y])

perchar = 0.1
background_color = "#FFC382"
story_ally_color = "#9ACDF5"
story_sov_color = "#EE0033"
story_axis_color = "#000066"
prompt_color = "green"
time_color = "yellow"
message_acti_reset = 15
message_tips_reset = 120



intro_text = \
f"\
城市争夺玩法2v2地图\
\n地图版本:V.{RWMAP_VERSION}\
\n地图官方群及发布点:699981990\
\n地图作者:咕咕咕\
\n地块使用:notTiled的V3模版,Xs的城夺地块集\
\n特别感谢斐比寻常W'213的教程,Xs的巴巴罗萨计划城夺地图\
\n本地图进行了自动化,\
\n参见:https://github.com/exgcdwu/\
\nRusted-Warfare-map-editor-for-city-occupation-play-"

time_line_str_length_1 = 44
time_line_str_length_2 = 39

time_line_interval = 2

map_message = [
    {"time": 1, "perchar": perchar, "color": prompt_color, "message": "地图正在初始化中,请等待20s,并阅读如下说明"},
    {"time": 4, "perchar": perchar, "color": prompt_color, "message": "本地图为城市争夺地图,地图上的炮塔和建筑可自动刷新"},
    {"time": 7, "perchar": perchar, "color": prompt_color, "message": "本地图提供初始兵力,同时兵力会自动刷新"},
    {"time": 10, "perchar": perchar, "color": prompt_color, "message": "特殊兵种:机械师可以缓慢建设城防"},
    {"time": 12, "perchar": perchar, "color": prompt_color, "message": "上方有当前占领分数和目标分数,城市的占领分数在名称后面的括号内"},
    {"time": 14, "perchar": perchar, "color": story_axis_color, "message": f"德军目标:1943年1月9日({int(victory_time/60)}分钟)之前占领分数保持在{AV_need}分及以上", "reset": message_tips_reset},
    {"time": 17, "perchar": perchar, "color": story_sov_color, "message": f"苏军目标:1943年1月9日({int(victory_time/60)}分钟)之前占领分数达到{SV_need}分", "reset": message_tips_reset},
    {"time": troop_add_warmup, "perchar": perchar, "color": time_color, "message": "======游戏报时:1942年11月8日(游戏开始)======", "timeline": time_line_str_length_2}, 

    {"time": troop_add_warmup + 11 * victory_time / 60, "perchar": perchar, "color": story_ally_color, "message": "1942年11月19日,于此同时,苏联红军开始实施天王星行动"},
    {"time": troop_add_warmup + 15 * victory_time / 60, "perchar": perchar, "color": story_ally_color, "message": "1942年11月23日,随着侧翼仆从国军队的溃败,德第六集团军在斯大林格勒被包围"},

    {"time": troop_add_warmup + 16 * victory_time / 60, "perchar": perchar, "color": time_color, "message": f"======游戏报时:1942年11月24日(还剩大约{int(victory_time*3/4/60)}分钟)======", "timeline": time_line_str_length_1}, 

    {"time": victory_time / 2 + troop_add_warmup, "perchar": perchar, "color": time_color, "message": f"======游戏报时:1942年12月8日(还剩大约{int(victory_time/2/60)}分钟)======", "timeline": time_line_str_length_1},   

    {"time": troop_add_warmup + 34 * victory_time / 60, "perchar": perchar, "color": story_ally_color, "message": "1942年12月12日,曼施坦因元帅发起代号为\"冬季风暴\"的反攻,试图拯救斯大林格勒地区被围的德军"},

    {"time": troop_add_warmup + 45 * victory_time / 60, "perchar": perchar, "color": time_color, "message": f"======游戏报时:1942年12月23日(还剩大约{int(victory_time*1/4/60)}分钟)======", "timeline": time_line_str_length_1},   

    {"time": troop_add_warmup + 49 * victory_time / 60, "perchar": perchar, "color": story_ally_color, "message": "1942年12月27日,第六集团军并未随顿河集团军群突围,曼施坦因的解围行动最终失败"},

    {"time": victory_time + troop_add_warmup, "perchar": perchar, "color": time_color, "message": f"======游戏报时:1943年1月9日(游戏结束)======", "timeline": time_line_str_length_2},  

    {"time": troop_add_warmup + 61 * victory_time / 60, "perchar": perchar, "color": story_ally_color, "message": "1943年1月10日,苏军发动了代号为\"指环\"的围歼战,目标是彻底歼灭第六集团军"},
    {"time": troop_add_warmup + 84 * victory_time / 60, "perchar": perchar, "color": story_ally_color, "message": "1943年2月3日,斯大林格勒包围圈内的德军已基本肃清"},


    {"perchar": perchar, "color": story_sov_color, "message": "苏军排山倒海的攻势瓦解了德军在大卢基附近的防御并将其占领", "acti": ".9,3-SV"}, 
    {"perchar": perchar, "color": story_sov_color, "message": "苏军跨过河流并迅速攻克了新索科利尼基,火星行动取得一定进展", "acti": ".7,3-SV"}, 

    #{"perchar": perchar, "color": story_sov_color, "message": "苏军占领斯坦尼斯拉夫沃", "acti": ".1,1-SV"}, 
    #{"perchar": perchar, "color": story_sov_color, "message": "苏军占领伊德里察", "acti": ".3,4-SV"}, 
    #{"perchar": perchar, "color": story_sov_color, "message": "苏军占领涅维尔", "acti": ".5,1-SV"}, 

    {"perchar": perchar, "color": story_sov_color, "message": "大卢基地区的德军余部基本被肃清,苏军取得胜利", "acti": "/SV", "reset": message_acti_reset}, 
    {"perchar": perchar, "color": story_axis_color, "message": "随着德军的持续抵抗,苏军未能完全占领大卢基及附近地区,德军取得胜利", "acti": "/AV", "reset": message_acti_reset}, 
]

trigger_pos_y_now = 0
trigger_pos_now = rw.frame.Coordinate(0, 0)

def get_trigger_pos(size:rw.frame.Coordinate = rw.frame.Coordinate(200, 100), is_column:bool = False)->rw.frame.Coordinate:
    global trigger_pos_y_now
    global trigger_pos_now
    coor_ans = trigger_pos_now
    if not is_column:
        trigger_pos_now = rw.frame.Coordinate(0, trigger_pos_y_now)
    coor_ans = trigger_pos_now - rw.frame.Coordinate(0, size.y())
    trigger_pos_y_now = min(trigger_pos_y_now, trigger_pos_now.y() - size.y())
    trigger_pos_now = trigger_pos_now + rw.frame.Coordinate(size.x(), 0)



    return coor_ans


def offset_translation(dict_name:str, isreverse:bool)->rw.frame.Coordinate:
    dict_int = int(''.join([char for char in dict_name if not char.isalpha()]))
    if dict_name.find("t") != -1:
        return_ans = deepcopy(building3_pos_tile_offset[dict_int])
        reverse_int = 3
    else:
        return_ans = deepcopy(building2_pos_tile_offset[dict_int])
        reverse_int = 2

    if (dict_name.find("r") != -1) ^ isreverse:
        return_ans = -return_ans - rw.frame.Coordinate(reverse_int, reverse_int)
    return [return_ans, dict_int]
        

def an_operation_translation(square_hex_x:rw.frame.Coordinate, dict_name:str, dict_value:str, 
                             team:int, reset:int, fort_warmup:int, fort_reset:int, isreverse:bool, iscityexp:bool, deacti_oid = None, acti_oid = None)\
     ->list[list[rw.tile.TileGroup_One], rw.frame.TagCoordinate, list]:
    off_trans = offset_translation(dict_name, isreverse)
    offset_grid = off_trans[0]
    issupply = True if (off_trans[1] == 0 and dict_name.find("t") == -1) else False
    if dict_value == rw.const.UNIT.supplyDepot:
        issupply = True

    tile_layer = pos_tile_layer(square_hex_x, offset_grid = rw.frame.Coordinate(offset_grid.y(), offset_grid.x()))
    pixel_object = pos_pixel_object(square_hex_x, offset_grid = offset_grid)
    object_group = []
    tilegroup_one_list = []

    tobject_now = None
    detect_now = None
    if issupply:

        pixel_object = pixel_object + rw.frame.Coordinate(10, 10)
        pixel_object_1 = pixel_object - rw.frame.Coordinate(1, 1)
        real_unit = rw.const.UNIT.turret if dict_value == rw.const.UNIT.supplyDepot else dict_value

        building = refreshbuilding(real_unit, pixel_object, fort_warmup, 
                                        fort_reset)
        if team != -1:
            tobject_now = rw.object_useful.UnitAdd(pixel_object, team, real_unit)

        if deacti_oid != None:
            building.add_deactiBy_s(deacti_oid)
        detect_now = rw.object_useful.UnitDetect(pixel_object, rw.const.COO.SIZE_STANDARD, 
                                                 maxUnits = 0, unitType = real_unit, warmup = fort_warmup, 
                                                 reset = fort_reset, id = getid())
        
        object_group.append(building)
        object_group.append(refreshbuilding(rw.const.UNIT.supplyDepot, pixel_object_1, 
                                            reset))
        if iscityexp:
            tilegroup_one_list.append(tilegroup_city_PathingOverride) 
        tilegroup_one_list.append(tilegroup_city_item2)

    else:
        pixel_object = pixel_object + (rw.frame.Coordinate(20, 20) if dict_name.find("t") != -1 else rw.frame.Coordinate(10, 10))
        object_group.append(refreshbuilding(dict_value, pixel_object, 
                                            reset))
        tilegroup_one_list.append(tilegroup_fort_item2 if dict_name.find("t") == -1 else tilegroup_fort_item3)
        
    return [tilegroup_one_list, tile_layer, object_group, tobject_now, detect_now]
    
def an_message_translation(message_dict:dict):
    time_now = -1
    if message_dict.get("time") != None:
        time_now = message_dict["time"]

    message_now = message_dict["message"]

    perchar_now = -1
    if message_dict.get("perchar") != None:
        perchar_now = message_dict["perchar"]

    color_now = None
    if message_dict.get("color") != None:
        color_now = message_dict["color"]

    reset_now = -1
    if message_dict.get("reset") != None:
        reset_now = message_dict["reset"]

    time_line = 0
    if message_dict.get("timeline") != None:
        time_line = message_dict["timeline"]

    message_now = [rw.object_useful.Message(city_origin_object_pixel, message_now, 
                                           delayPerChar = perchar_now, 
                                           warmup = time_now, textColor = color_now, 
                                           reset = reset_now)]
    if time_line != 0:
        message_now.append(rw.object_useful.Message(city_origin_object_pixel, "=" * time_line, 
                                           delayPerChar = perchar_now, 
                                           warmup = time_now - time_line_interval, 
                                           textColor = color_now))
        message_now.append(rw.object_useful.Message(city_origin_object_pixel, "=" * time_line, 
                                           delayPerChar = perchar_now, 
                                           warmup = time_now + time_line_interval, 
                                           textColor = color_now))

    return message_now

squaretroop_add_pos_em = [[np.zeros((len(troop1_pos_tile_offset), troop_phase_num), dtype = np.bool_)  for j in i] for i in squareteam_troop]

def find_apos_offset_id_troop_add(pos:rw.frame.Coordinate, troop_phase_now:int)->int:
    for i in range(len(troop1_pos_tile_offset)):
        if not squaretroop_add_pos_em[pos.x()][pos.y()][i, troop_phase_now]:
            squaretroop_add_pos_em[pos.x()][pos.y()][i, troop_phase_now] = True
            return troop1_pos_tile_offset[i]

def an_troopadd_translation(troop_pos_list:list, troop_phase_start:int, troop_name:str, 
                            troop_team_group:int, troop_team:int, detect_tgroup:list[list[list[rw.object_group_useful.BuildingDetect]]], 
                            troop_ctrl_list:list[rw.object_group_useful.Flash], troop_ctrl_all:rw.object_group_useful.Flash)->list[rw.object_useful.UnitAdd]:
    unitAdd_list = []
    for troop_name_now, troop_quan in troop_name.items():
        troop_phase_start_now = troop_phase_start
        troop_quan_use = 0
        while troop_quan_use < troop_quan:
            if troop_quan - troop_quan_use >= troop_phase_num - troop_phase_start_now:
                troop_phase_use_now = [i + troop_phase_start_now for i in range(troop_phase_num - troop_phase_start_now)]
                troop_phase_start_now = 0
                troop_quan_use = troop_quan_use + (troop_phase_num - troop_phase_start_now)
            else:
                troop_phase_use_now = [i + troop_phase_start_now for i in range(troop_quan - troop_quan_use)]
                troop_phase_start_now = (troop_phase_start_now + (troop_quan - troop_quan_use))
                troop_quan_use = troop_quan

            for index_t, troop_pos in enumerate(troop_pos_list):
                pos_pixel_object_now = pos_pixel_object(troop_pos) + find_apos_offset_id_troop_add(troop_pos, troop_phase_start_now) * tile_size
                deactiBy_s_list = [troop_ctrl_all.idTObject_s()] if len(troop_phase_use_now) == 5 else [troop_ctrl_list[i].idTObject_s() for i in troop_phase_use_now]
                actiBy_s_list = []
                for index, i in enumerate(detect_tgroup[troop_pos.x()][troop_pos.y()]):
                    if index != troop_team_group:
                        deactiBy_s_list = deactiBy_s_list + i.idTObject_s()
                if index_t != 0:
                    for index, i in enumerate(detect_tgroup[troop_pos_list[index_t - 1].x()][troop_pos_list[index_t - 1].y()]):
                        if index == troop_team_group:
                            deactiBy_s_list = deactiBy_s_list + i.idTObject_s()

                unitAdd_list.append(rw.object_useful.UnitAdd(pos_pixel_object_now, troop_team, troop_name_now, warmup = troop_add_warmup, 
                                         deactiBy_s = deactiBy_s_list
                                         #, actiBy_s = actiBy_s_list, isalltoacti = True
                                         ))
    return unitAdd_list



    

    

def pos_tile_cart(square_hex_x:rw.frame.Coordinate)->rw.frame.Coordinate:
    square_hex_x_float = rw.frame.Coordinate(square_hex_x.x(), square_hex_x.y(), dtype = np.float32)
    square_ori_cart = square_hex_x_float * project_hex_x_to_cart
    square_ld_cart = square_ori_cart + origin_square
    square_lt_cart = square_ld_cart - rw.frame.Coordinate(0, map_size_square.y(), dtype = np.float32)
    tile_lt_cart = square_lt_cart * square_size_tile
    tile_lt_cart_int = rw.frame.Coordinate(tile_lt_cart.x(), tile_lt_cart.y())
    return tile_lt_cart_int

def pos_tile_object(square_hex_x:rw.frame.Coordinate, offset_grid:rw.frame.Coordinate = rw.frame.Coordinate(0, 0))->rw.frame.Coordinate:
    tile_lt_cart = pos_tile_cart(square_hex_x)
    tile_lt_tobject_coo = tile_lt_cart * project_cart_to_tobject_coo
    tile_lt_tobject_coo_offset = tile_lt_tobject_coo + offset_grid
    return tile_lt_tobject_coo_offset

def pos_pixel_object(square_hex_x:rw.frame.Coordinate, offset_grid:rw.frame.Coordinate = rw.frame.Coordinate(0, 0), offset_pixel:rw.frame.Coordinate  = rw.frame.Coordinate(0, 0))->rw.frame.Coordinate:
    pixel_lt_tobject_coo_offset = pos_tile_object(square_hex_x, offset_grid) * tile_size
    return pixel_lt_tobject_coo_offset + offset_pixel

def pos_tile_layer(square_hex_x:rw.frame.Coordinate, offset_grid:rw.frame.Coordinate = rw.frame.Coordinate(0, 0))->rw.frame.Coordinate:
    tile_lt_cart = pos_tile_cart(square_hex_x)
    tile_lt_cart_layer_coo = tile_lt_cart * project_cart_to_layer_coo
    tile_lt_cart_layer_coo_offset = tile_lt_cart_layer_coo + offset_grid
    return tile_lt_cart_layer_coo_offset

def pos_tile_to_pixel(coo_grid:rw.frame.Coordinate, offset_pixel:rw.frame.Coordinate  = rw.frame.Coordinate(0, 0))->rw.frame.Coordinate:
    return (tile_size * coo_grid) + offset_pixel