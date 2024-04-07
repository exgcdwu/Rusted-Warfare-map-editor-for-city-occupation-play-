# rwmapeditor-exgcdwu
___一个铁锈战争(Rusted Warfare)地图编辑python库___

[![released version](https://img.shields.io/pypi/v/rwmapeditor-exgcdwu.svg)][pypi]
[![license](https://img.shields.io/github/license/Gsllchb/rwmapeditor-exgcdwu.svg)][license]

## 目标

python实现铁锈地图文件地块编辑和宾语编辑。

暂时不打算接触地块集。

重点减轻城市争夺地图的宾语编辑工作量

基本框架已完成。

## 安装

pip install rwmapeditor-exgcdwu

## 简易使用例子

```python
# coding: utf-8
map_dir = 'D:/Game/steam/steamapps/common/Rusted Warfare/mods/maps/'
map_name = 'example_mission.tmx'
map_name_out = 'example_mission(1).tmx'
mygraph:rw.RWmap = rw.RWmap.init_graphfile(map_dir + map_name, map_dir)
print(mygraph.output_str())

mygraph.addObject("Triggers", {"id": "100","type": "unitAdd", "x": "1000", "y":"1000", "width": "20", "height": "20"}, {"resetActivationAfter":"5s", "spawnUnits": "heavyTank*10", "team" :"0", "warmup":"20s"})

mygraph.addTile("Ground", rw.Coordinate(1, 0), "Long Grass", rw.Coordinate(0, 0))
mygraph.addTile("Ground", rw.Coordinate(2, 0), "Long Grass", rw.Coordinate(0, 0))
mygraph.addTile("Ground", rw.Coordinate(0, 1), "Long Grass", rw.Coordinate(0, 0))

mygraph.addTile_square("Ground", rw.Rectangle(rw.Coordinate(5, 5), rw.Coordinate(10, 10)), "Deep Water", rw.Coordinate(0, 0))

mygraph.write_file(map_dir + map_name_out)

```



