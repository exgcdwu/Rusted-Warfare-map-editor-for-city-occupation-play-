# Tutorials

- [Tutorials](#tutorials)
  - [使用之前](#使用之前)
    - [1.使用地图编辑器(Tiled,notTiled)创建新地图](#1使用地图编辑器tilednottiled创建新地图)
    - [2.手动载入地块集](#2手动载入地块集)
    - [3.手动创建所需的地块层和宾语层](#3手动创建所需的地块层和宾语层)
    - [4.即可使用python库改变地块和宾语](#4即可使用python库改变地块和宾语)
  - [基本操作命令](#基本操作命令)
    - [地图载入](#地图载入)
    - [地图输出（文本）](#地图输出文本)
    - [地图载出](#地图载出)
  - [宾语](#宾语)
    - [宾语添加](#宾语添加)
      - [字典添加模式](#字典添加模式)
      - [分组宾语添加模式](#分组宾语添加模式)
      - [宾语组添加模式](#宾语组添加模式)
    - [宾语搜索与操作](#宾语搜索与操作)
  - [地块](#地块)
    - [地块添加](#地块添加)
      - [单个地块](#单个地块)
      - [矩形地块](#矩形地块)
      - [地块组](#地块组)
    - [地块组格式](#地块组格式)

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

mymap = rw.RWmap.init_mapfile(map_dir + map_name)

```

### 地图输出（文本）

```python

print(mymap)
print(mymap.output_str(100, 100, rw.frame.Rectangle(rw.frame.Coordinate(0, 0), rw.frame.Coordinate(10, 10)), 50))

```

### 地图载出

注意，不建议输出到原地图文件，会造成文件覆盖。

文件覆盖会带来以下后果：

1.如果之后代码更改，将无法重新运行修改地图

2.如果操作错误或者库出现bug，将没有备份补救

```python

map_name_out = '[p2]example_skirmish_(2p)(1).tmx'
mymap.write_file(map_dir + map_name_out)

```

## 宾语

### 宾语添加

#### 字典添加模式

朴素的宾语添加方式，默认属性和自定义属性不得填反，属性字符串不得填错。

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
mymap.addObject_one(rw.tobject.TObject_One(rw.tobject.TObject_Type.init_unitAdd(0, "heavyTank*10"), 
                                    rw.tobject.TObject_Pos.init_rectangle(rw.frame.Rectangle(initial_c, add_c)), 
                                    time = rw.tobject.TObject_Time.init_time(warmup = 20, reset = 20)))
#建立一个自动刷兵点

```

#### 宾语组添加模式

使用现成的宾语组根据有限参数添加一组宾语。

现已更新建筑刷新宾语组，城市刷新宾语组（添加mapText），二者均可以提供任意队伍的检测接口。

已更新单位刷新宾语组，可以接受队伍检测接口。

```python

mymap.addObject_group(
    rw.object_group_useful.CityNoTeam.init_base\
    (rw.frame.Coordinate(1000, 1000), "acti_tu1", "城市", -1, 20, 20, 20))
# 建立一个补给站城市

```

### 宾语搜索与操作

```python

for tobject in mymap.iterator_object_s("Triggers", {"y": "1500"}):#返回属性成功匹配正则表达式的宾语（生成器）
    del tobject#宾语被删除

for tobject in mymap.iterator_object_s("Triggers", {"y": "1100"}):
    tobject.assignDefaultProperty("name", "名字改变了")#宾语默认属性被赋值
    tobject.assignOptionalProperty("team", "1")#宾语可选属性被赋值
    print(tobject.returnDefaultProperty("name"))#输出宾语默认属性
    print(tobject.returnOptionalProperty("team"))#输出宾语可选属性
    tobject.deleteDefaultProperty("visible")#删除宾语默认属性
    tobject.deleteOptionalProperty("resetActivationAfter")#删除宾语可选属性

```

## 地块

### 地块添加

#### 单个地块

```python

mymap.addTile(rw.frame.TagCoordinate("Ground", rw.frame.Coordinate(1, 0)), 126) 

#改变地块类型：第一项为地块位置（地块层名称+坐标），第二项提供三种参数（gid, 地块集名称+tileid，地块集名称+坐标）

```

#### 矩形地块

```python

tile1 = rw.frame.TagCoordinate("Deep Water", rw.frame.Coordinate(0, 0))
mymap.addTile_square(rw.frame.TagRectangle("Ground", rw.frame.Rectangle(rw.frame.Coordinate(5, 5), rw.frame.Coordinate(10, 10))), tile1)
#改变地块类型（矩形）：第一项为地块位置（地块层名称+矩形），第二项提供三种参数（gid, 地块集名称+tileid，地块集名称+坐标）

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
    "a": rw.frame.TagCoordinate("Long Grass", rw.frame.Coordinate(0, 0)), 
    "b": rw.frame.TagCoordinate("Dirt", rw.frame.Coordinate(0, 0))
}
tilegroup_one = rw.tile.TileGroup_One.init_tilegroup_addlayer(
    tile_dict, tilegroup_addlayer)
#匿名地块组确定地块类型

mymap.addTile_group(rw.frame.Coordinate(20, 20), tilegroup_one)
#添加地块组

```
