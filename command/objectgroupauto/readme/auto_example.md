# 宾语自动化示例说明

- [宾语自动化示例说明](#宾语自动化示例说明)
  - [开始使用](#开始使用)
  - [标记宾语](#标记宾语)
  - [地图示例格式](#地图示例格式)
  - [万能速查](#万能速查)
  - [塔防t](#塔防t)
    - [必填参数-塔防建筑](#必填参数-塔防建筑)
    - [选填参数-塔防建筑](#选填参数-塔防建筑)
    - [info中可改变的参数-塔防建筑](#info中可改变的参数-塔防建筑)
  - [周期振荡器fd](#周期振荡器fd)
    - [必填参数-周期振荡器](#必填参数-周期振荡器)
  - [单次振荡器fi](#单次振荡器fi)
    - [必填参数-单次振荡器](#必填参数-单次振荡器)
  - [方波器si](#方波器si)
    - [必填参数-方波器](#必填参数-方波器)
    - [选填参数-方波器](#选填参数-方波器)
    - [info中可改变的参数-方波器](#info中可改变的参数-方波器)
  - [附属建筑b](#附属建筑b)
    - [必填参数-附属建筑](#必填参数-附属建筑)
    - [选填参数-附属建筑](#选填参数-附属建筑)
    - [info中可改变的参数-附属建筑](#info中可改变的参数-附属建筑)
  - [城市检测可视化ic](#城市检测可视化ic)
    - [必填参数-城市检测可视化](#必填参数-城市检测可视化)
    - [info中可改变的参数-城市检测可视化](#info中可改变的参数-城市检测可视化)
  - [万能城市c](#万能城市c)
    - [必填参数-万能城市](#必填参数-万能城市)
    - [选填参数-万能城市](#选填参数-万能城市)
    - [info中可改变的参数-万能城市](#info中可改变的参数-万能城市)
  - [万能刷兵a](#万能刷兵a)
    - [必填参数-万能刷兵](#必填参数-万能刷兵)
    - [选填参数-万能刷兵](#选填参数-万能刷兵)
    - [info中可改变的参数-万能刷兵](#info中可改变的参数-万能刷兵)
  - [注意事项](#注意事项)
    - [标记宾语顺序](#标记宾语顺序)
    - [team](#team)
    - [时间](#时间)

## 开始使用

打开Termux应用或安装有python库rwmapeditor-exgcdwu的终端，请输入（文件名字应当为实际的文件路径，手机上请用mt浏览器查询文件路径）:

    objectgroupauto "宾语自动化例子(1.8.7.3).tmx" -o "宾语自动化结果展示(铁锈可以打开)(1.8.7.3).tmx" -v -y -D -di -c

可以用铁锈打开"宾语自动化例子"自动化后产生的新文件。

一个可以参考宾语自动化示例说明的文件，应当按照以下步骤创造:

    创建您的新地图

    创建Triggers触发层

    将"宾语自动化例子"文件中所有"info"宾语以及"dd.d"或者形如"ddx.dx"(x是一个不同的字母)的宾语复制粘贴进您的地图。以及fi,fd,si宾语复制粘贴进入（这些宾语不得与其他宾语重合，应当在地图外。）

然后开始编写标记宾语，然后运行:

    objectgroupauto "地图(未自动化).tmx" -o "地图.tmx" -v -y -D -di -c

这样就能将自己的地图自动化了。

之后将会介绍宾语自动化例子地图的格式，以及如何编写标记宾语。

## 标记宾语

标记宾语是一个没有类型，但有名称的宾语，且名称中有特定的前缀。在这里举几个例子(使用宾语自动化模板的)：

  t0 一个初始玩家为1的塔防

  t0,usu 一个初始玩家为1的补给站

  c0.c1.莫斯科 一个名字为莫斯科，引用为c1，队伍为0的城市。

  a.mg.fi20 一个受fi20的振荡器控制的，刷新小机甲的刷兵点。

  还有很多...

您可以对比"宾语自动化例子"里右边的各项标记宾语和其产生的结果，选择如何使用这些自动化模式。

## 地图示例格式

地图触发层宾语分为行和列进行处理。每一行都声明了一种宾语自动化格式。同一列只能放置同一种info或者放置标记宾语。当不同行发生共用info宾语时，该行对应列写明行号(mapText)，表明要用的info宾语的行号。第一行第一列有序号。第二列有该行自动化格式的名称。mapText名称简单介绍作用和参数。第二行有该info的名称，或者该列的意义。列号会有重合，需要进一步明确宾语类型。分为i(info宾语)/控（控制台标记宾语，不可操作）/附（附属标记宾语，可操作）/标（标记宾语，实际效果）。因此"i/控/附/标(行号, 列号)"是该info或标记宾语的坐标。

请将所有info复制下来放入地图，这样可以使用所有自动化模式。info宾语并不会追求简洁，将尽力将所有可能的城夺自动化情况纳入考虑，主要用于实际使用。下文并不会详细解释这些info的原理，仅介绍用法和可能修改的必要参数。想要了解原理请阅读[引导教程](https://github.com/exgcdwu/Rusted-Warfare-map-editor-for-city-occupation-play-/blob/main/command/auto/readme/auto_guide.md)。如果想对参数进行细致修改，请查找[参数说明](https://github.com/exgcdwu/Rusted-Warfare-map-editor-for-city-occupation-play-/blob/main/command/auto/readme/auto_tutorial.md)。

想要获得实际地图，必须添加-c选项。建议添加-D -di选项。

本示例基本用于两队游玩，混战需要修改。

## 万能速查

塔防t(前缀后无'.'，必填参数:建筑的初始队伍，选填参数:,i建筑初始刷新，默认0s，,r建筑刷新速度，默认20s，,u城市单位，默认为炮塔，,t塔防持续刷新队伍，默认为-1，,o使用unitType而不是onlyBuildings检测，,B建筑刷新括号内容，默认""(要求i小于r，时间必须以s为单位)

周期振荡器fd(前缀后有'.'，必填参数:振荡器引用，初始振荡时间，周期振荡时间。)\[用于刷兵和附属建筑刷新\]

单次振荡器fi(前缀后有'.'，必填参数:振荡器引用，初始振荡时间。)\[用于刷兵和附属建筑刷新\]

方波器si(前缀后有'.'，必填参数:振荡器引用，开始抑制时间，选填参数:,a开始抑制，默认之后抑制)\[用于刷兵\]

附属建筑b(前缀后无'.'，必填参数:附属建筑队伍，依附城市；可选参数：,u建筑单位，默认为虫塔，,n城市中立时也刷新，,f选用特别的flash引用(fd/fi)，应与,w匹配，,w 附属建筑一次性，,y不受依附城市控制，,o使用onlyBuildings而不是unitType检测)，,B附属建筑刷新括号内容，默认""

万能城市c(前缀后无'.'，必填参数:城市初始队伍，城市队伍检测引用，城市名称，选填参数:,i建筑初始刷新，默认0s，,r建筑刷新时间，默认20s，,u城市单位，默认为补给站，,t塔防持续刷新队伍，默认为-1，,s文本大小，默认为7，,e队伍检测刷新时间，默认1s，,c启用多个城市颜色，,x启用多个城市颜色，A队的文本(可以没有)，v启用多个城市颜色，B队的文本(可以没有)，,g是否有城防，,f城防刷新的f_cite，,n城防中立时是否刷新，,o是否启动onlyBuildings检测，,h城防的单位，默认为虫塔，,w城防一次性，,m不再添加队伍检测（除虫塔外功能丢失），,y城防是否被抑制，,b设定城防的初始玩家)，,B城市刷新括号内容，默认"(techLevel=2)"，,A城防刷新括号内容，默认""(要求i小于r，时间必须以s为单位)

城市检测可视化ic(前缀后有'.'，必填参数:城市引用。)

万能刷兵a(前缀后有'.'，必填参数:刷兵单位（在d中），控制振荡器；可选参数：,t刷新队伍，默认-1，,c城市（要有队伍检测），,p什么阵营占领该城市会刷新，,w兵力从哪个城市撤退。要么cpw参数都没有，要么只有cp参数，要么cpw参数都有。，,n城市中立时也刷新单位（并且不撤退）)，,m允许双方均在此刷兵（,m成立时，(,pw)自动失效。并且(,uvabef)才能生效），,u允许双方均刷兵时，a队刷兵，,v允许双方均刷兵时，b队刷兵，,a 允许双方均刷兵时，a队刷兵队伍，,b 允许双方均刷兵时，b队刷兵队伍，,e 允许双方均刷兵时，a队刷兵前线撤离城市，,f 允许双方均刷兵时，b队刷兵前线撤离城市，,s文本显示大小，,j是否使用emoji，,h是否使用符号，,i改变默认字符集，默认为dh(使用emoji并且,m成立时不能改变，emoji字符集为dj)，,k 方波器检测抑制。

## 塔防t

生成一个没有文本的建筑。

塔防t(前缀后无'.'，必填参数:建筑的初始队伍，选填参数:,i建筑初始刷新，默认0s，,r建筑刷新速度，默认20s，,u城市单位，默认为炮塔，,t塔防持续刷新队伍，默认为-1，,o使用unitType而不是onlyBuildings检测(要求i小于r，时间必须以s为单位)，,B 建筑刷新括号内容，默认""

### 必填参数-塔防建筑

  建筑的初始队伍(team)

### 选填参数-塔防建筑

  ",i": 建筑初始刷新，默认0s。

  ",r": 建筑刷新速度，默认20s。要求i <= r。

  ",u": 建筑单位类型，默认为炮塔。还可以添加其他建筑单位，比如su(supplyDepot补给站)等，具体可以在dictionary_info_dd参数里面查看简化情况。

  ",t": 建筑刷新队伍，默认-1.

  ",o": 是否改变默认的isonlybuilding 选项。isonlybuilding开启时，使用onlyBuildings检测单位，而不是使用unitType。

  ",B": 建筑刷新括号内容，默认""。如果是补给站应当设置为"tl2"（在d中引用）。
  
### info中可改变的参数-塔防建筑

  info : "dictionary_info_dd" [i(1, 3)]

  su : "supplyDepot" // 简化补给站翻译

  bt : "bugTurret" // 简化虫塔翻译

  tu : "turret" // 简化炮塔翻译

  ...可以添加更多建筑翻译供,u使用。之后所有单位都需要从dictionary_info_dd中获取。

  info : "building_info_t" [i(1, 6)]

  aunit_now : "turret" // 默认单位类型，可修改成其他建筑，示例中默认为炮塔。

  reset : "20s" // 默认建筑刷新速度

  inaddwarmup : "0s" // 建筑初始刷新时间，应当小于reset_now

  team : "-1" // 默认建筑刷新队伍

  isonlybuilding : "true" // 如果该建筑可升级，必须使该项为true，但建筑不得重叠。如果该建筑不可升级，则应当使该项为false。

  aunitbrace_now : "" // 建筑刷新括号内容，默认""。如果是补给站应当设置为"(techLevel=2)"。

## 周期振荡器fd

用于刷兵和附属建筑刷新。

周期振荡器fd(前缀后有'.'，必填参数:振荡器引用，初始振荡时间，周期振荡时间。)

### 必填参数-周期振荡器

  周期振荡器的引用(cite_name)

  周期振荡器的初始振荡时间(init)

  周期振荡器的周期振荡时间(period)

## 单次振荡器fi

用于刷兵和附属建筑刷新。

单次振荡器fi(前缀后有'.'，必填参数:振荡器引用，初始振荡时间。)

### 必填参数-单次振荡器

  单次振荡器的引用(cite_name)

  单次振荡器的初始振荡时间(init)

## 方波器si

用于刷兵和附属建筑刷新。

方波器si(前缀后有'.'，必填参数:振荡器引用，开始抑制时间，选填参数:,a开始抑制，默认之后抑制)

### 必填参数-方波器

  方波器的引用(cite_name)

  方波器的初始振荡时间(step)

### 选填参数-方波器

  ",a": 是否改变默认的isactiend 选项。isactiend启用时，方波器在step时间前不激活，step时间后激活。否则在step时间前激活，step时间后不激活。

### info中可改变的参数-方波器

  info : "building_info_b" [i(9, 13)]

  isactiend : "true" // isactiend启用时，方波器在step时间前不激活，step时间后激活。否则在step时间前激活，step时间后不激活。

## 附属建筑b

生成一个依附于城市的建筑。

附属建筑b(前缀后无'.'，必填参数:附属建筑队伍，依附城市；可选参数：,u建筑单位，默认为虫塔，,n城市中立时也刷新，,f选用特别的flash引用(fd/fi)，应与,w匹配，,w 附属建筑一次性，,y不受依附城市控制，,o使用onlyBuildings而不是unitType检测)，,B 附属建筑刷新括号内容，默认""

### 必填参数-附属建筑

  附属建筑的所属队伍(team)

  附属建筑所依附的城市(ctd_cite)

### 选填参数-附属建筑

  ",u": 建筑单位类型，默认为虫塔。还可以添加其他建筑单位，比如su(supplyDepot补给站)等，具体可以在dictionary_info_dd 参数里面查看简化情况。

  ",n": 是否改变默认的isneutralspawn 选项。isneutralspawn开启时，附属建筑在依附城市中立或不存在时也会刷新。

  ",w": 是否改变默认的isbugdisposable 选项。isbugdisposable开启时，附属建筑是重复刷新的，将会启用"fd6_3"(初始6s，每3s刷新一次)，否则启动"fi6"(初始6s后不再刷新)。

  ",f": 使用其他非默认的flash标记刷新附属建筑。如果为fd系列的flash_info，请确保isbugdisposable 开启。如果是fi系列的flash_info，请确保isbugdisposable 关闭。

  ",o": 是否改变默认的isonlybuilding 选项。isonlybuilding开启时，使用onlyBuildings检测单位，而不是使用unitType。

  ",y": 是否改变默认的isbugTurretdeacti 选项。isbugTurretdeacti关闭时，附属建筑不再依附。（持续刷新，不受控制）。

  ",B": 建筑刷新括号内容，默认""。如果是补给站应当设置为"tl2"（在d中引用）。
  
### info中可改变的参数-附属建筑

  info : "building_info_b" [i(4, 6)]

  aunit_now : "bugTurret" // 默认单位类型，可修改成其他建筑，示例中默认为虫塔。

  isonlybuilding : "false" // 城市是塔，城市不重叠，也没有城防时，可以用isonlybuilding。

  isbugTurretdeacti : "true" // isbugTurretdeacti关闭时，附属建筑不再依附。（持续刷新，不受控制）。

  isneutralspawn : "true" // isneutralspawn开启时，附属建筑在依附城市中立或不存在时也会刷新。

  isbugdisposable : "true" // isbugdisposable开启时，附属建筑是重复刷新的，将会启用"fd6_3"(初始6s，每3s刷新一次)，否则启动"fi6"(初始6s后不再刷新)。

  fd_cite : "fd6_3" // 已部署的flash_info_fd标记，表明该建筑默认下开局6s刷新，3s再刷新一次(isbugdisposable 开启)

  fi_cite : "fd6_3" // 已部署的flash_info_fi标记，表明该建筑默认下仅开局6s刷新(isbugdisposable 关闭)

  aunitbrace_now : "" // 建筑刷新括号内容，默认""。如果是补给站应当设置为"(techLevel=2)"。

## 城市检测可视化ic

会产生敌对高射炮，表示城市的归属。可用于胜负检测。在当前位置生成高射炮时，表示城市归属为a队，下方40长度下生成高射炮，表示城市归属b队。

城市检测可视化ic(前缀后有'.'，必填参数:城市引用。)

### 必填参数-城市检测可视化

  城市引用(ctd_cite)

### info中可改变的参数-城市检测可视化

  info : "idcheck_info_zic" [i(13, 14)]

  ismtext : "true" // 城市检测可视化是否有文本显示

  mtextsize : "7" // 城市检测可视化文本大小

  color : "#FF7700 #191970" // 城市检测可视化文本a, b队的颜色。可以参照info : "multiText_info_zmt" [i(5, 9)]。

## 万能城市c

生成一个城市，可以有不同功能。

万能城市c(前缀后无'.'，必填参数:城市初始队伍，城市队伍检测引用，城市名称，选填参数:,i建筑初始刷新，默认0s，,r建筑刷新时间，默认20s，,u城市单位，默认为补给站，,t塔防持续刷新队伍，默认为-1，,s文本大小，默认为7，,e队伍检测刷新时间，默认1s，,c启用多个城市颜色，,x启用多个城市颜色，A队的文本(可以没有)，v启用多个城市颜色，B队的文本(可以没有)，,g是否有城防，,f城防刷新的f_cite，,n城防中立时是否刷新，,o是否启动onlyBuildings检测，,h城防的单位，默认为虫塔，,w城防一次性，,m不再添加队伍检测（除虫塔外功能丢失），,y城防是否被抑制，,b设定城防的初始玩家)(要求i小于r，时间必须以s为单位)，,B 城市刷新括号内容，默认"(techLevel=2)"，,A 城防刷新括号内容，默认""

### 必填参数-万能城市

  城市的初始队伍(inaddteam)

  城市引用(cite_name)

  城市名称(cityname)

### 选填参数-万能城市

  ",i": 城市初始刷新时间，默认为0s。

  ",r": 城市刷新时间，默认为20s。

  ",u": 城市单位类型，默认为补给站。

  ",t": 城市持续刷新队伍，默认为-1。

  ",o": 是否改变默认的isonlybuilding 选项。isonlybuilding成立，使用onlyBuildings检测单位，而不是使用unitType。

  ",s": 城市文本大小，默认为7。

  ",m": 改变默认的isteamdetect选项。isteamdetect成立，队伍检测产生，可以外部引用，并且所有功能开启。否则仅能产生基础城市(,irutos)和不受控制的城防(,gwfb)(等同于,y启动)

  ",e": isteamdetect成立时，城市队伍检测刷新时间，默认为1s。

  ",c": isteamdetect成立时，改变默认的ismultiText选项。ismultiText成立时，将出现多个文本的城市。

  ",x": ismultiText成立时，A队的文本，默认为城市名称

  ",v": ismultiText成立时，B队的文本，默认为城市名称

  ",g": 是否改变默认的isbugTurret 选项。成立将在城市生成城防，",nwfyhb"才有意义。

  ",n": isbugTurret成立时，导入附属建筑,n选项。

  ",w": isbugTurret成立时，导入附属建筑,w选项。

  ",f": isbugTurret成立时，导入附属建筑,f选项。

  ",y": isbugTurret成立时，导入附属建筑,y选项。

  ",h": isbugTurret成立时，导入附属建筑,u选项。

  ",b": isbugTurret成立时，导入附属建筑刷新队伍必填参数，默认为城市的初始队伍。

  ",B": 城市刷新括号内容，默认"tl2"。

  ",A": 城防刷新括号内容，默认""。
  
### info中可改变的参数-万能城市

  附属建筑的相关改变（building_info_b）。

  info : "building_info_ztu" [i(6, 6)]

  aunit_now : "supplyDepot" // 万能城市默认刷新单位。

  aunitbrace_now : "(techLevel=2)" // 城市刷新括号内容。当设为"None"时，相当于""。

  inaddwarmup : "0s" // 城市初始刷新时间

  reset : "20s" // 城市持续刷新周期

  team : "-1" // 城市持续刷新队伍

  info : "teamDetect_info_ztdo" [i(3, 7)]

  reset : "1s" // 队伍检测刷新时间

  setTeam : "0 2 4,6 8,1 3 5 7 9,-3 -2 -1" // 检测队伍分组，-3指检测没有单位

  setidTeam : "Ac,A1c;Ac,A2c;Bc;Nc" // 不同组第一个id前缀相同，则属于同一个阵营。后面的id不同可有其他用途，比如文本。

  ";"和","分割了setidTeam。将其排列开来是这样的。

  |i \ j| 队伍 | 0 | 1 |
  |------|------|------|------|
  | 0 |0 2 4| Ac | A1c |
  | 1 |6 8| Ac | A2c |
  | 2 |1 3 5 7 9| Bc ||
  | 3 |-3 -2 -1| Nc ||

  a : "{setidTeam0_0_0}" // **Ac**,A1c;**Ac**,A2c;Bc;Nc("{setidTeam1_0_0}" 也行)

  a1 : "{setidTeam0_1_0}" // Ac,**A1c**;Ac,A2c;Bc;Nc

  a2 : "{setidTeam1_1_0}" // Ac,A1c;Ac,**A2c**;Bc;Nc

  b : "{setidTeam2_0_0}" // Ac,A1c;Ac,A2c;**Bc**;Nc

  n : "{setidTeam3_0_0}" // Ac,A1c;Ac,A2c;Bc;**Nc**

  brace : "a,b,n,a1,a2" // 这些将会被用于引用。

  // 这样设置是为了保证刷兵根据Ac,Bc,Nc阵营决定，但是城市颜色/刷兵颜色根据A1c,A2c,Bc,Nc决定。

  info : "tree_info_c" [i(6, 1)]

  mtextsize : "7" // 城市文本大小

  offset : "0 0,0 0,0 0,0 0,1 1" // 1 1会让城防隐藏。如果想要将城防暴露。1 1可以换为-1 -1。

  isbugTurret : "false" // isbugTurret开启时，默认出现城防。

  isteamdetect : "true" // isteamdetect开启时，默认出现队伍检测。否则不出现队伍检测，并且ismultiText将自动认为是false。

  ismultiText : "false" // ismultiText开启时，默认出现多个城名（不同颜色）。

  isonlybuilding : "false" // 城市是塔，城市不重叠，也没有城防时，可以用isonlybuilding。

  defence_aunitbrace : "None" // 城防刷新括号内容。"None"表示没有。

  a : "{idprefix0_0}.a"

  a1 : "{idprefix0_0}.a1"

  a2 : "{idprefix0_0}.a2"

  b : "{idprefix0_0}.b"

  n : "{idprefix0_0}.n"

  brace : "a,b,n,a1,a2" // 以上引用都是从teamDetect_info_ztdo队伍检测中获取的。

  info : "multiText_info_zmt" [i(5, 9)]

  acti : "{td_cite}.a1;{td_cite}.a2;{td_cite}.b;{td_cite}.n" // 来自teamDetect_info_ztdo的检测

  color : "#FFDD00,#FF2200,#191970,#FFFFFF" // 所有颜色

  text : "{text_a},{text_a},{text_b},{text_m}" // 对应阵营的文本

  // 三项的项数是一样的。所有multiText的这三项均是一样的，可以一起修改。包括 info : "multiText_info_zamt" [i(9, 9, 1)], info : "multiText_info_zamj" [i(9, 9, 2)], info : "multiText_info_zamf" [i(9, 9, 3)]。

## 万能刷兵a

生成一个刷兵点，可以有不同功能。

万能刷兵a(前缀后有'.'，必填参数:刷兵单位（在d中），控制振荡器；可选参数：,t刷新队伍，默认-1，,c城市（要有队伍检测），,p什么阵营占领该城市会刷新，,w兵力从哪个城市撤退。要么cpw参数都没有，要么只有cp参数，要么cpw参数都有。，,n城市中立时也刷新单位（并且不撤退）)，,m允许双方均在此刷兵（,m成立时，(,pw)自动失效。并且(,uvabef)才能生效），,u允许双方均刷兵时，a队刷兵，,v允许双方均刷兵时，b队刷兵，,a 允许双方均刷兵时，a队刷兵队伍，,b 允许双方均刷兵时，b队刷兵队伍，,e 允许双方均刷兵时，a队刷兵前线撤离城市，,f 允许双方均刷兵时，b队刷兵前线撤离城市，,s文本显示大小，,j是否使用emoji，,h是否使用符号，,i改变默认字符集，默认为dh(使用emoji并且,m成立时不能改变，emoji字符集为dj)，,k 方波器检测抑制。

### 必填参数-万能刷兵

  刷兵单位(dunit_op_n)，在dictionary_info_dd中有映射

  控制振荡器(f_cite)

### 选填参数-万能刷兵

  ",t": // 刷新队伍，默认"-1"。

  ",c": // 刷兵点受控城市引用。ismultiAdd未启动时，必须与",p"连用。受控城市队伍检测必须有。

  ",p": // ",c"启用，ismultiAdd未启用时，刷兵点阵营。必须是"a"或"b"，代表A队或B队。受控城市必须被该阵营占领时才启用。

  ",w": // ",c"启用，ismultiAdd未启用时，刷兵点撤退城市引用。撤退城市被敌方占领后刷兵点才能启用。

  ",n" // 是否改变默认的isneutralspawn 选项。isneutralspawn启用时，城市中立时刷兵点也启用，并且撤退城市中立不撤退。

  ",m" // 是否改变默认的ismultiAdd 选项。ismultiAdd启用时，双方占领受控城市均可刷兵，",pw"失效，",uvabef"生效。否则，",pw"生效，",uvabef"失效。

  ",u" // ",c"，ismultiAdd启用时，a队刷兵，默认为必填的刷兵。

  ",v" // ",c"，ismultiAdd启用时，b队刷兵，默认为必填的刷兵。

  ",a" // ",c"，ismultiAdd启用时，a队刷兵队伍，默认为"-1"。

  ",b" // ",c"，ismultiAdd启用时，b队刷兵队伍，默认为"-1"。

  ",e" // ",c"，ismultiAdd启用时，a队撤退城市引用，默认没有。a队刷兵必须在受控城市在己方手里、撤退城市被敌方占领后（如果有）才能启用。

  ",f" // ",c"，ismultiAdd启用时，b队撤退城市引用，默认没有。b队刷兵必须在受控城市在己方手里、撤退城市被敌方占领后（如果有）才能启用。

  ",h" // 是否改变默认的ischaracter 选项。ischaracter启用时，刷兵点上出现文本。

  ",j" // 是否改变默认的isemoji 选项。isemoji启用时，刷兵点上出现emoji。当isemoji选项和ischaracter选项同时启用时，会优先使用ischaracter。

  ",s" // ischaracter 或 isemoji 选项启用，刷兵点文本的大小，默认为"8"。

  ",i" // 改变默认字符集。默认为dh(isemoji启用 且 ismultiAdd 未启用时，默认字符集为dj；isemoji 启用 且 ismultiAdd 启用时，该项无效)

  ",k" // 方波器抑制标记，默认没有。

### info中可改变的参数-万能刷兵

  info : "tree_info_a" [i(9, 1)]

  ischaracter : "true" // ischaracter启用时，刷兵点上出现文本。

  isemoji : "false" // isemoji启用时，刷兵点上出现emoji。

  ismultiAdd : "false" // ismultiAdd启用时，双方占领受控城市均可刷兵，",pw"失效，",uvabef"生效。否则，",pw"生效，",uvabef"失效。

  isneutralspawn : "false" // isneutralspawn启用时，城市中立时刷兵点也启用，并且撤退城市中立不撤退。

  default_dict_cite_character : "dh" // 文本默认字典

  default_dict_cite_emoji : "dj" // emoji默认字典

  info : "multiText_info_zamt" [i(9, 9, 1)]

  info : "multiText_info_zamj" [i(9, 9, 2)]

  info : "multiText_info_zamf" [i(9, 9, 3)]

  三个info都要修改一套如下参数

  acti : "{td_cite}.a1;{td_cite}.a2;{td_cite}.b;{td_cite}.n" // 和"multiText_info_zmt" [i(5, 9)] acti 一致

  color : "#FFDD00,#FF2200,#191970,#FFFFFF" // 和"multiText_info_zmt" [i(5, 9)] color 一致

  text : "{text_a},{text_a},{text_b},{text_m}" // 和"multiText_info_zmt" [i(5, 9)] text 一致

  info : dictionary_info_ddj" [i(9, 3, 1)]

  emoji刷兵映射，注意"a","b","n"为不同阵营背景。为isemoji启用字符集。

  info : dictionary_info_ddf" [i(9, 3, 3)]

  特殊字符映射。

  info : dictionary_info_ddc" [i(9, 3, 4)]

  英文字符映射。

  info : dictionary_info_ddl" [i(9, 3, 5)]

  英文花体字符映射。

  info : dictionary_info_ddh" [i(9, 3, 6)]

  英文印刷体字符映射。

## 注意事项

### 标记宾语顺序

所有字典标记、flash标记、step标记必须手动放到文件开头。

城市等需要引用的标记需要在其他引用城市标记宾语的前面。

### team

-2为敌对，-1为中立，玩家从0开始，0代表1号玩家。

### 时间

所有时间必须以s为单位。

所有时间必须大于等于0s。
