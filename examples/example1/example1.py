import os
import sys
current_dir_path = os.path.dirname(os.path.abspath(__file__))
example_dir_path = os.path.dirname(current_dir_path)

package_dir = os.path.dirname(example_dir_path)
sys.path.append(package_dir)
#这两项可以省略，如果pip安装（确定包的位置）


import rwmap as rw

example1 = rw.RWmap.init_mapfile(f'{example_dir_path}\\example-empty\\example-empty.tmx')
# 一个200*200空地图 

grass = rw.frame.TagCoordinate("Short Grass", rw.frame.Coordinate(0, 0))
turret0 = rw.frame.TagCoordinate("units", rw.frame.Coordinate(0, 7))
turret1 = rw.frame.TagCoordinate("units", rw.frame.Coordinate(5, 7))
command0 = rw.frame.TagCoordinate("units", rw.frame.Coordinate(0, 6))
command1 = rw.frame.TagCoordinate("units", rw.frame.Coordinate(5, 6))
# 地块位置变量

origin = rw.frame.Coordinate(0, 0)
# 原点位置

credit_pos = rw.frame.Coordinate(0, 0)
# 添加资金改动宾语的位置

ground_graph = rw.frame.TagRectangle("Ground", rw.frame.Rectangle(
    rw.frame.Coordinate(0, 0), 
    rw.frame.Coordinate(200, 200)
))
# 整张地图的ground

example1.addTile_square(ground_graph, grass)
# ground被grass覆盖

id_prefix = "acti_tu"
id_now = 1
# 为城市检测提供id

def new_city_noteam(cityname:str, id_now:int)->rw.object_group_useful.CityNoTeam:
    building = rw.object_group_useful.RefreshBuildingNoTeam.init_base\
    (rw.frame.Coordinate(0, 0), id_prefix + str(id_now), "turret", -1, 20, 20, 20)
    city = rw.object_group_useful.CityNoTeam.init_bb(building, cityname, textSize = 12)
    return city
#城市建立函数

def new_troopadd()->rw.object_group_useful.RefreshTroop:
    return rw.object_group_useful.RefreshTroop(rw.frame.Coordinate(0, 0), -1, "c_tank", 
                                               20, 50)
#小坦生产函数

example1.addObject_one(rw.object_useful.Mapinfo(origin, rw.const.MAPTYPE.skirmish, 
                                                rw.const.FOG.los, rw.const.WIN.commandCenter, 
                                                text = "本地图宾语完全由宾语自动化完成。此为城夺刷兵地图例子1。\n\
                                                    使用普通的城市宾语组。"))
#添加map_info
example1.addObject_one(rw.object_useful.Credit(credit_pos, 0, setCredits = 0, reset = 1))
example1.addObject_one(rw.object_useful.Credit(credit_pos, 1, setCredits = 0, reset = 1))
#添加credit重置

for x in range(10, 200, 20):
    for y in range(10, 200, 20):
        # 循环建立城市与刷兵
        pos_building = rw.frame.Coordinate(2 * x + 1, 2 * y + 1) * example1.tile_size() / 2
        # 建筑位置
        pos_troopadd = rw.frame.Coordinate(2 * x + 3, 2 * y + 3) * example1.tile_size() / 2
        # 兵力位置
        if x < 100:
            example1.addTile(rw.frame.TagCoordinate.init_xy("Units", x, y), turret0)
        else:
            example1.addTile(rw.frame.TagCoordinate.init_xy("Units", x, y), turret1)
        # 玩家初始炮塔
        example1.addObject_group(new_city_noteam(f"城市({x},{y})", id_now), pos_building)
        # 添加城市
        id_now = id_now + 1
        # id变化
        example1.addObject_group(new_troopadd(), pos_troopadd)
        # 添加兵力刷新

example1.addTile(rw.frame.TagCoordinate("Units", rw.frame.Coordinate(10, 10)), command0)
# 玩家初始指挥中心
example1.addTile(rw.frame.TagCoordinate("Units", rw.frame.Coordinate(190, 190)), command1)
# 玩家初始指挥中心

example1.write_file(f'{current_dir_path}\\example1.tmx')
# 输出地图到当前文件夹

maps_dir_path = "D:\\Game\\steam\\steamapps\\common\\Rusted Warfare\\mods\\maps"
example1.write_file(f'{maps_dir_path}\\example1.tmx')
# 输出地图到游戏地图文件夹

