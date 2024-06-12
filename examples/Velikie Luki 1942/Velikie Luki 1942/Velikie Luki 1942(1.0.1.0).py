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
from Velikie_Luki_1942_data_1_0_1_0 import *



lukimap = rw.RWmap.init_mapfile(f'{current_dir_path}\\Velikie Luki 1942(basic map and ground)({RWMAP_GROUND_VERSION}).tmx')
# 反攻大卢基地块地图输入

origin = rw.frame.Coordinate(0, 0)
lukimap.addObject_one(rw.object_useful.Mapinfo(origin, rw.const.MAPTYPE.skirmish, 
                                                rw.const.FOG.los, rw.const.WIN.mainBuildings, 
                                                text = intro_text))
#添加map_info

credit_pos = rw.frame.Coordinate(0, -20)
for i in range(team_num):
    lukimap.addObject_one(rw.object_useful.Credit(credit_pos, i, setCredits = 0, reset = 1))
#添加credit重置
ini_exi = hexcity.tgroup.initial_exist_tile(list(range(team_num)))
lukimap.addTile_group(ini_exi[0], 
                      rw.frame.Coordinate())
lukimap.addObject_one(rw.object_useful.UnitRemove(rw.frame.Coordinate(), 
                                                  ini_exi[1], 
                                                  warmup = explore_warmup_and_initial))

detect_tgroup:list[list[list[rw.object_group_useful.BuildingDetect]]] = deepcopy([deepcopy(i) for i in squareteam_troop])
detect_worker_tgroup:list[list[rw.tobject.TObject_One]] = deepcopy([deepcopy(i) for i in squareteam_troop])
for x, detect_tgroup_y_list in enumerate(detect_tgroup):
    for y, detect_tgroup_now in enumerate(detect_tgroup_y_list):
        tile_now = pos_tile_layer(rw.frame.Coordinate(x, y))
        end_point = lukimap.end_point_layer()
        if tile_now.x() < -square_size_tile.y() / 4 or tile_now.y() < -square_size_tile.x() / 4 or\
            tile_now.x() > (end_point.x() + (square_size_tile.y() / 4)) or tile_now.y() > (end_point.y() + (square_size_tile.x() / 4)):
            continue
        pos_pixel_object_now = pos_pixel_object(rw.frame.Coordinate(x, y), offset_pixel = city_origin_object_pixel)
        pos_pixel_object_mid = pos_pixel_object(rw.frame.Coordinate(x, y))
        detect_tgroup[x][y] = [rw.object_group_useful.BuildingDetect(pos_pixel_object_now, [getid() for i in range(len(team_list[i]))], -1, 
                                                                    building_detectallteam_reset, unitType_andob = rw.const.UNIT.supplyDepot, team = team_list[i], 
                                                                    minUnits = 1)
        for i in range(team_group)
        ]
        detect_worker_tgroup[x][y] = rw.tobject.TObject_One(
                rw.tobject.TObject_Type.init_unitDetect(team = None, maxUnits = 0, unitType = rw.const.UNIT.mechEngineer), 
                pos = rw.tobject.TObject_Pos.init_rectangle(rw.frame.Rectangle(
                    -square_size_pixel / 2 + pos_pixel_object_mid, 
                    square_size_pixel)), 
                acti = rw.tobject.TObject_Acti.init_acti(getid()), 
                time = rw.tobject.TObject_Time.init_time(reset = fort_reset)
            )
        '''
        detect_worker_tgroup[x][y] = rw.tobject.TObject_One(
                rw.tobject.TObject_Type.init_unitDetect(team = None, maxUnits = 0, unitType = rw.const.UNIT.mechEngineer), 
                pos = rw.tobject.TObject_Pos.init_polygon(hex_x_shape, pos_pixel_object_mid), 
                acti = rw.tobject.TObject_Acti.init_acti(getid()), 
                time = rw.tobject.TObject_Time.init_time(reset = fort_reset)
            )
        '''
        lukimap.addObject_one(detect_worker_tgroup[x][y])
        for i in range(team_group):
            lukimap.addObject_group(detect_tgroup[x][y][i])
    #检测部署

