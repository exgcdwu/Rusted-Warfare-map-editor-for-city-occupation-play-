# 宾语自动添加教程

- [宾语自动添加教程](#宾语自动添加教程)
  - [目标](#目标)
  - [info宾语介绍](#info宾语介绍)
    - [info宾语中基本参数介绍](#info宾语中基本参数介绍)
    - [info宾语的其他说明](#info宾语的其他说明)
    - [info中的参数类型](#info中的参数类型)
  - [inadd\_info](#inadd_info)
    - [inadd\_info可选参数](#inadd_info可选参数)
  - [bdtext\_info](#bdtext_info)
    - [bdtext\_info必选参数](#bdtext_info必选参数)
    - [bdtext\_info可选参数](#bdtext_info可选参数)
  - [building\_info](#building_info)
    - [building\_info必填参数](#building_info必填参数)
    - [building\_info可选参数](#building_info可选参数)
  - [teamDetect\_info](#teamdetect_info)
    - [teamDetect必选参数](#teamdetect必选参数)
    - [teamDetect可选参数](#teamdetect可选参数)
  - [numDetect\_info](#numdetect_info)
    - [numDetect必选参数](#numdetect必选参数)
    - [numDetect可选参数](#numdetect可选参数)
  - [multiText\_info](#multitext_info)
    - [multiText必选参数](#multitext必选参数)
    - [multiText可选参数](#multitext可选参数)
  - [python使用](#python使用)
    - [开始](#开始)
    - [安装](#安装)
    - [使用](#使用)
    - [命令参数](#命令参数)
    - [其他特性](#其他特性)
    - [注意事项](#注意事项)
      - [team设置](#team设置)

## 目标

该命令行工具旨在简化城夺地图的制作。对于需要在不同位置放置相同宾语，但仅仅一些细节不同的时候，可以使用该工具简化操作。

只需要按照命令行教程的格式在地图文件中添加额外的info宾语（需要填写大量参数）和标记宾语（仅有名称需要填写,类型不需要填写），标记宾语就会根据info宾语自动生成想要的宾语。

具体来说，程序会识别标记宾语名称的前缀(prefix)，来找到指定的info宾语，并根据该info宾语的内容按照约定导入相关属性。相关属性可指定标记宾语的必填参数和可选参数，标记宾语可以依照info宾语的格式填写参数。

想要运行程序来进行自动转换，需要python编译器，下载指定库，并使用终端命令行操作您的地图文件，达到自动转换目的。

还可以使用Termux来在手机上操作python和命令行。
[github Termux](https://github.com/termux/termux-app)
[Termux下载](https://github.com/termux/termux-packages/releases/download/bootstrap-2024.08.18-r1%2Bapt-android-7/bootstrap-arm.zip)

## info宾语介绍

info宾语是执行一切自动转换的基础，地图作者需要将生成的不同组宾语中相同的参数放入info宾语，并将不同的参数设置为在标记宾语中才会填写的参数。

info宾语的名字必须以xxx_info开头，后面可以跟任意字符。后方可以存在",d"，表明添加了删除标记，该info宾语将不能参与宾语生成。

### info宾语中基本参数介绍

prefix: 填写标记宾语的前缀（或者其他info宾语的引用），在标记宾语名称开头加入prefix即证明该标记宾语使用该info宾语的格式。

isprefixseg：标记宾语中，前缀之后加入必填参数时，是否跟一个"."。

args: 声明标记宾语的必填参数。比如"unit,str;num,str"，这一串表明标记宾语必须填入2个参数，第一个是代入unit，第二个代入num。参数名后面目前只支持str格式。标记宾语在前缀之后添加supplyDepot.1意思是unit为supplyDepot，num为1。如果info宾语的prefix为e，那么标记宾语将填esupplyDepot.1。如果isprefixseg标记了，那么标记宾语将填e.supplyDepot.1。

opargs: 声明标记宾语的选填参数。比如"u,unit,str,supplyDepot;n,num,str,2"，这一串表明unit和num是可以选填的（第一个参数必须只有一个字母）。想填写unit为supplyDepot时需要输入",usupplyDepot"。想填写num为1时需要输入",n1"。注意，即使没有填写num，num默认为2。
*,d是默认存在的选项，加入即证明该标记宾语被打上了删除标记*

cite_name：标记宾语的引用，如果没有，无法被引用。比如在某info宾语中设置args为"cite_name,str"，在使用该info宾语格式的标记宾语中名称为"e.td"，其中e是前缀。在cite_name后面加"."再添加属性名称，即可实现引用。比如td.unit表明将会引用该标记宾语的其中unit的内容。
*不得出现循环引用，文件中靠前的宾语不得引用靠后的宾语。*

### info宾语的其他说明

无参数表明将不支持args和opargs。附属info宾语表示该info宾语不能独立指定相关标记宾语，只能被其他info宾语引用自己的prefix导入参数。

### info中的参数类型

请注意，is前缀的需要改变其数据类型为bool（文本文件中的形式为 type="bool" value="true" 或者 value="true"）。

存在一些需要输入多个数据的属性，这些属性格式总结如下：

字符串数组：字符串之间用','隔开

数字数组：数字之间用' '隔开

字符串二维数组：第一维用";"隔开，第二维用","隔开

数字二维数组：第一维用","隔开，第二维用" "隔开

info宾语内的属性也可以互相引用。假如info宾语内有一个属性为unit:supplyDepot。那么，设置另一个属性为inaddunit:{unit}即可实现引用（引用自己标记宾语的属性）。

## inadd_info

初始单位添加宾语，是附属宾语，且无参数。

### inadd_info可选参数

prefix：其他info宾语引用标记。（[info宾语默认参数](#info宾语中基本参数介绍)）

isinadd：可选，默认为是，在building_info中默认为否，是否添加城市的初始刷新。

inaddunit：当isinadd为是时必选，表示单位添加的类型。

inaddspawnnum：当isinadd为是时必选，表示单位添加的数量。

inaddteam：当isinadd为是时必选，表示单位添加的队伍。

inaddwarmup：当isinadd为是时必选，表示单位添加的warmup。

inaddisshowOnMap: 当isinadd为是时可选，默认为否，启用时，初始城市生成时小地图显示。

inaddname：当isinadd为是时可选，默认为""，建筑初始添加宾语名字。

inaddoffset: 当isinadd为是时可选，数字数组，默认为"0 0"，建筑初始添加宾语偏移。

inaddoffsetsize: 当isinadd为是时可选，数字数组，默认为"0 0"，建筑初始添加宾语大小改变。

## bdtext_info

建筑文本显示，是附属宾语，且无参数。

### bdtext_info必选参数

isbdtext：可选，默认为是，在building_info中默认为否，是否启用该宾语。

bdtext：当istext为是时必选，表示城市文本的内容。

bdcolor：当istext为是时必选，表示城市文本的颜色。

bdtextsize：当istext为是时必选，表示城市文本的字号。

### bdtext_info可选参数

bdname: 当istext为是时可选，默认为""，文本宾语名字。

bdoffset: 当istext为是时可选，数字数组，默认为"0 0"，文本宾语偏移。

bdoffsetsize: 当istext为是时可选，数字数组，默认为"0 0"，文本宾语大小改变。

## building_info

这是一个建筑添加info宾语。可以生成自动刷新建筑的宾语。
可以添加初始城市（inadd），确定城市初始阵营，附属宾语为inadd_info。城市可以提供文本生成（bdtext），显示城市名称，附属宾语为bdtext_info。因此，inadd_info和bdtext_info的所有必填参数和选填参数都在building_info中存在。

### building_info必填参数

prefix：标记宾语引用前缀。（[info宾语默认参数](#info宾语中基本参数介绍)）

idprefix: 表示所使用的id前缀，城市id在idprefix后将自动按照1,2...顺序延伸，请确保其他id没有此前缀。

detectReset: 建筑检测的resetActivationAfter。

addWarmup：建筑添加的warmup。

addReset：建筑添加的resetActivationAfter。

unit：建筑单位类型。

### building_info可选参数

isprefixseg: 可选，默认为否。（[info宾语默认参数](#info宾语中基本参数介绍)）

args：可选，默认没有，必填参数。（[info宾语默认参数](#info宾语中基本参数介绍)）

opargs：可选，默认没有，可选参数。（[info宾语默认参数](#info宾语中基本参数介绍)）

cite_name：可选，默认没有，标志宾语标记。（[info宾语默认参数](#info宾语中基本参数介绍)）

spawnnum：可选，默认为1，建筑添加的数量。

minUnits：可选，默认为1，建筑检测的minUnits。

maxUnits：可选，默认没有该参数，建筑检测的maxUnits。

team：可选，默认为-1，建筑添加的队伍。

isonlybuilding：可选，默认为否，是否启用onlybuilding来检测建筑。

isshowOnMap: 可选，默认为否，启用时，建筑生成时小地图显示。

addname：可选，默认为""，建筑添加宾语名字。

addoffset：可选，数字数组，默认为"0 0"，建筑添加宾语偏移。

addoffsetsize：可选，数字数组，默认为"0 0"，建筑添加宾语大小改变。

detectname: 可选，默认为"检测 {idprefix0}"，建筑检测宾语名字。

detectoffset: 可选，数字数组，默认为"-10 0"，建筑检测宾语偏移。

detectoffsetsize: 可选，数字数组，默认为"20 0"，建筑检测宾语大小改变。

inadd_prefix：可选，默认不存在。将会导入对应inadd_info的数据，建立初始建筑。

bdtext_prefix：可选，默认不存在。将会导入对应bdtext_info的数据，生成建筑名字。

## teamDetect_info

这是一个队伍检测info宾语。可以生成许多检测不同队伍单位宾语。

### teamDetect必选参数

prefix：标记宾语引用前缀。（[info宾语默认参数](#info宾语中基本参数介绍)）

unit：必选，检测单位类型。

reset：必选，表示检测宾语的刷新周期。

setTeam：数字二维数组，表示队伍分组。同阵营内部用空格隔开，阵营之间用逗号隔开。填写例子"0 2 4 6 8 10 12 14 16 18,1 3 5 7 9 11 13 15 17"。

setidTeam：字符串数组，表示队伍id前缀。不同阵营之间用逗号隔开，一个阵营仅有一个id。填写例子"A_city,B_city"。

### teamDetect可选参数

isprefixseg: 可选，默认为否。（[info宾语默认参数](#info宾语中基本参数介绍)）

args：可选，默认没有，必填参数。（[info宾语默认参数](#info宾语中基本参数介绍)）

opargs：可选，默认没有，可选参数。（[info宾语默认参数](#info宾语中基本参数介绍)）

cite_name：可选，默认没有，标志宾语标记。（[info宾语默认参数](#info宾语中基本参数介绍)）

minUnits：可选，默认为1，表示检测宾语的刷新周期。

maxUnits：可选，默认没有，表示检测宾语的刷新周期。

name：可选，字符串数组，默认为""，表示不同阵营宾语的名称。每个阵营仅会显示一个，不同阵营的名称之间用逗号隔开。填写例子"检测 setidTeam0_0,检测 setidTeam1_0"。

offset：可选，数字二维数组，默认自动进行错位显示，表示不同阵营宾语偏移。不同阵营之间用逗号隔开，一个阵营有x和y两个坐标，中间空格隔开。填写例子"0 -20,-20 0"。

offsetsize：可选，数字二维数组，默认自动进行错位显示，表示不同阵营宾语大小改变。不同阵营之间用逗号隔开，一个阵营有x和y两个坐标，中间空格隔开。填写例子"0 40,40 0"。

此外，还有大量only，将会原样添加到检测宾语中（如果有的话）。它们是：
onlyIdle,onlyBuildings,onlyMainBuildings,onlyEmptyQueue,onlyBuilders,onlyOnResourcePool,onlyAttack,onlyAttackAir,onlyTechLevel,includeIncomplete,onlyWithTag

## numDetect_info

这是一个多个单位检测info宾语。可以生成许多检测不同数量单位的宾语。

### numDetect必选参数

prefix：标记宾语引用前缀。（[info宾语默认参数](#info宾语中基本参数介绍)）

unit：必选，检测单位类型。

reset：必选，表示检测宾语的刷新周期。

team：必选，表示检测宾语的检测队伍

setNum：数字二维数组，表示不同数量检测的分组。使用相同id的检测内部用空格隔开（一组之内，两两分开，第一个做minUnits，第二个做maxUnits），使用不同id的检测之间用逗号隔开。填写例子"0 2 6 8,3 5"（检测到0-2,6-8个单位激活第一个id，检测到3-5个单位激活第二个id）（如果minUnits小于等于0，则不添加，如果maxUnits大于等于65536，则不添加）。

setidNum：字符串数组，表示不同数量检测的id前缀。不同检测id之间用逗号隔开，一个阵营仅有一个id。填写例子"A_city,B_city"。

### numDetect可选参数

isprefixseg: 可选，默认为否。（[info宾语默认参数](#info宾语中基本参数介绍)）

args：可选，默认没有，必填参数。（[info宾语默认参数](#info宾语中基本参数介绍)）

opargs：可选，默认没有，可选参数。（[info宾语默认参数](#info宾语中基本参数介绍)）

cite_name：可选，默认没有，标志宾语标记。（[info宾语默认参数](#info宾语中基本参数介绍)）

name：可选，字符串数组，默认为""，表示不同阵营宾语的名称。每个阵营仅会显示一个，不同阵营的名称之间用逗号隔开。填写例子"检测 setidTeam0_0,检测 setidTeam1_0"。

offset：可选，数字二维数组，默认自动进行错位显示，表示不同阵营宾语偏移。不同阵营之间用逗号隔开，一个阵营有x和y两个坐标，中间空格隔开。填写例子"0 -20,-20 0"。

offsetsize：可选，数字二维数组，默认自动进行错位显示，表示不同阵营宾语大小改变。不同阵营之间用逗号隔开，一个阵营有x和y两个坐标，中间空格隔开。填写例子"0 40,40 0"。

此外，还有大量only，将会原样添加到检测宾语中（如果有的话）。它们是：
onlyIdle,onlyBuildings,onlyMainBuildings,onlyEmptyQueue,onlyBuilders,onlyOnResourcePool,onlyAttack,onlyAttackAir,onlyTechLevel,includeIncomplete,onlyWithTag

## multiText_info

这是一个产生多个文本的info宾语。会根据规则自动产生一系列文本宾语。

### multiText必选参数

prefix：标记宾语引用前缀。（[info宾语默认参数](#info宾语中基本参数介绍)）

### multiText可选参数

isprefixseg: 可选，默认为否。（[info宾语默认参数](#info宾语中基本参数介绍)）

args：可选，默认没有，必填参数。（[info宾语默认参数](#info宾语中基本参数介绍)）

opargs：可选，默认没有，可选参数。（[info宾语默认参数](#info宾语中基本参数介绍)）

cite_name：可选，默认没有，标志宾语标记。（[info宾语默认参数](#info宾语中基本参数介绍)）

reset：可选，默认为1s，表示文本宾语的刷新周期。

acti：可选，字符串二维数组，默认没有。文本宾语的激活来源被";"分隔，将会添加进入。文本宾语数量保证将acti均加入。

deacti：可选，字符串二维数组，默认没有。文本宾语的抑制来源被";"分隔，将会添加进入。文本宾语数量保证将deacti均加入。

teamDetect_cite：可选，默认没有，teamDetect标记宾语引用。将会将teamDetect的id逐个加入激活中。如果isdefaultText选择，将继续所有teamDetect的id加入下一个的抑制中。文本宾语数量保证teamDetect_cite充分发挥作用。

numDetect_cite：可选，默认没有，numDetect标记宾语引用。将会将numDetect的id逐个加入激活中。文本宾语数量保证numDetect_cite充分发挥作用。

textsize：可选，字符串数组，默认没有。文本宾语文本的大小。textsize将尽力全部加入文本宾语组中。

color：可选，字符串数组，默认没有。文本宾语文本的颜色。color将尽力全部加入文本宾语组中。

text：可选，字符串数组，默认没有。文本宾语文本内容。text将尽力全部加入文本宾语组中。

name：可选，字符串数组，默认为""，表示不同阵营宾语的名称。每个阵营仅会显示一个，不同阵营的名称之间用逗号隔开。填写例子"检测 setidTeam0_0,检测 setidTeam1_0"。

offset：可选，数字二维数组，默认自动进行错位显示，表示不同阵营宾语偏移。不同阵营之间用逗号隔开，一个阵营有x和y两个坐标，中间空格隔开。填写例子"0 -20,-20 0"。

offsetsize：可选，数字二维数组，默认自动进行错位显示，表示不同阵营宾语大小改变。不同阵营之间用逗号隔开，一个阵营有x和y两个坐标，中间空格隔开。填写例子"0 40,40 0"。

## python使用

### 开始

下载任意一款python编译器。

### 安装

    pip install rwmapeditor-exgcdwu==1.6.0

### 使用

打开终端，输入如下指令：

    triggerauto {map_file}

该指令读入地图路径，将转换结果自动输到原路径。

### 命令参数

-o 输出到不同路径（建议，防止覆盖后无法悔改）。

-r 选择进行id的重置。不添加-r命令可以保证已有的id不会改变(从其他地方使用id不会断线错位)。

-d -D --DeleteAll：

默认情况下，带,d的info宾语或者标记宾语自动产生的宾语将会被删除（并且不产生），",d"后缀删除后仍然可以重新产生宾语。[正常使用]

-d 命令会同时把带,d的info宾语或者标记宾语(也包括其city_info带,d)删除，删除标记没有反悔机会。[删除决定去掉的标记宾语/info宾语]

-D 命令在-d命令的基础上，将所有info宾语和标记宾语删除，只留下使用宾语。[发布地图]

--DeleteAll 命令会将所有info宾语、标记宾语和自动产生的宾语均删除，彻底除去使用痕迹。[取消使用该宾语格式]

--resetid 命令将会将宾语ID重置为自然数列。

-v 显示运行信息

--infopath命令约定了.py文件路径，--infovar命令约定了变量名，随后程序会根据该约定变量来自动转换。
默认会使用auto/_data.py中的auto_func_arg作为约定变量。可以自行修改约定变量来个性化自动转换模式。

[约定变量](https://github.com/exgcdwu/Rusted-Warfare-map-editor-for-city-occupation-play-/blob/main/auto/_data.py)

### 其他特性

会检测info宾语和标记宾语的参数正确性，错误时返回错误信息。

会自动将info和标记宾语放到文件最后，保证在Tiled中info和标记宾语可以直接被点击到。

### 注意事项

#### team设置

和铁锈一样，team设置是从0开始的，-1中立，-2敌对。
