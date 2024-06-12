# Auto object adder tutotial

## RW map process

### city_info

自动建立城市需要事先提供格式。请在任意位置部署一个或多个名称为city_info的宾语，类型不填。
如果有多个，请让它们的前缀(prefix)均不同，这样可以采用多种格式来部署城市（通过前缀区分）。

请在属性中添加以下所有参数：

请注意，is前缀的需要改变其数据类型为bool

prefix：表示城市前缀

idprefix: 表示所使用的id前缀，城市id在idprefix后将自动按照1,2...顺序延伸，请确保其他id没有此前缀

detectReset: 城市检测的resetActivationAfter

addWarmup：城市添加的warmup

addReset：城市添加的resetActivationAfter

unit：城市所用的建筑单位

isonlybuilding：可选，是否启用onlybuilding来检测城市(而不是检测unit)，默认为否（即使用unit检测）

isinadd：可选，是否添加城市的初始刷新，默认为否

isaddWarmup：可选，当isinadd为是时，表示初始刷新的warmup

istext：可选，是否有文本显示，默认为否

textColor：可选，当istext为是时，表示城市文本的颜色

textSize：可选，当istext为是时，表示城市文本的字号

### city

在任意处添加宾语，然后名称格式为{prefix}.{cityname}(,t{number})（实际没有大括号和小括号）

prefix为前缀，表明使用的格式

cityname为城市名称，该城市名称会出现在显示文本中

,t是可选项，当添加城市的初始刷新(isinadd=true)时，可以在最后加上,t，后面跟上队伍数字（以0开始

## python process

### start

下载任意一款python编译器

### install

```console
pip install rwmapeditor-exgcdwu==1.5.0
```

### use

打开终端，输入如下指令：

```console
triggerauto {map_file}
```

该指令读入地图路径，将转换结果自动输到原路径

如果输出到不同路径，后面添加-o命令（建议）
