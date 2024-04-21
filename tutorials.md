# Tutorials

[toc]

## 使用之前

### 1.使用地图编辑器(Tiled,notTiled)创建新地图

地图格式：zlib、gzip

渲染顺序：右下(right-down)

方向：orthogonal

### 2.手动载入地块集

### 3.手动创建所需的地块层和宾语层

### 4.即可使用python库改变地块和宾语

## 基本操作命令

### 地图载入

```python
import rwmap as rw

map_dir = 'D:/Game/steam/steamapps/common/Rusted Warfare/mods/maps/'
map_name = '[p2]example_skirmish_(2p).tmx'
map_file = map_dir + map_name

mymap:rw.RWmap = rw.RWmap.init_mapfile(map_file)

```

### 地图输出（文本）

```python

print(mymap)
print(mymap.output_str(100, 100, rw.frame.Rectangle(rw.frame.Coordinate(0, 0), rw.frame.Coordinate(10, 10)), 50))

```

### 地图载出

```python

map_name_out = '[p2]example_skirmish_(2p).tmx'
mymap.write_file(map_dir + map_name_out)

```

## 宾语

### 宾语添加

#### 字典添加模式

朴素的宾语添加方式，默认属性和自定义属性不得填反。

```python

mymap.addObject(
    "Triggers", 
    {"name": "刷兵实验", "type": "unitAdd", "x": "1500", "y":"1100", "width": "20", "height": "20", "visible": "0"}, 
    {"resetActivationAfter":"5s", "spawnUnits": "heavyTank*10", "team" :"0", "warmup":"5s"})

mymap.addObject(
    "Triggers", 
    {"name": "刷兵实验", "type": "unitAdd", "x": "1000", "y":"1500", "width": "20", "height": "20"}, 
    {"resetActivationAfter":"5s", "spawnUnits": "heavyTank*10", "team" :"0", "warmup":"5s"})

```

#### 分组宾语添加模式

进阶宾语添加方式，分别将宾语的各个功能部分填写完整。

```python

initial_c = rw.frame.Coordinate(1200, 2000)
add_c = rw.frame.Coordinate(40, 40)
mymap.addObject_one(rw.object.TObject_One(rw.object.TObject_Type.init_unitAdd(0, "heavyTank*10"), 
                                    rw.object.TObject_Pos.init_rectangle(rw.frame.Rectangle(initial_c, add_c)), 
                                    time = rw.object.TObject_Time.init_time(warmup = 20, reset = 20)))
#建立一个自动刷兵点

```

#### 宾语组添加模式

使用现成的宾语组根据有限参数添加一组宾语。

```python

mymap.addObject_group(rw.object_group_useful.RefreshBuilding.init_building(rw.frame.Coordinate(1500, 1000), rw.frame.Coordinate(40, 40), 
                                               "turret", "acti_tu1", 10, 10,
                                               name_add = "城市添加", name_detect = "城市检测", 
                                               warmup_add = 10, warmup_detect = 5))
#建立一个可自动刷新的建筑

mymap.addObject_group(rw.object_group_useful.City.init_city(rw.frame.Coordinate(1500, 1500), rw.frame.Coordinate(40, 40), 
                                               "turret", "acti_tu2", 10, 10, "城市", textColor = "white", 
                                               textSize = 50, name_add = "城市添加", name_detect = "城市检测", 
                                               name_maptext = "城市文本", warmup_add = 10, warmup_detect = 5))
#建立一个自动刷新的城市，有名字

```

### 宾语搜索与操作

```python

for tobject in mymap.iterator_object("Triggers", {"y": "1500"}):#返回属性成功匹配正则表达式的宾语（生成器）
    del tobject#宾语被删除

for tobject in mymap.iterator_object("Triggers", {"y": "1100"}):
    tobject.assignDefaultProperty("name", "名字改变了")#宾语默认属性被赋值
    tobject.assignOptionalProperty("team", "1")#宾语可选属性被赋值
    print(tobject.returnDefaultProperty("name"))#输出宾语默认属性
    print(tobject.returnOptionalProperty("team"))#输出宾语可选属性
    tobject.deleteDefaultProperty("visible")#删除宾语默认属性
    tobject.deleteOptionalProperty("resetActivationAfter")#删除宾语可选属性

```

### 宾语组格式

可制作自己的宾语组

```python

class RefreshBuilding(rw.tobject.TObject_Group):
    @classmethod
    def init_building(cls, pos: rw.frame.Coordinate, size: rw.frame.Coordinate, spawnUnits:str, id_detect:str, 
                  reset_add:int, reset_detect:int, name_add:str = None, name_detect:str = None, 
                  warmup_add:int = -1, warmup_detect:int = -1, techLevel:int = -1):
        uadd = rw.object_useful.UnitAdd(pos, -1, spawnUnits, name = name_add, warmup = warmup_add, 
                                   reset = reset_add, techLevel = techLevel)
        udetect = rw.object_useful.UnitDetect(pos, size, name = name_detect, maxUnits = 0, 
                                         unitType = spawnUnits, warmup = warmup_detect, reset = reset_detect, 
                                         id = id_detect)
        tobn = udetect.return_idTObject()
        uadd.add_actiBy([tobn])
        return cls([uadd, udetect])

#可自动刷新的建筑示例

```

## 地块

### 地块添加

#### 单个地块

```python

mymap.addTile("Ground", rw.frame.Coordinate(1, 0), "Long Grass", rw.frame.Coordinate(0, 0))
mymap.addTile("Ground", rw.frame.Coordinate(2, 0), "Long Grass", rw.frame.Coordinate(1, 2))
mymap.addTile("Ground", rw.frame.Coordinate(0, 1), "Long Grass", rw.frame.Coordinate(0, 0))
#改变地块类型：第一项地块层名称，第二项地块层改变位置，第三项地块集名称（全名），第四项所用地块位置（在地块集中）

```

#### 矩形地块

```python

mymap.addTile_square("Ground", rw.frame.Rectangle(rw.frame.Coordinate(5, 5), rw.frame.Coordinate(10, 10)), "Deep Water", rw.frame.Coordinate(0, 0))
mymap.addTile_square("Ground", rw.frame.Rectangle(rw.frame.Coordinate(20, 5), rw.frame.Coordinate(30, 10)), "Long Grass", rw.frame.Coordinate(2, 1))
#改变地块类型（矩形）：第一项地块层名称，第二项地块层改变位置（前者为起始位置，后者为增量），第三项地块集名称（全名），第四项所用地块位置（在地块集中）

```

#### 地块组

```python

mymap.addTile_group(rw.frame.Coordinate(5, 20), rw.tile_group_useful.fill_tile_group_one_ground_water_28_24)
#改变地块类型（地块组）：第一项位置，第二项地块组（使用默认）

```

### 地块组格式

```python

tilegroup_matrix = rw.tile.TileGroup_Matrix([['a'] * 6  if i % 2 == 0 else ['b'] * 6 for i in range(10)])
#创建匿名地块组
tilegroup_addlayer = rw.tile.TileGroup_AddLayer.init_tilegroup_matrix("Ground", tilegroup_matrix)
#匿名地块组确定地块层
tile_dict = {
    "a": rw.frame.Coordinate("Long Grass", rw.frame.Coordinate(0, 0)), 
    "b": rw.frame.Coordinate("Dirt", rw.frame.Coordinate(0, 0))
}
tilegroup_one = rw.tile.TileGroup_One.init_tilegroup_addlayer(
    tile_dict, tilegroup_addlayer)
#匿名地块组确定地块类型

mymap.addTile_group(rw.frame.Coordinate(20, 20), tilegroup_one)
#添加地块组

```
