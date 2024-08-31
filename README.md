# rwmapeditor-exgcdwu

___一个铁锈战争 (Rusted Warfare) 地图编辑 python 库___

![released version](https://img.shields.io/pypi/v/rwmapeditor-exgcdwu.svg)

## 目标

python实现铁锈地图文件地块编辑和宾语编辑。

重点减轻城市争夺地图的宾语编辑工作量。

基本框架已完成。

地块组框架已完成。

宾语组框架已完成。

宾语自动化命令行系统正在添加。

宾语自动化命令行系统app正在开发。

## 安装

```console
pip install rwmapeditor-exgcdwu
```

## 教程

[简易使用教程](https://github.com/exgcdwu/Rusted-Warfare-map-editor-for-city-occupation-play-/blob/main/Tutorial.md)

【python库的使用教程】

[城夺地图代码](https://github.com/exgcdwu/Rusted-Warfare-map-editor-for-city-occupation-play-/blob/main/examples/)

【正在开发的城夺地图和代码】

[宾语自动化命令行教程](https://github.com/exgcdwu/Rusted-Warfare-map-editor-for-city-occupation-play-/blob/main/auto/auto_tutorial.md)

【一个结合Tiled或者notTiled共同使用的宾语生成器，使用命令行操作，基于该库开发】

[宾语自动化app](https://github.com/Delta-Water/RustedWarfare-Development-Tools)

【宾语自动化命令行可能进行图形化，敬请期待。感谢print("")的帮助。】

## 其他

### 外部文件

本库使用了铁锈战争的默认地块集，存放在rwmap/other_data/maps/

文件中存在一些地块集模版，存放在rwmap/examples/template/，包括
notTiled的v3模板，城夺地块集模板（来自Xs）

使用kivy库生成app时使用了支持中文的字体库，存放在auto/_app/。[字体链接](https://www.fonts.net.cn/font-35156113491.html)
