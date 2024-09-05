<style>
    h2,h3{
        page-break-before:always;
    }
</style>

# 宾语自动化简易急速教程

- [宾语自动化简易急速教程](#宾语自动化简易急速教程)
  - [目标](#目标)
  - [下载与初始化（手机）](#下载与初始化手机)
  - [开始使用](#开始使用)
  - [info宾语和标志宾语简单介绍](#info宾语和标志宾语简单介绍)
  - [例子](#例子)
    - [产生建筑(版本 \>= 1.6.4)](#产生建筑版本--164)
      - [info宾语-建筑](#info宾语-建筑)
      - [标志宾语-建筑](#标志宾语-建筑)
    - [产生城市(版本 \>= 1.6.4)](#产生城市版本--164)
      - [info宾语-城市](#info宾语-城市)
      - [标志宾语-城市](#标志宾语-城市)
    - [队伍检测（检测内容相同，但检测队伍不同）(版本\>=1.6.4)](#队伍检测检测内容相同但检测队伍不同版本164)
      - [info宾语-队伍检测](#info宾语-队伍检测)
      - [标志宾语-队伍检测](#标志宾语-队伍检测)
      - [引用的说明-队伍检测](#引用的说明-队伍检测)
    - [城市+队伍检测（版本\>=1.6.4）](#城市队伍检测版本164)
      - [info宾语-城市+队伍检测](#info宾语-城市队伍检测)
      - [标志宾语-城市+队伍检测](#标志宾语-城市队伍检测)
      - [引用的说明-城市+队伍检测](#引用的说明-城市队伍检测)
    - [城市+队伍检测+城市文本颜色变化（版本\>=1.6.4）](#城市队伍检测城市文本颜色变化版本164)
      - [info宾语-城市+队伍检测+城市文本颜色变化](#info宾语-城市队伍检测城市文本颜色变化)
      - [标志宾语-城市+队伍检测+城市文本颜色变化](#标志宾语-城市队伍检测城市文本颜色变化)
      - [引用的说明-城市+队伍检测+城市文本颜色变化](#引用的说明-城市队伍检测城市文本颜色变化)
    - [城市+本地额外塔防（版本\>=1.6.4）](#城市本地额外塔防版本164)
      - [标志宾语-城市+本地额外塔防](#标志宾语-城市本地额外塔防)
      - [引用的说明-城市+本地额外塔防](#引用的说明-城市本地额外塔防)
    - [占领区刷兵(版本\>=1.6.4)](#占领区刷兵版本164)
      - [info宾语-占领区刷兵](#info宾语-占领区刷兵)
      - [标志宾语-占领区刷兵](#标志宾语-占领区刷兵)
      - [引用的说明-占领区刷兵](#引用的说明-占领区刷兵)
      - [如果引用的不是teamDetect\_info，而是内部有teamDetect\_info的tree\_info?](#如果引用的不是teamdetect_info而是内部有teamdetect_info的tree_info)
      - [如果换成普通刷兵？](#如果换成普通刷兵)
  - [注意事项](#注意事项)
    - [引用(cite\_name)要求](#引用cite_name要求)
    - [键值触碰关键词](#键值触碰关键词)

## 目标

宾语自动化的急速入门。

## 下载与初始化（手机）

下载群文件中的 termux 并安装。打开后可以看到一个黑色的命令行界面，之后需要在这个界面操作。

termux python环境及包下载（需要一段时间，保持网络畅通）（中间出现的提问选项，全部输入y再回车）：
*感谢kend在使用termux安装python包方面的帮助*

    pkg update -y
    pkg install -y python
    pkg install -y python-numpy
    pkg install -y python-pillow
    pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple #（如果清华镜像不可以，换成别的镜像比如https://pypi.mirrors.ustc.edu.cn/simple也行）
    pip install asteval
    pip install regex # 1.6.3新加入
    pip install rwmapeditor-exgcdwu==1.6.4 --no-deps

需要获取读取存储权限：

    termux-setup-storage

之后就可以使用termux使用triggerauto处理地图文件了。

如果想要更改版本，使用如下命令行。

    pip uninstall -y rwmapeditor-exgcdwu
    pip install rwmapeditor-exgcdwu==1.6.1 --no-deps #（新版本，大于等于1.6.1）

## 开始使用

打开termux，输入如下指令：

    triggerauto {输入地图路径} -o {输出地图路径}

该指令读入地图路径，将转换结果自动输出。如何查找地图的路径呢？可以使用mt浏览器查找地图路径复制并粘贴。长按并点击paste即可粘贴。更多参数见[宾语自动化命令行教程](https://github.com/exgcdwu/Rusted-Warfare-map-editor-for-city-occupation-play-/blob/main/auto/auto_tutorial.md)。

## info宾语和标志宾语简单介绍

进行自动化，至少需要两种宾语。一种是info宾语，可以为自动化提供信息。一种是标志宾语，可以为自动化提供位置和更具体的信息。之后只需运行命令行即可。

info宾语和标志宾语的类型都必须是空的。info宾语名字形如xxx_info，有不同info宾语可供选择。info宾语可以添加大量属性。标志宾语只用写名字即可。

接下来将会给出常见自动化的info例子和标志宾语例子。如果想要更灵活的处理，请参见[宾语自动化命令行教程](https://github.com/exgcdwu/Rusted-Warfare-map-editor-for-city-occupation-play-/blob/main/auto/auto_tutorial.md)。

## 例子

### 产生建筑(版本 >= 1.6.4)

产生一个自动刷新建筑。

#### info宾语-建筑

名称："building_info"，类型不填。

属性：

prefix："b" //标志宾语使用前缀

idprefix："city" //检测的id前缀

detectReset："20s" //建筑检测的resetActivationAfter

addWarmup："20s" //建筑添加的warmup（也是初始建筑添加）

addReset："20s" //建筑添加的resetActivationAfter

unit："turret" //单位类型

isonlybuilding："true" //使用onlyBuildings检测，而不使用unitType检测。

isinadd："true" //允许初始建筑添加

args："inaddteam,str" //参数导入

#### 标志宾语-建筑

名称："b{队伍}"，类型不填。

属性不填。

### 产生城市(版本 >= 1.6.4)

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

isinadd："true" //允许初始建筑添加

args："inaddteam,str;bdtext,str" //参数导入

#### 标志宾语-城市

名称："c{队伍}.{城市名}"，类型不填。

属性不填。

### 队伍检测（检测内容相同，但检测队伍不同）(版本>=1.6.4)

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

### 城市+队伍检测（版本>=1.6.4）

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

isinadd："true" //允许初始建筑添加

args："inaddteam,str;bdtext,str" //参数导入

// 一个常规城市标志宾语

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

// 一个队伍检测宾语

第三个info宾语。

名称："tree_info"，类型不填。

属性：

prefix："ctd" //标志宾语使用前缀

idprefix："mtd,1" //申请id做cite_name

name："c{inaddteam}.{cityname};td.{idprefix0_0}" //产生分支标志宾语的格式

a："{idprefix0_0}.a" // 简化引用

b："{idprefix0_0}.b" // 简化引用

brace："a,b" //最终翻译

args："inaddteam,str;cite_name,str;cityname,str" //参数导入

// 通过tree将二者组合

#### 标志宾语-城市+队伍检测

名称："ctd{队伍}.{引用名字}.{城市名}"。类型不填。
属性不填。

#### 引用的说明-城市+队伍检测

假如有一标志宾语为"ctd3.ctd1.斯大林格勒"。在其他宾语中出现"ctd_t1.a"或者"ctd_t1.b"会得到队伍检测的id。如果希望非自动化的宾语也执行这一功能，添加-c选项。

### 城市+队伍检测+城市文本颜色变化（版本>=1.6.4）

#### info宾语-城市+队伍检测+城市文本颜色变化

第一个info宾语。

名称："building_info"，类型不填。

属性：

prefix："c" //标志宾语使用前缀

idprefix："city" //检测的id前缀

detectReset："20s" //建筑检测的resetActivationAfter

addWarmup："20s" //建筑添加的warmup

addReset："20s" //建筑添加的resetActivationAfter

unit："supplyDepot" //单位类型

isinadd："true" //允许初始建筑添加

args："inaddteam,str" //参数导入

// 一个常规城市标志宾语

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

// 一个队伍检测宾语

第三个info宾语。

名称："multiText_info"，类型不填。

属性：

prefix："mt" //标志宾语使用前缀

color："red,blue,white" //文本颜色

isdefaultText："true" //使用teamDetect时的可选项。

text："{btext},{{xtext}},{{rtext}}"

textsize："{mytextsize}"

args："teamDetect_cite,str;btext,str" //参数导入

opargs："t,mytextsize,str,7;x,xtext,str,{btext};r,rtext,str,{btext}" //文本大小，第二个文本

isprefixseg："true" //前缀与必填参数之间需要"."

// 多个文本宾语

第四个info宾语。

名称："tree_info"，类型不填。

属性：

prefix："ctd_t" //标志宾语使用前缀

idprefix："mtd,1" //申请id做cite_name

name："c{inaddteam};td.{idprefix0_0};mt.{idprefix0_0}.{cityname},t{textsize},x{xtext},r{rtext}" //产生分支标志宾语的格式

a："{idprefix0_0}.a" // 简化引用

b："{idprefix0_0}.b" // 简化引用

brace："a,b" //最终翻译

args："inaddteam,str;cite_name,str;cityname,str" //参数导入

opargs："t,textsize,str,7;x,xtext,str,{cityname};r,rtext,str,{cityname}" //文本大小，第二个文本变化（如果有）

// 将其组合

#### 标志宾语-城市+队伍检测+城市文本颜色变化

名称："ctd_t{队伍}.{引用名字}.{城市名},t{文本大小，默认为7},x{B队文本，默认城市名},r{默认文本，默认城市名}"。","为可选项，可以不填。类型不填。
属性不填。

#### 引用的说明-城市+队伍检测+城市文本颜色变化

假如有一标志宾语为"ctd_t3.ctd_t1.红斯大林格勒,t10,x蓝斯大林格勒,r白斯大林格勒"。在其他宾语中出现"ctd_t1.a"或者"ctd_t1.b"会得到队伍检测的id。如果希望非自动化的宾语也执行这一功能，添加-c选项。

### 城市+本地额外塔防（版本>=1.6.4）

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

isinadd："true" //允许初始建筑添加

args："inaddteam,str;bdtext,str" //参数导入

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

名称："building_f_info"，类型不填。

属性：

prefix："bbt" //标志宾语使用前缀

idprefix："bbt" //检测的id前缀

detectReset："3s" //建筑检测的resetActivationAfter

addWarmup："3s" //建筑添加的warmup

unit："bugTurret" //单位类型

isinadd："true"  //允许初始建筑添加

deacti："fd1.idprefix0,{{td_cite}.{teamtoid_dep}\['inaddteam'\]}" //闪烁器引用，队伍检测引用

args："inaddteam,str;td_cite,str" //参数导入

前三个info宾语是城市+队伍检测+城防的模板。

第四个info宾语。

名称："tree_info"，类型不填。

属性：

prefix："cbtd" //标志宾语使用前缀

idprefix："mtd,1" //申请id做cite_name

name："c{inaddteam}.{cityname};td.{idprefix0_0};bbt{inaddteam}.{idprefix0_0}" //产生分支标志宾语的格式

a："{idprefix0_0}.a" // 简化引用

b："{idprefix0_0}.b" // 简化引用

brace："a,b" //最终翻译

offset："0 0,0 0,-1 -1"

args："inaddteam,str;cite_name,str;cityname,str" //参数导入

此外，需要部署振荡器来帮助城防刷新。

振荡器info。

第五个info宾语。

名称："flash_info"，类型不填。

属性：

prefix："fd" //标志宾语使用前缀

idprefix："fd" //申请id

initialtime："20s" //初始刷新

periodtime： "3s" //刷新周期

args："cite_name,str" //参数导入

isprefixseg："true" //前缀与必填参数之间需要"."

部署振荡器，这样城防建筑可以使用。

名称："fd.fd1"，类型不填。

#### 标志宾语-城市+本地额外塔防

名称："cbtd{队伍}.{引用名字}.{城市名}"，类型不填。

属性不填。

#### 引用的说明-城市+本地额外塔防

假如有一标志宾语为"cbtd3.cbtd1.斯大林格勒"。在其他宾语中出现"cbtd1.a"或者"cbtd1.b"会得到队伍检测的id。如果希望非自动化的宾语也执行这一功能，添加-c选项。

### 占领区刷兵(版本>=1.6.4)

产生刷兵宾语。

#### info宾语-占领区刷兵

名称："dictionary_info"，类型不填。

属性：

prefix："d"

me："mechGun*1"

he："heavyTank*1"...

任意可以简化单位的写法。

名称："d.d"，类型属性不填。

如此，在其他位置输入"dd.me"将会自动认为是"mechGun*1"...

名称：object_info，类型不填。

属性：

prefix："oa" //标志宾语使用前缀

type："unitAdd" //类型

warmup："1s" //防止振动器初始刷新

deactivatedBy："fd1.idprefix0,{{td_cite}.{teamtoid_dep}\['td_team'\]}" //闪烁器引用，队伍检测引用

team："-1" //队伍，也可为"{td_team}"

spawnUnits："d.{dc_unit}"

args："dc_unit,str;td_cite,str;td_team,str" //参数导入

isprefixseg："true" //前缀与必填参数之间需要"."

需要有引用名为fd1的振荡器。需要一个teamDetect引用作为约束。

#### 标志宾语-占领区刷兵

名称："oa.{刷新单位}.{teamDetect引用}.{队伍}"，类型不填。
属性不填。

#### 引用的说明-占领区刷兵

假如有一标志宾语为"oa.me.td1.0"。那么仅在td1检测阵营为与0相同时刷新，刷新频率跟随fd1振荡器。刷新单位为"mechGun*1"

#### 如果引用的不是teamDetect_info，而是内部有teamDetect_info的tree_info?

注意使用brace，然后外部调用哦。

#### 如果换成普通刷兵？

需要对前面的占领刷兵info进行一定的修改。删除其中一部分参数。

## 注意事项

### 引用(cite_name)要求

允许中英文和数字，不允许其他符号

### 键值触碰关键词

不可控，一般不会碰到，一般换一个就没问题。
