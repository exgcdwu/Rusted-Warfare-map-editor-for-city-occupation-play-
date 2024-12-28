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

### 电脑

建议安装vscode，请自行搜索如何在vscode上使用python并下载python包。然后使用

    pip install rwmapeditor-exgcdwu

来安装包，开始使用。

### 手机termux

还可以使用Termux来在手机上操作python和命令行。

[github Termux](https://github.com/termux/termux-app)

termux python环境及包下载（需要一段时间，保持网络畅通）（中间出现的提问选项，全部输入y再回车）：

`感谢kend在使用termux安装python包方面的帮助`

`每一条均需要顺序执行，开头不得出现空格。请尽量复制粘贴后执行。`

    pkg update -y
    pkg install -y python
    pkg install -y python-numpy
    pkg install -y python-pillow
    pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple #（如果清华镜像不可以，换成别的镜像比如https://pypi.mirrors.ustc.edu.cn/simple 也行）
    pip install asteval
    pip install regex # 1.6.3新加入
    pip install pybind11 # 1.8.0新加入
    pip install imageio # 1.8.0新加入
    pip install sortedcontainers # 1.8.0新加入

    pip install rwmapeditor-exgcdwu==1.8.0 --no-deps
    termux-setup-storage

然后点同意获取读取存储权限

之后就可以使用termux使用objectgroupauto处理地图文件了。

如果想要更改版本，使用如下命令行。

    pip uninstall -y rwmapeditor-exgcdwu
    pip install rwmapeditor-exgcdwu==1.6.1 --no-deps #（新版本，大于等于1.6.1）

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
