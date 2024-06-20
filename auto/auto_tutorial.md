# Auto object adder tutorial

## Objective

该命令行工具旨在简化城夺地图的制作。对于需要在不同位置放置相同宾语，但仅仅一些细节不同的时候，可以使用该工具简化操作。

只需要按照命令行教程的格式在地图文件中添加额外的info宾语（需要填写大量参数）和标记宾语（仅有名称需要填写），标记宾语就会根据info宾语自动在原地生成想要的宾语。

具体来说，程序会识别标记宾语名称的前缀(prefix)，来找到指定的info宾语，并根据该info宾语的内容按照约定自动生成新的宾语。该约定变量由--infopath --infovar命令确定，无该命令是提供默认约定变量。

想要运行程序来进行自动转换，需要python编译器，下载指定库，并使用终端命令行操作您的地图文件，达到自动转换目的。

## info objects

自动建立城市需要事先提供格式。请在任意位置部署一个或多个名称包含info宾语，类型不填。有多种info宾语，可以提供自动生成的不同格式。
,d是可选项（放在info宾语名称的最后），表示想要删除该城市类型下所有自动产生的宾语
如果有多个，请让它们的前缀(prefix)之间不能互为前缀，这样可以采用多种格式来部署城市（通过前缀区分）。

存在附属info宾语，请不要使用附属info宾语的prefix来做标记宾语。附属info宾语仅可以被正常info宾语使用相关info_prefix导入。

## info arguments

请注意，is前缀的需要改变其数据类型为bool（形式为 type="bool" value="true" 或者 value="true"）。

存在一些需要输入多个数据的属性，这些属性格式总结如下：

字符串数组：字符串之间用','隔开

数字数组：数字之间用' '隔开

字符串二维数组：第一维用";"隔开，第二维用","隔开

数字二维数组：第一维用","隔开，第二维用" "隔开

## city_info

这是一个城市添加info宾语。可以生成自动刷新城市的宾语。此外，此info宾语提供了许多可选项以供实现复杂功能。
可以添加初始城市（inadd），确定城市初始阵营。
城市可以提供阵营检测（teamDetect），从而激活或抑制其他宾语。城市可以提供文本生成（mapText），显示城市名称。并且可以选择根据城市所属阵营改变城市颜色（teamText）。

此外，还有四种附属info宾语可以为city_info提供信息。

### Required

prefix：表示城市前缀。

idprefix: 表示所使用的id前缀，城市id在idprefix后将自动按照1,2...顺序延伸，请确保其他id没有此前缀。

detectReset: 城市检测的resetActivationAfter。

addWarmup：城市添加的warmup。

addReset：城市添加的resetActivationAfter。

unit：城市所用的建筑单位。

### Optional

isonlybuilding：可选，默认为否，是否启用onlybuilding来检测城市。

isprefixseg: 可选，默认为否，启用时，prefix与cityname之间需要'.'隔开。

isshowOnMap: 可选，默认为否，启用时，城市生成时小地图显示。

unitAddname：可选，默认为""，建筑添加宾语名字。

unitAddoffset：可选，数字数组，默认为"0 0"，建筑添加宾语偏移。

unitAddoffsetsize：可选，数字数组，默认为"0 0"，建筑添加宾语大小改变。

unitDetectname: 可选，默认为"检测 {idprefix0}"，建筑检测宾语名字。

unitDetectoffset": 可选，数字数组，默认为"-10 0"，建筑检测宾语偏移。

unitDetectoffsetsize": 可选，数字数组，默认为"20 0"，建筑检测宾语大小改变。

### info optional

#### inadd_info

inadd_prefix：可选，可以添加inadd_info宾语的prefix确定将该inadd_info载入，载入后相关参数仍可修改。

isinadd：可选，默认为否，在inadd_info中默认为是，是否添加城市的初始刷新。

inaddWarmup：当isinadd为是时可选，默认"0s"，表示初始刷新的warmup。

isinshowOnMap: 当isinadd为是时可选，默认为否，启用时，初始城市生成时小地图显示。

inunitAddname：当isinadd为是时可选，默认为"{team}"，建筑初始添加宾语名字。

inunitAddoffset: 当isinadd为是时可选，数字数组，默认为"-20 0"，建筑初始添加宾语偏移。

inunitAddoffsetsize: 当isinadd为是时可选，数字数组，默认为"40 0"，建筑初始添加宾语大小改变。

#### text_info

text_prefix：可选，可以添加text_info宾语的prefix确定将该text_info载入，载入后相关参数仍可修改。

istext：可选，默认为否，在text_info中默认为是，是否有文本显示。

textColor：当istext为是时必选，表示城市文本的颜色。

textSize：当istext为是时必选，表示城市文本的字号。

