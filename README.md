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

许多其他命令均在command/文件夹。

宾语自动化命令行系统app正在开发。

## 安装

提供三种安装方法(pip, 下载下来安装, 手机Termux)，[安装教程](https://github.com/exgcdwu/Rusted-Warfare-map-editor-for-city-occupation-play-/blob/main/INSTALL.md)

## 教程

[简易使用教程](https://github.com/exgcdwu/Rusted-Warfare-map-editor-for-city-occupation-play-/blob/main/Tutorial.md)

【python库的使用教程】

[城夺地图代码](https://github.com/exgcdwu/Rusted-Warfare-map-editor-for-city-occupation-play-/blob/main/examples/)

【正在开发的城夺地图和代码】

[地块集和图片嵌入](https://github.com/exgcdwu/Rusted-Warfare-map-editor-for-city-occupation-play-/blob/main/command/tsindep/)

【将地块集和图片嵌入地图，解决Tiled不能嵌入图片的问题。】

[地块集自动化](https://github.com/exgcdwu/Rusted-Warfare-map-editor-for-city-occupation-play-/blob/main/command/tilesetauto/)

【自动生成地块集】

[地块自动化](https://github.com/exgcdwu/Rusted-Warfare-map-editor-for-city-occupation-play-/blob/main/command/layerauto/)

【地块映射】

[地块自动添加障碍](https://github.com/exgcdwu/Rusted-Warfare-map-editor-for-city-occupation-play-/blob/main/command/layerobauto/)

【自动添加周期地块】

[地图放大](https://github.com/exgcdwu/Rusted-Warfare-map-editor-for-city-occupation-play-/blob/main/command/resizeauto/)

【地图放大】

[图块自动化](https://github.com/exgcdwu/Rusted-Warfare-map-editor-for-city-occupation-play-/blob/main/command/layerauto/)

【按照一定的规则部署地块】

[宾语自动化引导教程](https://github.com/exgcdwu/Rusted-Warfare-map-editor-for-city-occupation-play-/blob/main/command/objectgroupauto/readme/auto_guide.md)

[宾语自动化地图示例](https://github.com/exgcdwu/Rusted-Warfare-map-editor-for-city-occupation-play-/blob/main/command/objectgroupauto/example/auto_example.tmx)

[宾语自动化地图示例自动化结果](https://github.com/exgcdwu/Rusted-Warfare-map-editor-for-city-occupation-play-/blob/main/command/objectgroupauto/example/auto_example_answer.tmx)

[宾语自动化参数说明](https://github.com/exgcdwu/Rusted-Warfare-map-editor-for-city-occupation-play-/blob/main/command/objectgroupauto/readme/auto_tutorial.md)

【一个结合Tiled或者notTiled共同使用的宾语生成器，使用命令行操作，基于该库开发】

[宾语自动化app](https://github.com/Delta-Water/RustedWarfare-Development-Tools)

【宾语自动化命令行已经可以图形化。感谢print("")的帮助。】

[ID重排](https://github.com/exgcdwu/Rusted-Warfare-map-editor-for-city-occupation-play-/blob/main/command/idrearrange/)

【宾语ID重排，可以兼容自动化（或者说，宾语自动化开始就会检测，然后试图ID重排）】

## 其他

### 外部文件

本库使用了铁锈战争的默认地块集，存放在rwmap/other_data/maps/

文件中存在一些地块集模版，存放在rwmap/examples/template/，包括
notTiled的v3模板，来自Xs的若干城夺地块集。文件中的地图文件可能包括这些地块集。

使用kivy库生成app时使用了支持中文的字体库，存放在command/auto/_app/。[字体链接](https://www.fonts.net.cn/font-35156113491.html)
