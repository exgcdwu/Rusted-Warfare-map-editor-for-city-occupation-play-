# 宾语自动添加教程

- [宾语自动添加教程](#宾语自动添加教程)
  - [目标](#目标)
  - [info宾语介绍](#info宾语介绍)
    - [info宾语中基本参数介绍](#info宾语中基本参数介绍)
    - [info宾语的其他说明](#info宾语的其他说明)
    - [info中的参数类型](#info中的参数类型)
  - [tree\_info](#tree_info)
    - [tree\_info必填参数](#tree_info必填参数)
    - [tree\_info可选参数](#tree_info可选参数)
    - [tree\_info可被引用的其他参数](#tree_info可被引用的其他参数)
  - [object\_info](#object_info)
    - [object\_info必填参数](#object_info必填参数)
    - [object\_info可选参数](#object_info可选参数)
  - [dictionary\_info](#dictionary_info)
    - [dictionary\_info必填参数](#dictionary_info必填参数)
    - [dictionary\_info可选参数](#dictionary_info可选参数)
  - [inadd\_info](#inadd_info)
    - [inadd\_info必选参数](#inadd_info必选参数)
    - [inadd\_info可选参数](#inadd_info可选参数)
  - [bdtext\_info](#bdtext_info)
    - [bdtext\_info必选参数](#bdtext_info必选参数)
    - [bdtext\_info可选参数](#bdtext_info可选参数)
  - [building\_info](#building_info)
    - [building\_info必填参数](#building_info必填参数)
    - [building\_info可选参数](#building_info可选参数)
    - [building\_info可被引用的其他参数](#building_info可被引用的其他参数)
  - [teamDetect\_info](#teamdetect_info)
    - [teamDetect必选参数](#teamdetect必选参数)
    - [teamDetect可选参数](#teamdetect可选参数)
    - [teamDetect\_info可被引用的其他参数](#teamdetect_info可被引用的其他参数)
  - [numDetect\_info](#numdetect_info)
    - [numDetect必选参数](#numdetect必选参数)
    - [numDetect可选参数](#numdetect可选参数)
    - [numDetect\_info可被引用的其他参数](#numdetect_info可被引用的其他参数)
  - [multiText\_info](#multitext_info)
    - [multiText必选参数](#multitext必选参数)
    - [multiText可选参数](#multitext可选参数)
  - [multiRemove\_info](#multiremove_info)
    - [multiRemove必选参数](#multiremove必选参数)
    - [multiRemove可选参数](#multiremove可选参数)
  - [python使用](#python使用)
    - [开始](#开始)
    - [安装](#安装)
    - [使用](#使用)
    - [命令参数](#命令参数)
    - [其他特性](#其他特性)
    - [注意事项](#注意事项)
      - [team设置](#team设置)
      - [造成混淆的宾语](#造成混淆的宾语)
      - [自动化后的地图处理](#自动化后的地图处理)

## 目标

该命令行工具旨在简化城夺地图的制作。对于需要在不同位置放置相同宾语，但仅仅一些细节不同的时候，可以使用该工具简化操作。

只需要按照命令行教程的格式在地图文件中添加额外的info宾语（需要填写大量参数）和标记宾语（仅有名称需要填写,类型不需要填写），标记宾语就会根据info宾语自动生成想要的宾语。

具体来说，程序会识别标记宾语名称的前缀(prefix)，来找到指定的info宾语，并根据该info宾语的内容按照约定导入相关属性。相关属性可指定标记宾语的必填参数和可选参数，标记宾语可以依照info宾语的格式填写参数。

想要运行程序来进行自动转换，需要python编译器，下载指定库，并使用终端命令行操作您的地图文件，达到自动转换目的。

还可以使用Termux来在手机上操作python和命令行。
[github Termux](https://github.com/termux/termux-app)

termux python环境及包下载（需要一段时间，保持网络畅通）（中间出现的提问选项，全部输入y再回车）：
*感谢kend在使用termux安装python包方面的帮助*

    pkg update -y
    pkg install -y python
    pkg install -y python-numpy
    pkg install -y python-pillow
    pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple #（如果清华镜像不可以，换成别的镜像比如https://pypi.mirrors.ustc.edu.cn/simple也行）
    pip install asteval
    pip install regex # 1.6.3新加入
    pip install rwmapeditor-exgcdwu==1.6.3 --no-deps

需要获取读取存储权限：

    termux-setup-storage

之后就可以使用termux使用triggerauto处理地图文件了。

如果想要更改版本，使用如下命令行。

    pip uninstall -y rwmapeditor-exgcdwu
    pip install rwmapeditor-exgcdwu==1.6.1 --no-deps #（新版本，大于等于1.6.1）

## info宾语介绍

info宾语是执行一切自动转换的基础，地图作者需要将生成的不同组宾语中相同的参数放入info宾语，并将不同的参数设置为在标记宾语中才会填写的参数。

info宾语的名字必须以xxx_info开头，后面可以跟任意字符。后方可以存在",d"，表明添加了删除标记，该info宾语将不能参与宾语生成。

### info宾语中基本参数介绍

prefix: 填写标记宾语的前缀（或者其他info宾语的引用），在标记宾语名称开头加入prefix即证明该标记宾语使用该info宾语的格式。

isprefixseg：标记宾语中，前缀之后加入必填参数时，是否跟一个"."。

args: 声明标记宾语的必填参数。比如"unit,str;num,str"，这一串表明标记宾语必须填入2个参数，第一个是代入unit，第二个代入num。参数名后面目前只支持str格式。标记宾语在前缀之后添加supplyDepot.1意思是unit为supplyDepot，num为1。如果info宾语的prefix为e，那么标记宾语将填esupplyDepot.1。如果isprefixseg标记了，那么标记宾语将填e.supplyDepot.1。

opargs: 声明标记宾语的选填参数。比如"u,unit,str,supplyDepot;n,num,str,2"，这一串表明unit和num是可以选填的（第一个参数必须只有一个字母）。想填写unit为supplyDepot时需要输入",usupplyDepot"。想填写num为1时需要输入",n1"。注意，即使没有填写num，num默认为2。
*,d是默认存在的选项，加入即证明该标记宾语被打上了删除标记*

*参数事实上可以不添加info有的参数，可以自创一个参数，但在实际参数中引用。比如args设置为"buildingname,str"，而info中写unit:{buildingname}，inaddunit:{buildingname}。可以实现复用。*

cite_name：标记宾语的引用，如果没有，无法被引用。比如在某info宾语中设置args为"cite_name,str"，在使用该info宾语格式的标记宾语中名称为"e.td"，其中e是前缀。在cite_name后面加"."再添加属性名称，即可实现引用。比如td.unit表明将会引用该标记宾语的其中unit的内容。
*不得出现循环引用，文件中靠前的宾语不得引用靠后的宾语。*

brace：字符串数组。在最后会将数组中的所有键进行字符串翻译，以为外部引用提供良好的代入环境。比如，设置brace为"a"，a为"{setidTeam0_0}"，cite_name为"m1"。这样外部出现m1.a时，相当于得到了队伍检测的第一个id。

### info宾语的其他说明

无参数表明将不支持args和opargs。附属info宾语表示该info宾语不能独立指定相关标记宾语，只能被其他info宾语引用自己的prefix导入参数，并且不支持brace。

### info中的参数类型

请注意，is前缀的需要改变其数据类型为bool（文本文件中的形式为 type="bool" value="true" 或者 value="true"）。

存在一些需要输入多个数据的属性，这些属性格式总结如下：

字符串数组：字符串之间用','隔开

数字数组：数字之间用' '隔开

字符串二维数组：第一维用";"隔开，第二维用","隔开

数字二维数组：第一维用","隔开，第二维用" "隔开

info宾语内的属性也可以互相引用。假如info宾语内有一个属性为unit:supplyDepot。那么，设置另一个属性为inaddunit:{unit}即可实现引用（引用自己标记宾语的属性）。

## tree_info

这是一个可以产生其他标志宾语的info宾语。产生的新标志宾语将会继续产生新宾语。会形成类似一棵树的结构。

### tree_info必填参数

prefix：标记宾语引用前缀。（[info宾语默认参数](#info宾语中基本参数介绍)）

name：字符串二维数组。用;分割开来新产生标志宾语的name，建议大量使用引用。

### tree_info可选参数

isprefixseg: 可选，默认为是。（[info宾语默认参数](#info宾语中基本参数介绍)）

args：可选，默认没有，必填参数。（[info宾语默认参数](#info宾语中基本参数介绍)）

opargs：可选，默认没有，可选参数。（[info宾语默认参数](#info宾语中基本参数介绍)）

cite_name：可选，默认没有，标志宾语标记。（[info宾语默认参数](#info宾语中基本参数介绍)）

brace：可选，默认没有，外部引用翻译列表。（[info宾语默认参数](#info宾语中基本参数介绍)）

idprefix：可选，字符串二维数组，默认没有。每一列第一个表示要获取的id前缀，第二个表示要获取的id前缀的数量。这些id应当被用于cite_name。

offset：可选，数字二维数组，默认"0 0"，表示不同分支标记宾语偏移。当只有一个坐标时，该偏移对所有分支均适用。不同分支之间用逗号隔开，一个分支有x和y两个坐标，中间空格隔开。填写例子"0 -20,-20 0"。

offsetsize：可选，数字二维数组，默认"0 0"，表示不同分支标记宾语大小改变。当只有一个坐标时，该偏移对所有分支均适用。不同分支之间用逗号隔开，一个阵营有x和y两个坐标，中间空格隔开。填写例子"0 40,40 0"。

### tree_info可被引用的其他参数

idprefix{i}_{j}是检测的id。i是第几个id前缀产生的id，j是该id前缀获得的第几个id。

## object_info

这是一个任意生成一个宾语的info宾语。

### object_info必填参数

prefix：标记宾语引用前缀。（[info宾语默认参数](#info宾语中基本参数介绍)）

### object_info可选参数

isprefixseg: 可选，默认为否。（[info宾语默认参数](#info宾语中基本参数介绍)）

args：可选，默认没有，必填参数。（[info宾语默认参数](#info宾语中基本参数介绍)）

opargs：可选，默认没有，可选参数。（[info宾语默认参数](#info宾语中基本参数介绍)）

cite_name：可选，默认没有，标志宾语标记。（[info宾语默认参数](#info宾语中基本参数介绍)）

brace：可选，默认没有，外部引用翻译列表。（[info宾语默认参数](#info宾语中基本参数介绍)）

所有可能的宾语参数都能添加，标志宾语将会按程序生成一个对应的宾语。

## dictionary_info

这是一个可以书写键值对以供引用的info宾语，任何键值对均可写入。info宾语写完后，再写一个标志宾语就可以进行引用了。

### dictionary_info必填参数

prefix：标记宾语引用前缀。（[info宾语默认参数](#info宾语中基本参数介绍)）

cite_name：第一个必填参数，标志宾语标记。（[info宾语默认参数](#info宾语中基本参数介绍)）

brace：可选，默认没有，外部引用翻译列表。（[info宾语默认参数](#info宾语中基本参数介绍)）

### dictionary_info可选参数

isprefixseg: 可选，默认为是。（[info宾语默认参数](#info宾语中基本参数介绍)）

还有任意键值对。

## inadd_info

初始单位添加宾语，是附属宾语，且无参数。

### inadd_info必选参数

prefix：其他info宾语引用标记。（[info宾语默认参数](#info宾语中基本参数介绍)）

isinadd：可选，默认为是，在building_info中默认为否，是否添加城市的初始刷新。

inaddunit：当isinadd为是时必选，表示单位添加的类型。

inaddspawnnum：当isinadd为是时必选，表示单位添加的数量。

inaddteam：当isinadd为是时必选，表示单位添加的队伍。

inaddwarmup：当isinadd为是时必选，表示单位添加的warmup。

### inadd_info可选参数

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

brace：可选，默认没有，外部引用翻译列表。（[info宾语默认参数](#info宾语中基本参数介绍)）

spawnnum：可选，默认为1，建筑添加的数量。

minUnits：可选，默认为1，建筑检测的minUnits。

maxUnits：可选，默认没有该参数，建筑检测的maxUnits。

team：可选，默认为-1，建筑添加的队伍。

isonlybuilding：可选，默认为否，是否启用onlybuilding来检测建筑，如果启用，则不使用unitType检测。

isshowOnMap: 可选，默认为否，启用时，建筑生成时小地图显示。

addname：可选，默认为""，建筑添加宾语名字。

addoffset：可选，数字数组，默认为"0 0"，建筑添加宾语偏移。

addoffsetsize：可选，数字数组，默认为"0 0"，建筑添加宾语大小改变。

detectname: 可选，默认为"检测 "，建筑检测宾语名字。

detectoffset: 可选，数字数组，默认为"-10 0"，建筑检测宾语偏移。

detectoffsetsize: 可选，数字数组，默认为"20 0"，建筑检测宾语大小改变。

inadd_prefix：可选，默认不存在。将会导入对应inadd_info的数据，建立初始建筑。

bdtext_prefix：可选，默认不存在。将会导入对应bdtext_info的数据，生成建筑名字。

### building_info可被引用的其他参数

idprefix0是建筑检测的id。

## teamDetect_info

这是一个队伍检测info宾语。可以生成许多检测不同队伍单位宾语。

### teamDetect必选参数

prefix：标记宾语引用前缀。（[info宾语默认参数](#info宾语中基本参数介绍)）

reset：必选，表示检测宾语的刷新周期。

setTeam：数字二维数组，表示队伍分组。同阵营内部用空格隔开，阵营之间用逗号隔开。填写例子"0 2 4 6 8 10 12 14 16 18,1 3 5 7 9 11 13 15 17"。

setidTeam：字符串数组，表示队伍id前缀。不同阵营之间用逗号隔开，一个阵营仅有一个id。填写例子"A_city,B_city"。

### teamDetect可选参数

isprefixseg: 可选，默认为否。（[info宾语默认参数](#info宾语中基本参数介绍)）

args：可选，默认没有，必填参数。（[info宾语默认参数](#info宾语中基本参数介绍)）

opargs：可选，默认没有，可选参数。（[info宾语默认参数](#info宾语中基本参数介绍)）

cite_name：可选，默认没有，标志宾语标记。（[info宾语默认参数](#info宾语中基本参数介绍)）

brace：可选，默认没有，外部引用翻译列表。（[info宾语默认参数](#info宾语中基本参数介绍)）

unit：可选，检测单位类型，用于unitType。

minUnits：可选，默认为1，表示检测宾语的刷新周期。

maxUnits：可选，默认没有，表示检测宾语的刷新周期。

name：可选，字符串数组，默认为"{setidTeam0_0[len(setidTeam[0]):]},{setidTeam1_0[len(setidTeam[1]):]},..."，表示不同阵营宾语的名称。每个阵营仅会显示一个，不同阵营的名称之间用逗号隔开。填写例子"setidTeam0_0,setidTeam1_0"。

offset：可选，数字二维数组，默认"0 0"，表示不同阵营宾语偏移。当只有一个坐标时，该偏移对所有阵营均适用。不同阵营之间用逗号隔开，一个阵营有x和y两个坐标，中间空格隔开。填写例子"0 -20,-20 0"。

offsetsize：可选，数字二维数组，默认"0 0"，表示不同阵营宾语大小改变。当只有一个坐标时，该偏移对所有阵营均适用。不同阵营之间用逗号隔开，一个阵营有x和y两个坐标，中间空格隔开。填写例子"0 40,40 0"。

此外，还有大量only，将会原样添加到检测宾语中（如果有的话）。它们是：
onlyIdle,onlyBuildings,onlyMainBuildings,onlyEmptyQueue,onlyBuilders,onlyOnResourcePool,onlyAttack,onlyAttackAir,onlyTechLevel,includeIncomplete,onlyWithTag

### teamDetect_info可被引用的其他参数

setidTeam0_0,setidTeam1_0...是生成的id。

## numDetect_info

这是一个多个单位检测info宾语。可以生成许多检测不同数量单位的宾语。

### numDetect必选参数

prefix：标记宾语引用前缀。（[info宾语默认参数](#info宾语中基本参数介绍)）

reset：必选，表示检测宾语的刷新周期。

team：必选，表示检测宾语的检测队伍

setNum：数字二维数组，表示不同数量检测的分组。使用相同id的检测内部用空格隔开（一组之内，两两分开，第一个做minUnits，第二个做maxUnits），使用不同id的检测之间用逗号隔开。填写例子"0 2 6 8,3 5"（检测到0-2,6-8个单位激活第一个id，检测到3-5个单位激活第二个id）（如果minUnits小于等于0，则不添加，如果maxUnits大于等于65536，则不添加）。

setidNum：字符串数组，表示不同数量检测的id前缀。不同检测id之间用逗号隔开，一个阵营仅有一个id。填写例子"A_city,B_city"。

### numDetect可选参数

isprefixseg: 可选，默认为否。（[info宾语默认参数](#info宾语中基本参数介绍)）

args：可选，默认没有，必填参数。（[info宾语默认参数](#info宾语中基本参数介绍)）

opargs：可选，默认没有，可选参数。（[info宾语默认参数](#info宾语中基本参数介绍)）

cite_name：可选，默认没有，标志宾语标记。（[info宾语默认参数](#info宾语中基本参数介绍)）

brace：可选，默认没有，外部引用翻译列表。（[info宾语默认参数](#info宾语中基本参数介绍)）

unit：可选，检测单位类型，用于unitType。

name：可选，字符串数组，默认为""，表示不同组宾语的名称。每个组仅会显示一个，不同组的名称之间用逗号隔开。

offset：可选，数字二维数组，默认"0 0"，表示不同组宾语偏移。当只有一个坐标时，该偏移对所有组均适用。不同组之间用逗号隔开，一个组有x和y两个坐标，中间空格隔开。填写例子"0 -20,-20 0"。

offsetsize：可选，数字二维数组，默认"0 0"，表示不同组宾语大小改变。当只有一个坐标时，该偏移对所有组均适用。不同组之间用逗号隔开，一个组有x和y两个坐标，中间空格隔开。填写例子"0 40,40 0"。

此外，还有大量only，将会原样添加到检测宾语中（如果有的话）。它们是：
onlyIdle,onlyBuildings,onlyMainBuildings,onlyEmptyQueue,onlyBuilders,onlyOnResourcePool,onlyAttack,onlyAttackAir,onlyTechLevel,includeIncomplete,onlyWithTag

### numDetect_info可被引用的其他参数

setidNum0_0,setidNum1_0...是生成的id。

## multiText_info

这是一个产生多个文本的info宾语。会根据规则自动产生一系列文本宾语。

### multiText必选参数

prefix：标记宾语引用前缀。（[info宾语默认参数](#info宾语中基本参数介绍)）

### multiText可选参数

isprefixseg: 可选，默认为否。（[info宾语默认参数](#info宾语中基本参数介绍)）

args：可选，默认没有，必填参数。（[info宾语默认参数](#info宾语中基本参数介绍)）

opargs：可选，默认没有，可选参数。（[info宾语默认参数](#info宾语中基本参数介绍)）

cite_name：可选，默认没有，标志宾语标记。（[info宾语默认参数](#info宾语中基本参数介绍)）

brace：可选，默认没有，外部引用翻译列表。（[info宾语默认参数](#info宾语中基本参数介绍)）

reset：可选，默认为1s，表示文本宾语的刷新周期。

acti：可选，字符串二维数组，默认没有。文本宾语的激活来源被";"分隔，将会添加进入。文本宾语数量保证将acti均加入。

deacti：可选，字符串二维数组，默认没有。文本宾语的抑制来源被";"分隔，将会添加进入。文本宾语数量保证将deacti均加入。

teamDetect_cite：可选，默认没有，teamDetect标记宾语引用。将会将teamDetect的id逐个加入激活中。如果isdefaultText选择，将继续所有teamDetect的id加入下一个的抑制中。文本宾语数量保证teamDetect_cite充分发挥作用。

isdefaultText：可选，默认为否，teamDetect_cite是否包含默认文本。具体见上文teamDetect_cite。

numDetect_cite：可选，默认没有，numDetect标记宾语引用。将会将numDetect的id逐个加入激活中。文本宾语数量保证numDetect_cite充分发挥作用。

textsize：可选，字符串数组，默认没有。文本宾语文本的大小。如果仅有一个，那么该textsize将会应用于所有产生文本宾语中。textsize将尽力全部加入文本宾语组中。

color：可选，字符串数组，默认没有。文本宾语文本的颜色。如果仅有一个，那么该color将会应用于所有产生文本宾语中。color将尽力全部加入文本宾语组中。

text：可选，字符串数组，默认没有。文本宾语文本内容。如果仅有一个，那么该text将会应用于所有产生文本宾语中。text将尽力全部加入文本宾语组中。

name：可选，字符串数组，默认为""，表示不同阵营宾语的名称。每个阵营仅会显示一个，不同阵营的名称之间用逗号隔开。

offset：可选，数字二维数组，默认"0 0"，表示不同组宾语偏移。当只有一个坐标时，该偏移对所有组均适用。不同组之间用逗号隔开，一个组有x和y两个坐标，中间空格隔开。填写例子"0 -20,-20 0"。

offsetsize：可选，数字二维数组，默认"0 0"，表示不同组宾语大小改变。当只有一个坐标时，该偏移对所有组均适用。不同组之间用逗号隔开，一个组有x和y两个坐标，中间空格隔开。填写例子"0 40,40 0"。

## multiRemove_info

这是一个产生多个删除宾语的info宾语。类似于multiText。

### multiRemove必选参数

prefix：标记宾语引用前缀。（[info宾语默认参数](#info宾语中基本参数介绍)）

### multiRemove可选参数

isprefixseg: 可选，默认为否。（[info宾语默认参数](#info宾语中基本参数介绍)）

args：可选，默认没有，必填参数。（[info宾语默认参数](#info宾语中基本参数介绍)）

opargs：可选，默认没有，可选参数。（[info宾语默认参数](#info宾语中基本参数介绍)）

cite_name：可选，默认没有，标志宾语标记。（[info宾语默认参数](#info宾语中基本参数介绍)）

brace：可选，默认没有，外部引用翻译列表。（[info宾语默认参数](#info宾语中基本参数介绍)）

acti：可选，字符串二维数组，默认没有。删除宾语的激活来源被";"分隔，将会添加进入。删除宾语数量保证将acti均加入。

deacti：可选，字符串二维数组，默认没有。删除宾语的抑制来源被";"分隔，将会添加进入。删除宾语数量保证将deacti均加入。

teamDetect_cite：可选，默认没有，teamDetect标记宾语引用。将会将teamDetect的id逐个加入激活中。删除宾语数量保证teamDetect_cite充分发挥作用。

numDetect_cite：可选，默认没有，numDetect标记宾语引用。将会将numDetect的id逐个加入激活中。删除宾语数量保证numDetect_cite充分发挥作用。

warmup：可选，字符串数组，默认没有。删除宾语的warmup。如果仅有一个，那么warmup将会应用于所有删除宾语中。warmup将尽力全部加入删除宾语组中。

reset：可选，字符串数组，默认没有。删除宾语的resetActivationAfter。如果仅有一个，那么该reset将会应用于所有删除宾语中。reset将尽力全部加入删除宾语组中。

team：可选，字符串数组，默认没有。删除宾语队伍。如果仅有一个，那么team将会应用于所有删除宾语中。team将尽力全部加入删除宾语组中。

name：可选，字符串数组，默认为""，表示不同组宾语的名称。每个组宾语仅会显示一个，不同组宾语的名称之间用逗号隔开。

offset：可选，数字二维数组，默认"0 0"，表示不同组宾语偏移。当只有一个坐标时，该偏移对所有组均适用。不同组之间用逗号隔开，一个组有x和y两个坐标，中间空格隔开。填写例子"0 -20,-20 0"。

offsetsize：可选，数字二维数组，默认"0 0"，表示不同组宾语大小改变。当只有一个坐标时，该偏移对所有组均适用。不同组之间用逗号隔开，一个组有x和y两个坐标，中间空格隔开。填写例子"0 40,40 0"。

## python使用

### 开始

下载任意一款python编译器。

### 安装

    pip install rwmapeditor-exgcdwu==1.6.3

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

--resetid 命令将会将宾语ID重置为自然数列。应当添加，否则ID空洞会越来越多，尤其是同一地图频繁进行自动化操作。不添加对实际地图没有影响。

-v 显示运行信息

--infopath命令约定了.py文件路径，--infovar命令约定了变量名，随后程序会根据该约定变量来自动转换。
默认会使用auto/_data中的auto_func_arg作为约定变量。可以自行修改约定变量来个性化自动转换模式。

-c表明除了info宾语，标记宾语，以及标记宾语产生的宾语，其他宾语也可以使用引用来获得参数。

[约定变量](https://github.com/exgcdwu/Rusted-Warfare-map-editor-for-city-occupation-play-/blob/main/auto/_data/)

### 其他特性

会检测info宾语和标记宾语的参数正确性，错误时返回错误信息。

会自动将info和标记宾语放到文件最后，保证在Tiled中info和标记宾语可以直接被点击到。

### 注意事项

#### team设置

和铁锈一样，team设置是从0开始的，-1中立，-2敌对。

#### 造成混淆的宾语

所有type一栏空着的宾语，但与info不产生联系。

#### 自动化后的地图处理

如果要清除一组宾语，不得擅自删除。请在标志宾语后面添加,d（暂时清除，不产生新宾语）或者,D（无论如何都会删除）。再运行自动化程序。不经过以上步骤的删除，可能造成不良后果。
