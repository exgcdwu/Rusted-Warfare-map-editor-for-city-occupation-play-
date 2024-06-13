# Auto object adder tutotial

## Objective

该命令行工具旨在简化城夺地图的制作。对于需要在不同位置放置相同宾语，但仅仅一些细节不同的时候，可以使用该工具简化操作。

只需要按照命令行教程的格式在地图文件中添加额外的info宾语（需要填写大量参数）和标记宾语（仅有名称需要填写），标记宾语就会根据info宾语自动在原地生成想要的宾语。

具体来说，程序会识别标记宾语名称的前缀(prefix)，来找到指定的info宾语，并根据该info宾语的内容按照约定自动生成新的宾语。该约定变量由-v -i命令确定，无该命令是提供默认约定变量。

想要运行程序来进行自动转换，需要python编译器，下载指定库，并使用终端命令行操作您的地图文件，达到自动转换目的。

## RW map process

### city_info

自动建立城市需要事先提供格式。请在任意位置部署一个或多个名称前缀为city_info的宾语，类型不填。
如果有多个，请让它们的前缀(prefix)均不同，这样可以采用多种格式来部署城市（通过前缀区分）。

请在属性中添加以下参数，可选参数可以不用添加：

请注意，is前缀的需要改变其数据类型为bool（形式为 type="bool" value="true"）

prefix：表示城市前缀

idprefix: 表示所使用的id前缀，城市id在idprefix后将自动按照1,2...顺序延伸，请确保其他id没有此前缀

detectReset: 城市检测的resetActivationAfter

addWarmup：城市添加的warmup

addReset：城市添加的resetActivationAfter

unit：城市所用的建筑单位

isonlybuilding：可选，默认为否，是否启用onlybuilding来检测城市

isinadd：可选，默认为否，是否添加城市的初始刷新

isaddWarmup：可选，默认"0s"，当isinadd为是时，表示初始刷新的warmup

istext：可选，默认为否，是否有文本显示

textColor：可选，当istext为是时，表示城市文本的颜色

textSize：可选，当istext为是时，表示城市文本的字号

isprefixseg: 可选，默认为否，启用时，prefix与cityname之间需要'.'隔开。不要在不应该出现的地方出现'.'

isshowOnMap: 可选，默认为否，启用时，城市生成时小地图显示

isinshowOnMap: 可选，默认为否，启用时，当isinadd为是时，初始城市生成时小地图显示

mapTextName：可选，默认为"{cityname}"，即城市名，当istext为是时，文本显示宾语名字

unitAddName：可选，默认为""，建筑添加宾语名字

inunitAddName：可选，默认为"{team}"，即队伍，当isinadd为是时，建筑初始添加宾语名字

unitDetectName：可选，默认为"检测 {idprefix0}"，即检测id，建筑检测宾语名字

### city

在任意处添加宾语，然后名称格式为{prefix}{cityname}(,t{number})（实际没有大括号和小括号）。

为了地图编辑器观看效果，对宾语形状大小做稍许改动。

prefix为前缀，表明使用的格式

cityname为城市名称，该城市名称会出现在显示文本中

,t是可选项，当添加城市的初始刷新(isinadd=true)时，可以在最后加上,t，后面跟上队伍数字（以0开始，-1中立，-2敌对）

## python process

### start

下载任意一款python编译器。

### install

```console
pip install rwmapeditor-exgcdwu==1.5.5
```

### use

打开终端，输入如下指令：

```console
triggerauto {map_file}
```

该指令读入地图路径，将转换结果自动输到原路径

如果输出到不同路径，后面添加-o命令再加新路径（建议）

如果想要进行ID和id的重置，后面添加-r命令，不添加-r命令可以保证已有的ID和id不会改变

如果想要删除info和标记宾语，后面添加-d命令

如果想要自定义的约定，请使用-i -v 命令，-i命令约定了.py文件路径，-v命令约定了变量名，
随后程序会根据该变量来自动转换

[约定变量](https://github.com/exgcdwu/Rusted-Warfare-map-editor-for-city-occupation-play-/blob/main/auto/_data.py)