for x, terrain_y_list in enumerate(terrain):
    for y, terrain_now in enumerate(terrain_y_list):
        tile_now = pos_tile_layer(rw.frame.Coordinate(x, y))
        end_point = lukimap.end_point_layer()
        if tile_now.x() < -square_size_tile.y() / 4 or tile_now.y() < -square_size_tile.x() / 4 or\
            tile_now.x() > (end_point.x() + (square_size_tile.y() / 4)) or tile_now.y() > (end_point.y() + (square_size_tile.x() / 4)):
            continue
        railway_now = hexcity.direction.str_to_NESbool(hexcity.lutility.get_listoflist_s(terrain, [x, y, 2]))
        railway_N = hexcity.direction.str_to_NESbool(hexcity.lutility.get_listoflist_s(terrain, [x, y + 1, 2]))
        railway_S = hexcity.direction.str_to_NESbool(hexcity.lutility.get_listoflist_s(terrain, [x - 1, y - 1, 2]))
        railway_W = hexcity.direction.str_to_NESbool(hexcity.lutility.get_listoflist_s(terrain, [x - 1, y, 2]))

        railway_N_CW_bool = railway_now + [railway_S[0], railway_W[1], railway_N[2]]

        terrain_now_tile = deepcopy(terrain_now[0])
        if city.get((x, y)) != None:
            continue
        if terrain_now_tile == "e":
            continue
        if sum(railway_N_CW_bool) != 0:
            terrain_now_tile = "c"
        for name, value in terrain_operation[terrain_now_tile].items():
            operation = an_operation_translation(rw.frame.Coordinate(x, y), name, value, int(squareteam[x][y]), 
                                                 building_detect_reset, fort_reset + troop_add_warmup, fort_reset, False, False, 
                                                 deacti_oid = detect_worker_tgroup[x][y].idTObject_s())
            for tilegroup in operation[0]:
                lukimap.addTile_group(tilegroup, operation[1])

            for objectgroup in operation[2]:
                lukimap.addObject_group(objectgroup)
    # 野外防御



victory_c:list[rw.object_group_useful.VictoryCO] = []
for i in range(team_group):
    victory_c.append(rw.object_group_useful.VictoryCO(rw.frame.Coordinate(), team_list[i]))
    #胜利部署

victory_city_detect_AV = []
victory_city_detect_SV = []
city_victory_count = []

for name, value in city.items():
    city_name = value[0]
    city_level = int(value[1]) if value[1] != '' else 0
    city_fort_level = int(value[2]) if value[2] != '' else 0
    city_victory = 1 if value[3] != "" else 0
    if city_victory == 1:
        city_victory = int(value[3][1:]) if value[3][1:] != "" else 1
    x = int(name[0])
    y = int(name[1])
    tile_now = pos_tile_layer(rw.frame.Coordinate(x, y))
    if tile_now.x() < -square_size_tile.y() / 4 or tile_now.y() < -square_size_tile.x() / 4:
        continue
    pos_grid = pos_tile_layer(rw.frame.Coordinate(x, y))

    railway_now = hexcity.direction.str_to_NESbool(hexcity.lutility.get_listoflist_s(terrain, [x, y, 2]))
    railway_N = hexcity.direction.str_to_NESbool(hexcity.lutility.get_listoflist_s(terrain, [x, y + 1, 2]))
    railway_S = hexcity.direction.str_to_NESbool(hexcity.lutility.get_listoflist_s(terrain, [x - 1, y - 1, 2]))
    railway_W = hexcity.direction.str_to_NESbool(hexcity.lutility.get_listoflist_s(terrain, [x - 1, y, 2]))

    railway_N_CW_bool = railway_now + [railway_S[0], railway_W[1], railway_N[2]]

    team_now = int(squareteam[x][y])  
    isreverse = False if team_now % 2 != 0 else True
    operation_now = citylevel_operation[city_level] if city_level != 0 else terrain_operation[terrain[x][y][0] if sum(railway_N_CW_bool) == 0 else "c"]

    fort_now = 0
    iscityexp = True if city_name != '' else False
    detect_pre = None

    for name, value in operation_now.items():
        if fort_now < city_fort_level:
            team = int(squareteam[x][y])
            fort_now = fort_now + 1
        else:
            team = -1
        deacti_oid_now = [detect_worker_tgroup[x][y].idTObject_s()]
        if detect_pre != None:
            deacti_oid_now.append(detect_pre.idTObject_s())
        operation = an_operation_translation(rw.frame.Coordinate(x, y), name, value, team, 
                                                city_level_to_reset[city_level], 
                                                fort_reset + troop_add_warmup, 
                                                fort_reset, isreverse, iscityexp, 
                                                deacti_oid = deacti_oid_now)
        detect_pre = operation[4]
        if detect_pre != None:
            lukimap.addObject_one(detect_pre)

        for tilegroup in operation[0]:
            lukimap.addTile_group(tilegroup, operation[1])

        for objectgroup in operation[2]:
            lukimap.addObject_group(objectgroup.unitDetect_s())
        for objectgroup in operation[2]:
            lukimap.addObject_group(objectgroup.unitAdd_s())

        if operation[3] != None:
            lukimap.addObject_one(operation[3])

    if city_victory != 0:
        city_victory_count.append(city_victory)
        victory_city_detect_AV.append(detect_tgroup[x][y][0].idTObject_s())
        victory_city_detect_SV.append(detect_tgroup[x][y][1].idTObject_s())
    #城市部署
    if city_name != "":
        city_name_now = city_name.split("/")[1]
        pos_pixel_object_now = pos_pixel_object(rw.frame.Coordinate(x, y), offset_pixel = city_origin_object_pixel)
        city_text = [rw.object_group_useful.CityTextAllTeam(pos_pixel_object_now, [city_name_now for j in team_list[i]], 
                                                            textColor = [city_text_color[i] for j in team_list[i]], 
                                                            textSize = city_text_size[city_level], 
                                                            actiBy_s_list = detect_tgroup[x][y][i].idTObject_s()) for i in range(team_group)]
        detect_id = []
        for j in detect_tgroup[x][y]:
            detect_id = detect_id + j.idTObject_s()
        city_text_mid = rw.object_group_useful.CityTextAllTeam(pos_pixel_object_now, [city_name_now], 
                                                            textSize = city_text_size[city_level], 
                                                            deactiBy_s_list = detect_id)
        lukimap.addObject_group(city_text_mid)
        for city_text_i in city_text:
            lukimap.addObject_group(city_text_i)

