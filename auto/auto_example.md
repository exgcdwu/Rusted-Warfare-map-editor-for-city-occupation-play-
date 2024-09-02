# 宾语自动添加的例子

- [宾语自动添加的例子](#宾语自动添加的例子)
  - [目标](#目标)
  - [下载与初始化](#下载与初始化)
  - [开始使用](#开始使用)
  - [info宾语和标志宾语简单介绍](#info宾语和标志宾语简单介绍)
  - [例子](#例子)
    - [产生建筑(版本 \>= 1.6.1)](#产生建筑版本--161)
      - [info宾语-建筑](#info宾语-建筑)
      - [标志宾语-建筑](#标志宾语-建筑)
    - [产生城市(版本 \>= 1.6.1)](#产生城市版本--161)
      - [info宾语-城市](#info宾语-城市)
      - [标志宾语-城市](#标志宾语-城市)
    - [队伍检测（检测内容相同，但检测队伍不同）(版本\>=1.6.3)](#队伍检测检测内容相同但检测队伍不同版本163)
      - [info宾语-队伍检测](#info宾语-队伍检测)
      - [标志宾语-队伍检测](#标志宾语-队伍检测)
      - [引用的说明-队伍检测](#引用的说明-队伍检测)
    - [城市+队伍检测（版本\>=1.6.3）](#城市队伍检测版本163)
      - [info宾语-城市+队伍检测](#info宾语-城市队伍检测)
      - [标志宾语-城市+队伍检测](#标志宾语-城市队伍检测)
      - [引用的说明-城市+队伍检测](#引用的说明-城市队伍检测)

## 目标

宾语自动化的急速入门。

## 下载与初始化

下载群文件中的termux app并安装。可以看到一个黑色的窗口，可以输入指令。接下来要进行初始化，才能使用triggerauto命令。

termux python环境及包下载（需要一段时间，保持网络畅通）（中间出现的提问选项，全部输入y再回车）：
*感谢kend在使用termux安装python包方面的帮助*

    pkg update -y
    pkg install -y python
    pkg install -y python-numpy
    pkg install -y python-pillow
    pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple #（如果清华镜像不可以，换成别的镜像比如https://pypi.mirrors.ustc.edu.cn/simple也行）
    pip install asteval
    pip install rwmapeditor-exgcdwu==1.6.1 --no-deps

需要获取读取存储权限：

    termux-setup-storage

之后就可以使用termux使用triggerauto处理地图文件了。

如果想要更改版本，使用如下命令行。

    pip uninstall -y rwmapeditor-exgcdwu
    pip install rwmapeditor-exgcdwu==1.6.1 --no-deps #（新版本，大于等于1.6.1）

## 开始使用

打开终端，输入如下指令：

    triggerauto {输入地图路径} -o {输出地图路径}

该指令读入地图路径，将转换结果自动输出。如何查找地图的路径呢？可以使用mt浏览器查找地图路径复制并粘贴。长按并点击paste即可粘贴。更多参数见[宾语自动化命令行教程](https://github.com/exgcdwu/Rusted-Warfare-map-editor-for-city-occupation-play-/blob/main/auto/auto_tutorial.md)。

## info宾语和标志宾语简单介绍

进行自动化，至少需要两种宾语。一种是info宾语，可以为自动化提供信息。一种是标志宾语，可以为自动化提供位置和更具体的信息。之后只需运行命令行即可。

info宾语和标志宾语的类型都必须是空的。info宾语名字形如xxx_info，有不同info宾语可供选择。info宾语可以添加大量属性。标志宾语只用写名字即可。

接下来将会给出常见自动化的info例子和标志宾语例子。如果想要更灵活的处理，请参见[宾语自动化命令行教程](https://github.com/exgcdwu/Rusted-Warfare-map-editor-for-city-occupation-play-/blob/main/auto/auto_tutorial.md)。

## 例子

### 产生建筑(版本 >= 1.6.1)

产生一个自动刷新建筑。

#### info宾语-建筑

名称："building_info"，类型不填。
属性：
prefix："b" //标志宾语使用前缀
idprefix："city" //检测的id前缀
detectReset："20s" //建筑检测的resetActivationAfter
addWarmup："20s" //建筑添加的warmup
addReset："20s" //建筑添加的resetActivationAfter
unit："turret" //单位类型
isonlybuilding："true" //使用onlyBuildings检测，而不使用unitType检测。

#### 标志宾语-建筑

名称："b"，类型不填。
属性不填。

### 产生城市(版本 >= 1.6.1)

产生一个自动刷新建筑。上面有名字。

#### info宾语-城市

名称："building_info"，类型不填。
属性：
prefix："c" //标志宾语使用前缀
idprefix："city" //检测的id前缀
detectReset："20s" //建筑检测的resetActivationAfter
addWarmup："20s" //建筑添加的warmup
addReset："20s" //建筑添加的resetActivationAfter
unit："supplyDepot" //单位类型
isbdtext："true" //启用文本
bdcolor："white" //城市文本颜色
bdtextsize："7" //城市文本大小
args："bdtext,str" //参数导入
isprefixseg："true" //前缀与必填参数之间需要"."

#### 标志宾语-城市

名称："c.{城市名}"，类型不填。
属性不填。

### 队伍检测（检测内容相同，但检测队伍不同）(版本>=1.6.3)

产生若干队伍检测宾语。

#### info宾语-队伍检测

名称：teamDetect_info，类型不填。
属性：
prefix："td" //标志宾语使用前缀
unit："supplyDepot" //检测类型（或者使用onlyBuildings："true" //检测建筑）
reset："10s" //检测的resetActivationAfter
setidTeam："A_city,B_city" //（检测前缀，巴巴罗萨举例）
setTeam："0 2 4 6 8 10 12 14 16 18,1 3 5 7 9 11 13 15 17" //（队伍从0开始，巴巴罗萨举例）
a："{setidTeam0_0}" // 简化引用
b："{setidTeam1_0}" // 简化引用
brace："a,b" //最终翻译
args："cite_name,str" //参数导入
isprefixseg："true" //前缀与必填参数之间需要"."

#### 标志宾语-队伍检测

名称："td.{外部引用名}"，类型不填。
属性不填。

#### 引用的说明-队伍检测

假如有一标志宾语为"td.td1"。在其他宾语中出现"td1.a"或者"td1.b"会得到队伍检测的id。如果希望非自动化的宾语也执行这一功能，添加-c选项。

### 城市+队伍检测（版本>=1.6.3）

#### info宾语-城市+队伍检测

第一个info宾语。
名称："building_info"，类型不填。
属性：
prefix："c" //标志宾语使用前缀
idprefix："city" //检测的id前缀
detectReset："20s" //建筑检测的resetActivationAfter
addWarmup："20s" //建筑添加的warmup
addReset："20s" //建筑添加的resetActivationAfter
unit："supplyDepot" //单位类型
isbdtext："true" //启用文本
bdcolor："white" //城市文本颜色
bdtextsize："7" //城市文本大小
args："bdtext,str" //参数导入
isprefixseg："true" //前缀与必填参数之间需要"."

第二个info宾语。
名称："teamDetect_info"，类型不填。
属性：
prefix："td" //标志宾语使用前缀
unit："supplyDepot" //检测类型（或者使用onlyBuildings："true" //检测建筑）
reset："10s" //检测的resetActivationAfter
setidTeam："A_city,B_city" //（检测前缀，巴巴罗萨举例）
setTeam："0 2 4 6 8 10 12 14 16 18,1 3 5 7 9 11 13 15 17" //（队伍从0开始，巴巴罗萨举例）
a："{setidTeam0_0}" // 简化引用
b："{setidTeam1_0}" // 简化引用
brace："a,b" //最终翻译
args："cite_name,str" //参数导入
isprefixseg："true" //前缀与必填参数之间需要"."

第三个info宾语。
名称："tree_info"，类型不填。
属性：
prefix："tc" //标志宾语使用前缀
idprefix："mtd,1" //申请id做cite_name
name："c.{cityname};td.{idprefix0_0}" //产生分支标志宾语的格式
a："{idprefix0_0}.a" // 简化引用
b："{idprefix0_0}.b" // 简化引用
brace："a,b" //最终翻译
args："cite_name,str;cityname,str" //参数导入
isprefixseg："true" //前缀与必填参数之间需要"."

#### 标志宾语-城市+队伍检测

名称："tc.{引用名字}.{城市名}"，类型不填。
属性不填。

#### 引用的说明-城市+队伍检测

假如有一标志宾语为"tc.tc1.莫斯科"。在其他宾语中出现"tc1.a"或者"tc1.b"会得到队伍检测的id。如果希望非自动化的宾语也执行这一功能，添加-c选项。
