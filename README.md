# rwmapeditor-exgcdwu

___一个铁锈战争 (Rusted Warfare) 地图编辑 python 库___

![released version](https://img.shields.io/pypi/v/rwmapeditor-exgcdwu.svg)

[简易使用教程](https://github.com/exgcdwu/Rusted-Warfare-map-editor-for-city-occupation-play-/blob/main/Tutorial.md)

【教程已过时】

[城夺宾语自动化命令行教程](https://github.com/exgcdwu/Rusted-Warfare-map-editor-for-city-occupation-play-/blob/main/auto/auto_tutotial.md)

[简单城夺地图代码例子](https://github.com/exgcdwu/Rusted-Warfare-map-editor-for-city-occupation-play-/blob/main/examples/example1/example1.py)

## 目标

python实现铁锈地图文件地块编辑和宾语编辑。

暂时不打算接触地块集。

重点减轻城市争夺地图的宾语编辑工作量

基本框架已完成。

地块组框架已完成。

宾语组框架已完成。

## 安装

```console
pip install rwmapeditor-exgcdwu
```

## 使用之前

### 1.使用地图编辑器(Tiled,notTiled)创建新地图

地图格式：zlib、gzip、纯base64

渲染顺序：右下(right-down)

方向：orthogonal

#### 2.手动载入地块集

#### 3.手动创建所需的地块层和宾语层

#### 4.即可使用python库改变地块和宾语

## 其他

### 外部文件

本库使用了铁锈战争的默认地块集，存放在rwmap/other_data/maps/

文件中存在一些地块集模版，存放在rwmap/examples/template/，包括
notTiled的v3模板，城夺地块集模板（来自Xs）