site_num_v = len(victory_city_detect_AV)

manycount_victory = rw.object_group_useful.ManyCount(rw.frame.Coordinate(), site_num_v, 
                                                     1, 1, 1, getid_num(site_num_v), getid_num(count_total_v + 1), getid_num(count_total_v + 1), 
                                                     count_num = city_victory_count)
for x in range(site_num_v):
    manycount_victory.Count_s(x).add_actiBy_s(victory_city_detect_AV[x])
    manycount_victory.Count_s(x).add_deactiBy_s(victory_city_detect_SV[x])

vic_text_pos = rw.frame.Coordinate(lukimap.size().x() * lukimap.tile_size().x() / 2, square_size_pixel.y() / 2)
vic_text_offset_y = rw.frame.Coordinate(0, tile_size.y() * victory_text_offset_tile_y)
vic_text_offset_x = rw.frame.Coordinate(tile_size.x() * victory_text_offset_tile_x, 0)
vic_text_pos_AV = vic_text_pos - vic_text_offset_x
vic_text_pos_SV = vic_text_pos + vic_text_offset_x

vic_text_AV = rw.object_group_useful.ScoreText(vic_text_pos_AV, count_total_v, 
                                               victory_text_size, prefix = "轴心占领分数:", size = tile_size, 
                                               textColor = city_text_color[0], 
                                               actiBy_s_list = [manycount_victory.Count_geq_idObject_s(i) for i in range(count_total_v + 1)],
                                               deactiBy_s_list = [manycount_victory.Count_geq_idObject_s(i + 1) for i in range(count_total_v)])

vic_text_AV_goal = rw.object_useful.MapText(vic_text_pos_AV + vic_text_offset_y, 
                                            f"轴心保持分数:{AV_need}", textColor = 
                                            city_text_color[0], textSize = victory_text_size)

vic_text_SV = rw.object_group_useful.ScoreText(vic_text_pos_SV, count_total_v, 
                                               victory_text_size, prefix = "苏联占领分数:", size = tile_size, 
                                               textColor = city_text_color[1], 
                                               actiBy_s_list = [manycount_victory.Count_leq_idObject_s(count_total_v - i) for i in range(count_total_v + 1)],
                                               deactiBy_s_list = [manycount_victory.Count_leq_idObject_s(count_total_v - i - 1) for i in range(count_total_v)])

vic_text_SV_goal = rw.object_useful.MapText(vic_text_pos_SV + vic_text_offset_y, 
                                            f"苏联胜利分数:{SV_need}", textColor = 
                                            city_text_color[1], textSize = victory_text_size)