mapTextname: 当istext为是时可选，默认为""，文本宾语名字。

mapTextoffset: 当istext为是时可选，数字数组，默认为"0 0"，文本宾语偏移。

mapTextoffsetsize: 当istext为是时可选，数字数组，默认为"0 0"，文本宾语大小改变。

#### teamDetect_info

teamDetect_prefix：可选，可以添加teamDetect_info宾语的prefix确定将该teamDetect_info载入，载入后相关参数仍可修改。

isteamDetect：可选，默认为否，在teamDetect_info中默认为是，是否有队伍检测显示。

teamDetectreset：当isteamDetect为是时必选，表示检测宾语的刷新周期。

setTeam：当isteamDetect为是时必选，数字二维数组，表示队伍分组。同阵营内部用空格隔开，阵营之间用逗号隔开。填写例子"0 2 4 6 8 10 12 14 16 18,1 3 5 7 9 11 13 15 17"。

setidTeam：当isteamDetect为是时必选，字符串数组，表示队伍id前缀。不同阵营之间用逗号隔开，一个阵营仅有一个id。填写例子"A_city,B_city"。

teamDetectname：当isteamDetect为是时可选，字符串数组，默认为"检测 setidTeam0_0, 检测setidTeam1_0,..."，表示不同阵营宾语的名称。每个阵营仅会显示一个，不同阵营的名称之间用逗号隔开。填写例子"检测 setidTeam0_0,检测 setidTeam1_0"。

teamDetectoffset：当isteamDetect为是时可选，数字二维数组，默认自动进行错位显示，表示不同阵营宾语偏移。不同阵营之间用逗号隔开，一个阵营有x和y两个坐标，中间空格隔开。填写例子"0 -20,-20 0"。

teamDetectoffsetsize：当isteamDetect为是时可选，数字二维数组，默认自动进行错位显示，表示不同阵营宾语大小改变。不同阵营之间用逗号隔开，一个阵营有x和y两个坐标，中间空格隔开。填写例子"0 40,40 0"。

#### teamText_info

teamText_prefix：可选，可以添加teamText_info宾语的prefix确定将该teamText_info载入，载入后相关参数仍可修改。

isteamText：当istext和isteamDetect为是时可选，默认为否，在teamText_info中默认为是，是否有队伍文本显示。

teamTextcolor：当isteamText为是时必选，字符串数组，表示不同阵营文本颜色。不同阵营之间用逗号隔开，一个阵营仅有一个颜色。填写例子"#520FFF,#FFF520"。在不受任何玩家控制时，颜色为textColor。

teamTextreset：当isteamText为是时可选，默认为"1s"，表示队伍文本宾语刷新周期。

teamTextname：当isteamText为是时可选，字符串数组，默认为",,..."，表示不同阵营宾语的名称。每个阵营仅会显示一个，不同阵营的名称之间用逗号隔开。填写例子"文本 setidTeam0_0 颜色 teamTextcolor[0],文本 setidTeam1_0 颜色 teamTextcolor[1]"。

teamTextoffset：当isteamText为是时可选，数字二维数组，默认为"0 0,0 0,..."，表示不同阵营宾语偏移。不同阵营之间用逗号隔开，一个阵营有x和y两个坐标，中间空格隔开。填写例子"0 -5,-5 0"。

teamTextoffsetsize：当isteamText为是时可选，数字二维数组，默认"0 0,0 0,..."，表示不同阵营宾语大小改变。不同阵营之间用逗号隔开，一个阵营有x和y两个坐标，中间空格隔开。填写例子"0 10,10 0"。

## tagged objects

### city tagged objects

在任意处添加宾语，然后名称格式为{prefix}{cityname}(,t{number})（实际没有大括号和小括号）。

prefix为前缀，表明使用的格式。

cityname为城市名称，该城市名称会出现在显示文本中（isprefixseg为是时，prefix和cityname之间有'.'，如果为否，不要有'.'）。

,t是可选项，当添加城市的初始刷新时，可以在最后加上,t，后面跟上队伍数字，将会决定该建筑开局的归属，默认为-1，即中立单位。

,d是可选项，表示想要删除该标记宾语产生的宾语。

## python process

### start

下载任意一款python编译器。

### install

    pip install rwmapeditor-exgcdwu==1.5.9

### use

打开终端，输入如下指令：

    triggerauto {map_file}

该指令读入地图路径，将转换结果自动输到原路径。

### Command arguments

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

### Other features

会检测info宾语和标记宾语的参数正确性，错误时返回错误信息。

会自动将info和标记宾语放到文件最后，保证在Tiled中info和标记宾语可以直接被点击到。

### Cautions

和铁锈一样，team设置是从0开始的，-1中立，-2敌对。

## Troubleshooting