victory_c[1].add_deactiBy_s(manycount_victory.Count_leq_idObject_s(AV_need - 1))
victory_c[0].add_deactiBy_s(manycount_victory.Count_geq_idObject_s(count_total_v - SV_need + 1))

timedelay = rw.object_group_useful.TimeDelay(rw.frame.Coordinate(), victory_time + troop_add_warmup, 
                                             getid())
timedelay_troop = rw.object_group_useful.TimeDelay(rw.frame.Coordinate(), troop_add_warmup, 
                                             getid())




for victory_c_i in victory_c:
    victory_c_i.add_deactiBy_s(timedelay_troop.idTObject_s())

if not is_AV_advance:
    victory_c[1].add_deactiBy_s(timedelay.idTObject_s())
if not is_SV_advance:
    victory_c[0].add_deactiBy_s(timedelay.idTObject_s())

for i, victory_c_i in enumerate(victory_c):
    lukimap.addObject_group(victory_c_i, get_trigger_pos())
lukimap.addObject_group(timedelay, get_trigger_pos())
lukimap.addObject_group(timedelay_troop, get_trigger_pos())
lukimap.addObject_group(manycount_victory, get_trigger_pos())
lukimap.addObject_group(vic_text_AV)
lukimap.addObject_group(vic_text_SV)
lukimap.addObject_one(vic_text_AV_goal)
lukimap.addObject_one(vic_text_SV_goal)
lukimap.addObject_one(rw.object_useful.Camera(vic_text_pos))

# 胜负结算部署

troop_ctrl_list = []
troop_ctrl_all = rw.object_group_useful.Flash(get_trigger_pos(), troop_add_warmup - troop_add_acti_time_for_period_loose, 
                                                        2 * troop_add_acti_time_for_period_loose, troop_period, getid())
lukimap.addObject_group(troop_ctrl_all)
for i in range(troop_phase_num):
    troop_ctrl_now = rw.object_group_useful.Flash(get_trigger_pos(tile_size * 2), troop_add_warmup + i * troop_period - troop_add_acti_time_for_period, 
                                                        troop_add_acti_time_for_period, troop_period * troop_phase_num, getid(), delayisdetect = False)
    lukimap.addObject_group(troop_ctrl_now)
    troop_ctrl_list.append(troop_ctrl_now)
# 兵力生产控制器


'''
acti_debug_now = victory_c[1].actiBy_s()
deacti_debug_now = victory_c[1].deactiBy_s()
for index, acti in enumerate(acti_debug_now):
    is_col = False if index == 0 else True
    acti_count = rw.object_group_useful.Count(get_trigger_pos(tile_size * 2, is_col), 
                                              1, 1, 1, getid())
    acti_count.add_actiBy_s(acti)
    print("1" + acti._name)
    lukimap.addObject_group(acti_count)

for index, deacti in enumerate(deacti_debug_now):
    is_col = False if index == 0 else True
    deacti_count = rw.object_group_useful.Count(get_trigger_pos(tile_size * 2, is_col), 
                                              1, 1, 1, getid())
    deacti_count.add_actiBy_s(deacti)
    print("2" + deacti._name)
    lukimap.addObject_group(deacti_count)

for index in range(total_v + 1):
    is_col = False if index == 0 else True
    acti_count = rw.object_group_useful.Count(get_trigger_pos(tile_size * 2, is_col), 
                                              1, 1, 1, getid())
    acti = manycount_victory.Count_leq_idObject_s(index)
    acti_count.add_actiBy_s(acti)
    print("3" + acti._name)
    lukimap.addObject_group(acti_count)

for index in range(total_v + 1):
    is_col = False if index == 0 else True
    acti_count = rw.object_group_useful.Count(get_trigger_pos(tile_size * 2, is_col), 
                                              1, 1, 1, getid())
    acti = manycount_victory.Count_geq_idObject_s(index)
    acti_count.add_actiBy_s(acti)
    print("4" + acti._name)
    lukimap.addObject_group(acti_count)
'''



for x, terrain_y_list in enumerate(terrain):
    for y, terrain_now in enumerate(terrain_y_list):
        tile_now = pos_tile_layer(rw.frame.Coordinate(x, y))
        if tile_now.x() < -square_size_tile.y() / 4 or tile_now.y() < -square_size_tile.x() / 4:
            continue
        pos_pixel_object_now = pos_pixel_object(rw.frame.Coordinate(x + 0.5, y, dtype = np.float32), offset_pixel = city_origin_object_pixel)
        for team_now in range(team_num):
            lukimap.addObject_one(rw.object_useful.UnitAdd(pos_pixel_object_now, team_now, rw.const.UNIT.outpostT2, warmup = explore_warmup_and_initial))
        lukimap.addObject_one(rw.object_useful.UnitRemove(pos_pixel_object_now, lukimap.tile_size(), warmup = explore_delete))
        pos_pixel_object_now2 = pos_pixel_object(rw.frame.Coordinate(x + 0.25, y, dtype = np.float32), offset_pixel = city_origin_object_pixel)
        lukimap.addObject_one(rw.object_useful.UnitAdd(pos_pixel_object_now2, int(squareteam[x][y]), rw.const.UNIT.outpostT2, warmup = explore_team_warmup))
        lukimap.addObject_one(rw.object_useful.UnitRemove(pos_pixel_object_now2, lukimap.tile_size(), warmup = explore_team_delete))

    # 地图初始化部署

for x, squaretroop_y_list in enumerate(squaretroop):
    for y, squaretroop_now in enumerate(squaretroop_y_list):
        tile_now = pos_tile_layer(rw.frame.Coordinate(x, y))
        if tile_now.x() < -square_size_tile.y() / 4 or tile_now.y() < -square_size_tile.x() / 4:
            continue
        pos_pixel_object_mid = pos_pixel_object(rw.frame.Coordinate(x, y))

        tid = 0
        for name, value in squaretroop_now.items():
            if (name == rw.const.UNIT.mechGun or name == rw.const.UNIT.hovercraft) and squaretroop_t[x][y] % 2 == 1:
                value = int(value / 3 * 2)
            for i in range(value):
                pos_pixel_object_now = pos_pixel_object_mid + troop1_pos_tile_offset[tid] * lukimap.tile_size()
                lukimap.addObject_one(rw.object_useful.UnitAdd(pos_pixel_object_now, squaretroop_t[x][y], name, warmup = troop_add_warmup))
                tid = tid + 1
    # 兵力部署

for index, troop in enumerate(troop_add):
    unitAdd_list = an_troopadd_translation(troop[0], troop[2], troop[3], troop[4], troop[1], 
                                           detect_tgroup, troop_ctrl_list, troop_ctrl_all)
    for unitAdd_now in unitAdd_list:
        lukimap.addObject_one(unitAdd_now)

    # 兵力生产部署

for message_dict in map_message:
    message_list = an_message_translation(message_dict)
    if message_dict.get("acti") != None:
        acti_str = message_dict["acti"]
        detect_ido = None
        if acti_str[0] == ".":
            acti_str_list = acti_str[1:].split("-")
            acti_side = acti_str_list[1]
            acti_str_list = acti_str_list[0].split(",")
            x = int(acti_str_list[0])
            y = int(acti_str_list[1])
            detect_ido = detect_tgroup[x][y][0] if acti_side == "AV" else detect_tgroup[x][y][1]
            detect_ido = detect_ido.idTObject_s()
            for message_now in message_list:
                message_now.add_actiBy_s(detect_ido)
        elif acti_str[0] == "/":
            acti_str_now = acti_str[1:]
            detect_ido = victory_c[1].deactiBy_s() if acti_str_now == "AV" else victory_c[0].deactiBy_s()
            for message_now in message_list:
                message_now.add_deactiBy_s(detect_ido)
        if detect_ido != None:
            for message_now in message_list:
                message_now.add_deactiBy_s(timedelay_troop.idTObject_s())
    for message_now in message_list:
        lukimap.addObject_one(message_now)
    # 广播计划






lukimap.write_file(f'{current_dir_path}\\Velikie Luki 1942({RWMAP_VERSION}).tmx')
# 输出地图到当前文件夹

maps_dir_path = "D:\\Game\\steam\\steamapps\\common\\Rusted Warfare\\mods\\maps"
lukimap.write_file(f'{maps_dir_path}\\  反攻大卢基(1942.11.8-1943.1.9)【4p,包围城夺】(V.{RWMAP_VERSION}).tmx')
lukimap.write_file(f'{maps_dir_path}\\攻防战测试【4p】(V.{RWMAP_VERSION}).tmx')
# 输出地图到游戏地图文件夹