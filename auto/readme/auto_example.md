# 宾语自动化示例说明

- [宾语自动化示例说明](#宾语自动化示例说明)
  - [目标](#目标)
  - [地图示例格式](#地图示例格式)
  - [万能速查](#万能速查)
  - [1.塔防建筑，无文本](#1塔防建筑无文本)
    - [所需info和标记-塔防建筑](#所需info和标记-塔防建筑)
    - [前缀-塔防建筑](#前缀-塔防建筑)
    - [必填参数-塔防建筑](#必填参数-塔防建筑)
    - [选填参数-塔防建筑](#选填参数-塔防建筑)
    - [info中可改变的参数-塔防建筑](#info中可改变的参数-塔防建筑)
    - [示例-塔防建筑](#示例-塔防建筑)
  - [2.城市建筑，有文本](#2城市建筑有文本)
    - [所需info和标记-城市建筑](#所需info和标记-城市建筑)
    - [前缀-城市建筑](#前缀-城市建筑)
    - [必填参数-城市建筑](#必填参数-城市建筑)
    - [选填参数-城市建筑](#选填参数-城市建筑)
    - [info中可改变的参数-城市建筑](#info中可改变的参数-城市建筑)
    - [示例-城市建筑](#示例-城市建筑)
  - [3.城市建筑，有队伍检测，有文本](#3城市建筑有队伍检测有文本)
    - [所需info和标记-城市队伍](#所需info和标记-城市队伍)
    - [前缀-城市队伍](#前缀-城市队伍)
    - [必填参数-城市队伍](#必填参数-城市队伍)
    - [选填参数-城市队伍](#选填参数-城市队伍)
    - [info中可改变的参数-城市队伍](#info中可改变的参数-城市队伍)
    - [示例-城市队伍](#示例-城市队伍)
  - [4.附属建筑](#4附属建筑)
    - [所需info和标记-附属建筑](#所需info和标记-附属建筑)
    - [前缀-附属建筑](#前缀-附属建筑)
    - [必填参数-附属建筑](#必填参数-附属建筑)
    - [选填参数-附属建筑](#选填参数-附属建筑)
    - [info中可改变的参数-附属建筑](#info中可改变的参数-附属建筑)
    - [示例-附属建筑](#示例-附属建筑)
  - [5.多文本城市](#5多文本城市)
    - [所需info和标记-多文本城市](#所需info和标记-多文本城市)
    - [前缀-多文本城市](#前缀-多文本城市)
    - [必填参数-多文本城市](#必填参数-多文本城市)
    - [选填参数-多文本城市](#选填参数-多文本城市)
    - [info中可改变的参数-多文本城市](#info中可改变的参数-多文本城市)
    - [示例-多文本城市](#示例-多文本城市)
  - [注意事项](#注意事项)
    - [team](#team)
    - [时间](#时间)

## 目标

提供可在地图中直接复制粘贴的info宾语及其用法，为[宾语自动化地图示例](https://github.com/exgcdwu/Rusted-Warfare-map-editor-for-city-occupation-play-/blob/main/auto/example/auto_example.tmx)提供注释。

如果想学习宾语自动化，请阅读[宾语自动化引导教程](https://github.com/exgcdwu/Rusted-Warfare-map-editor-for-city-occupation-play-/blob/main/auto/readme/auto_guide.md)。

如果想阅读宾语自动化的所有具体参数和详细注意事项，请阅读[宾语自动化参数说明](https://github.com/exgcdwu/Rusted-Warfare-map-editor-for-city-occupation-play-/blob/main/auto/readme/auto_tutorial.md)。

## 地图示例格式

地图触发层宾语分为行和列进行处理。每一行都声明了一种宾语自动化格式。同一列只能放置同一种info或者放置标记宾语。当不同行发生共用info宾语时，该行对应列写明行号(mapText)，表明要用的info宾语的行号。第一行第一列有序号。第二列有该行自动化格式的名称。mapText名称简单介绍作用和参数。第二行有该info的名称，或者该列的意义。列号会有重合，需要进一步明确宾语类型。分为i(info宾语)/控（控制台标记宾语，不可操作）/附（附属标记宾语，可操作）/标（标记宾语，实际效果）。因此"i/控/附/标(行号, 列号)"是该info或标记宾语的坐标。

如果想将某一行的info导入，请导入所有该行的info，并将该行对应列表明序号的对应行的info一并复制（如果对应info有多个，可以有第三个坐标表示取走第几个）。可以将所有info复制下来放入地图，这样可以使用所有自动化模式。info宾语并不会追求简洁，将尽力将所有可能的城夺自动化情况纳入考虑，主要用于实际使用。下文并不会详细解释这些info的原理，仅介绍用法和可能修改的必要参数。想要了解原理请阅读[引导教程](https://github.com/exgcdwu/Rusted-Warfare-map-editor-for-city-occupation-play-/blob/main/auto/readme/auto_guide.md)。如果想对参数进行细致修改，请查找[参数说明](https://github.com/exgcdwu/Rusted-Warfare-map-editor-for-city-occupation-play-/blob/main/auto/readme/auto_tutorial.md)。

想要获得实际地图，必须添加-c选项。建议添加-D选项。

## 万能速查

塔防t(必填参数:建筑的初始队伍，选填参数:,i建筑初始刷新，默认0s，,r建筑刷新速度，默认20s，,c文本颜色，默认white，,s文本大小，默认为7)(要求i小于r，时间必须以s为单位)

万能城市c(必填参数:城市初始队伍，城市队伍检测引用，城市名称，选填参数:,i建筑初始刷新，默认0s，,r建筑刷新时间，默认20s，,u城市单位，默认为补给站，,s文本大小，默认为7，,e队伍检测刷新时间，默认1s，,c启用多个城市颜色，,x启用多个城市颜色，A队的文本(可以没有)，v启用多个城市颜色，B队的文本(可以没有)，,g是否有城防，,f城防刷新的f_cite，,n城防中立时是否刷新，,o是否启动onlyBuildings检测，,h城防的单位，默认为虫塔，,w城防一次性，,m不再添加队伍检测（除虫塔外功能丢失），,y城防是否被抑制，,b设定城防的初始玩家)(要求i小于r，时间必须以s为单位)

万能刷兵a(必填参数:刷兵单位（在dictionary中），控制振荡器；可选参数：,t刷新队伍，默认-1；，,c城市（要有队伍检测），,s什么阵营占领该城市会刷新，,w兵力从哪个城市撤退。要么csw参数都没有，要么只有cs参数，要么csw参数都有。，,n城市中立时也刷新单位（并且不撤退）)

附属建筑b(必填参数:附属建筑队伍，依附城市；可选参数：,u建筑单位，默认为虫塔，,n城市中立时也刷新，,f选用特别的flash引用(fd/fi)，应与,w匹配，,w 附属建筑一次性，,y不受依附城市控制)

## 1.塔防建筑，无文本

### 所需info和标记-塔防建筑

  info: "dictionary_info_d" [i(1, 3)]
  info: "building_info_t" [i(1, 6)]
  标记: "d.d" [控(1, 1)]

### 前缀-塔防建筑

  "t"

### 必填参数-塔防建筑

  建筑的初始队伍(team)

### 选填参数-塔防建筑

  ",i": 建筑初始刷新，默认0s。

  ",r": 建筑刷新速度，默认20s。要求i <= r。

  ",u": 建筑单位类型，默认为炮塔。还可以添加其他建筑单位，比如su(supplyDepot补给站)等，具体可以在dictionary_info_d 参数里面查看简化情况。

  ",t": 建筑刷新队伍，默认-1.

  ",o": 是否改变默认的isonlybuilding 选项。isonlybuilding开启时，使用onlyBuildings检测单位，而不是使用unitType。
  
### info中可改变的参数-塔防建筑

  info : "dictionary_info_d" [i(1, 3)]

    su : "supplyDepot" // 简化补给站翻译

    bt : "bugTurret" // 简化虫塔翻译

    tu : "turret" // 简化炮塔翻译

    ...可以添加更多建筑翻译供,u使用。

  info : "building_info_t" [i(1, 6)]

    aunit_now : "turret" // 默认单位类型，可修改成其他建筑，示例中默认为炮塔。

    reset : "20s" // 默认建筑刷新速度

    inaddwarmup : "0s" // 建筑初始刷新时间，应当小于reset_now

    team : "-1" // 默认建筑刷新队伍

    isonlybuilding : "true" // 如果该建筑可升级，必须使该项为true，但建筑不得重叠。如果该建筑不可升级，则应当使该项为false。

### 示例-塔防建筑

  标记 : "t-2" [标(1, 1)] // 初始敌对建筑

  标记 : "t-1" [标(1, 2)] // 初始中立建筑

  标记 : "t0,r1s" [标(1, 3)] // 初始玩家1，刷新速度为1s

  标记 : "t0,i10s" [标(1, 4)] // 初始玩家1，初始刷新10s

  标记 : "t0,i20s" [标(1, 5)] // 初始玩家1，初始刷新20s

  标记 : "t0,usu,o" [标(1, 6)] // 初始玩家1，单位为补给站(supplyDepot)，转换为unitType检测

  标记 : "t0,ubt,o" [标(1, 7)] // 初始玩家1，单位为虫塔(bugTurret)，转换为unitType检测

  标记 : "t0,t0" [标(1, 8)] // 初始玩家1，刷新玩家也为1(必然给1刷新)。

  标记 : "t1,t1" [标(1, 9)] // 初始玩家2，刷新玩家也为2(必然给2刷新)。

## 2.城市建筑，有文本

### 所需info和标记-城市建筑

  info: "dictionary_info_d" [i(1, 3)]
  info: "building_info_zci" [i(2, 6)]
  标记: "d.d" [控(1, 1)]

### 前缀-城市建筑

  "zci"

### 必填参数-城市建筑

  城市的初始队伍(team)

  城市名称(cityname)

### 选填参数-城市建筑

  ",i": 建筑初始刷新，默认0s。

  ",r": 建筑刷新速度，默认20s。要求i <= r。

  ",u": 建筑单位类型，默认为炮塔。还可以添加其他建筑单位，比如su(supplyDepot补给站)等，具体可以在dictionary_info_d 参数里面查看简化情况。

  ",t": 建筑刷新队伍，默认-1。

  ",c": 城市文本颜色，默认white。

  ",s": 城市文本大小，默认7。

  ",o": 是否改变默认的isonlybuilding 选项。isonlybuilding开启时，使用onlyBuildings检测单位，而不是使用unitType。
  
### info中可改变的参数-城市建筑

  info : "dictionary_info_d" [i(1, 3)]

    su : "supplyDepot" // 简化补给站翻译

    bt : "bugTurret" // 简化虫塔翻译

    tu : "turret" // 简化炮塔翻译

    ...可以添加更多建筑翻译供,u使用。

  info : "building_info_zci" [i(1, 6)]

    aunit_now : "supplyDepot" // 默认单位类型，可修改成其他建筑，示例中默认为炮塔。

    reset : "20s" // 默认建筑刷新速度

    inaddwarmup : "0s" // 建筑初始刷新时间，应当小于reset_now

    team : "-1" // 默认建筑刷新队伍

    mcolor : "white" // 默认城市名称颜色

    mtextsize : "7" // 默认城市名称大小

    isonlybuilding : "false" // 如果该建筑可升级，必须使该项为true，但建筑不得重叠。如果该建筑不可升级，则应当使该项为false。

### 示例-城市建筑

  标记 : "zci-2.城1" [标(2, 1)] // 初始敌对城市

  标记 : "zci-1.城2" [标(2, 2)] // 初始中立城市

  标记 : "zci0.城3,r1s" [标(2, 3)] // 初始玩家1，刷新速度为1s

  标记 : "zci0.城4,i10s" [标(2, 4)] // 初始玩家1，初始刷新10s

  标记 : "zci0.城5,i20s" [标(2, 5)] // 初始玩家1，初始刷新20s

  标记 : "zci0.城6,utu,o" [标(2, 6)] // 初始玩家1，单位为炮塔(turret)，转换为使用onlyBuildings检测。

  标记 : "zci0.城7,ubt" [标(2, 7)] // 初始玩家1，单位为虫塔(bugTurret)

  标记 : "zci0.城8,t0" [标(2, 8)] // 初始玩家1，刷新玩家也为1(必然给1刷新)。

  标记 : "zci1.城9,t1" [标(2, 9)] // 初始玩家2，刷新玩家也为2(必然给2刷新)。

  标记 : "zci0.城10,cred" [标(2, 10)] // 初始玩家1，城市颜色红色。

  标记 : "zci0.城11,s12" [标(2, 11)] // 初始玩家1，城市文本大小为12。

## 3.城市建筑，有队伍检测，有文本

### 所需info和标记-城市队伍

  info: "dictionary_info_d" [i(1, 3)]
  info: "building_info_zci" [i(2, 6)]
  info: "teamDetect_info_ztdo" [i(3, 7)]
  info: "tree_info_zcto" [i(3, 1)]
  标记: "d.d" [控(1, 1)]

### 前缀-城市队伍

  "zcto"

### 必填参数-城市队伍

  城市的初始队伍(team)

  城市引用(cite_name)

  城市名称(cityname)

### 选填参数-城市队伍

  ",i": 建筑初始刷新，默认0s。

  ",r": 建筑刷新速度，默认20s。要求i <= r。

  ",u": 建筑单位类型，默认为炮塔。还可以添加其他建筑单位，比如su(supplyDepot补给站)等，具体可以在dictionary_info_d 参数里面查看简化情况。

  ",t": 建筑刷新队伍，默认-1。

  ",c": 城市文本颜色，默认white。

  ",s": 城市文本大小，默认7。

  ",e": 城市队伍检测刷新时间，默认1s。

  ",o": 是否改变默认的isonlybuilding 选项。isonlybuilding开启时，使用onlyBuildings检测单位，而不是使用unitType。
  
### info中可改变的参数-城市队伍

  info : "dictionary_info_d" [i(1, 3)]

    su : "supplyDepot" // 简化补给站翻译

    bt : "bugTurret" // 简化虫塔翻译

    tu : "turret" // 简化炮塔翻译

    ...可以添加更多建筑翻译供,u使用。

  info : "building_info_ci" [i(1, 6)]

    aunit_now : "supplyDepot" // 默认单位类型，可修改成其他建筑，示例中默认为炮塔。

    reset : "20s" // 默认建筑刷新速度

    inaddwarmup : "0s" // 建筑初始刷新时间，应当小于reset_now

    team : "-1" // 默认建筑刷新队伍

    mcolor : "white" // 默认城市名称颜色

    mtextsize : "7" // 默认城市名称大小

    isonlybuilding : "false" // 如果该建筑可升级，必须使该项为true，但建筑不得重叠。如果该建筑不可升级，则应当使该项为false。

  info : "teamDetect_info_ztdo" [i(3, 8)]

    reset : "1s" // 默认队伍检测刷新时间

    isonlybuilding : "false" // 如果该建筑可升级，必须使该项为true，但建筑不得重叠。如果该建筑不可升级，则应当使该项为false。

    setTeam : "0 2 4 6 8,1 3 5 7 9,-3 -2 -1" // 第一组代表a队，第二组代表b队，第三组(n)代表未被占领(-3是建筑未刷新)

    setidTeam : "Ac,Bc,Nc" // 三个对应检测id前缀，数目与setTeam的组数保持一致

    a : "{setidTeam0_0}" // 得到对应a队id(第一组)，供引用使用

    b : "{setidTeam1_0}" // 得到对应b队id(第二组)，供引用使用

    n : "{setidTeam2_0}" // 得到对应未占领id(第三组)，供引用使用

    brace : "a,b,n" // 队伍检测供外部引用

  info : "tree_info_zcto" [i(3, 1)]

    a : "{idprefix0_0}.a" // 从队伍检测得到对应a队id(第一组)，供引用使用

    b : "{idprefix0_0}.b" // 从队伍检测得到对应b队id(第二组)，供引用使用

    n : "{idprefix0_0}.n" // 从队伍检测得到对应未占领id(第三组)，供引用使用

    brace : "a,b,n" // 城市队伍检测供外部引用

### 示例-城市队伍

  标记 : "zcto-2.zcto城1.城1" [标(3, 1)] // 初始敌对城市

  标记 : "zcto-1.zcto城2.城2" [标(3, 2)] // 初始中立城市

  标记 : "zcto0.zcto城3.城3,r1s" [标(3, 3)] // 初始玩家1，刷新速度为1s

  标记 : "zcto0.zcto城4.城4,i10s" [标(3, 4)] // 初始玩家1，初始刷新10s

  标记 : "zcto0.zcto城5.城5,i20s" [标(3, 5)] // 初始玩家1，初始刷新20s

  标记 : "zcto0.zcto城6.城6,utu,o" [标(3, 6)] // 初始玩家1，单位为炮塔(turret)，转换为使用onlyBuildings检测。

  标记 : "zcto0.zcto城7.城7,ubt" [标(3, 7)] // 初始玩家1，单位为虫塔(bugTurret)

  标记 : "zcto0.zcto城8.城8,t0" [标(3, 8)] // 初始玩家1，刷新玩家也为1(必然给1刷新)。

  标记 : "zcto1.zcto城9.城9,t1" [标(3, 9)] // 初始玩家2，刷新玩家也为2(必然给2刷新)。

  标记 : "zcto0.zcto城10.城10,cred" [标(3, 8)] // 初始玩家1，城市颜色红色。

  标记 : "zcto0.zcto城11.城11,s12" [标(3, 9)] // 初始玩家1，城市文本大小为12。

  标记 : "zcto0.zcto城12.城12,e20s" [标(3, 9)] // 初始玩家1，队伍检测刷新速度为20s。

标记宾语上下有使用引用的mapText。例如"zcto城1.a"引用将会被-c选项翻译为该城被A队占领的检测，"zcto城1.b"为B队占领，
"zcto城1.n"为中立。

## 4.附属建筑

### 所需info和标记-附属建筑

  info: "dictionary_info_d" [i(1, 3)]
  info: "building_info_zci" [i(2, 6)]
  info: "teamDetect_info_ztdo" [i(3, 7)]
  info: "tree_info_zcto" [i(3, 1)]
  info: "flash_info_fd" [i(4, 12, 1)]
  info: "flash_info_fi" [i(4, 12, 2)]
  info: "building_info_b" [i(4, 6)]
  标记: "d.d" [控(1, 1)]
  标记: "fd.fd6_3.12s.6s" [控(4, 2, 1)]
  标记: "fd.fd12_6.12s.6s" [控(4, 2, 2)]
  标记: "fi.fi6.6s" [控(4, 2, 3)]
  标记: "zcto-2.zbt测1.测1" [附(4, 1)]
  标记: "zcto0.zbt测2.测2" [附(4, 2)]
  标记: "zcto3.zbt测3.测3" [附(4, 3)]

### 前缀-附属建筑

  "b"

### 必填参数-附属建筑

  附属建筑的所属队伍(team)

  附属建筑所依附的城市(ctd_cite)

### 选填参数-附属建筑

  ",u": 建筑单位类型，默认为虫塔。还可以添加其他建筑单位，比如su(supplyDepot补给站)等，具体可以在dictionary_info_d 参数里面查看简化情况。

  ",n": 是否改变默认的isneutralspawn 选项。

  ",w": 是否改变默认的isbugdisposable 选项。

  ",f": 使用其他非默认的flash标记刷新附属建筑。如果为fd系列的flash_info，请确保isbugdisposable 开启。如果是fi系列的flash_info，请确保isbugdisposable 关闭。

  ",o": 是否改变默认的isonlybuilding 选项。isonlybuilding开启时，使用onlyBuildings检测单位，而不是使用unitType。

  ",y": 是否改变默认的isbugTurretdeacti 选项。
  
### info中可改变的参数-附属建筑

  info : "dictionary_info_d" [i(1, 3)]

    su : "supplyDepot" // 简化补给站翻译

    bt : "bugTurret" // 简化虫塔翻译

    tu : "turret" // 简化炮塔翻译

    ...可以添加更多建筑翻译供,u使用。

  info : "building_info_b" [i(4, 6)]

    aunit_now : "bugTurret" // 默认单位类型，可修改成其他建筑，示例中默认为虫塔。

    isbugTurretdeacti : "true" // isbugTurretdeacti关闭时，附属建筑不再依附。（持续刷新，不受控制）。

    isneutralspawn : "true" // isneutralspawn开启时，附属建筑在依附城市中立或不存在时也会刷新。

    isbugdisposable : "true" // isbugdisposable开启时，附属建筑是重复刷新的，将会启用"fd6_3"(初始6s，每3s刷新一次)，否则启动"fi6"(初始6s后不再刷新)。

    fd_cite : "fd6_3" // 已部署的flash_info_fd标记，表明该建筑默认下开局6s刷新，3s再刷新一次(isbugdisposable 开启)

    fi_cite : "fd6_3" // 已部署的flash_info_fi标记，表明该建筑默认下仅开局6s刷新(isbugdisposable 关闭)

### 示例-附属建筑

  标记 : "b-2.b测1" [标(4, 1)] // "b测1"中立建筑刷附属建筑，附属建筑为敌对

  标记 : "b-1.b测1" [标(4, 2)] // "b测1"中立建筑刷附属建筑，附属建筑为中立

  标记 : "b0.b测2" [标(4, 3)] // "b测2"A队建筑或中立建筑刷附属建筑，附属建筑为1号

  标记 : "b3.b测3" [标(4, 4)] // "b测3"B队建筑或中立建筑刷附属建筑，附属建筑为4号

  标记 : "b0.b测2,ffd12_6" [标(4, 5)] // "b测2"A队建筑或中立建筑刷附属建筑，附属建筑为1号，刷新改为初始12s，持续6s

  标记 : "b0.b测2,usu" [标(4, 6)] // "b测2"A队建筑或中立建筑刷附属建筑，附属建筑为1号，单位为补给站

  标记 : "b0.b测2,utu,o" [标(4, 7)] // "b测2"A队建筑或中立建筑刷附属建筑，附属建筑为1号，单位为炮塔，转换为使用onlyBuildings检测。

  标记 : "b0.b测2,ure" [标(4, 8)] // "b测2"A队建筑或中立建筑刷附属建筑，附属建筑为1号，单位为修复湾

  标记 : "b-2.b测1,n" [标(4, 9)] // "b测1"中立建筑刷附属建筑，附属建筑为敌对

  标记 : "b0.b测2,n" [标(4, 8)] // "b测2"A队建筑刷附属建筑，附属建筑为1号

  标记 : "b3.b测3,n" [标(4, 9)] // "b测3"B队建筑刷附属建筑，附属建筑为4号

  标记 : "b3.b测3,w" [标(4, 9)] // "b测3"B队建筑或中立建筑刷附属建筑，附属建筑为4号。仅初始刷新（切换为"fi6""）

  标记 : "b3.b测3,y" [标(4, 9)] // 初始6s，持续3s刷新，不受控制。

## 5.多文本城市

### 所需info和标记-多文本城市

  info: "dictionary_info_d" [i(1, 3)]
  info: "building_info_zci" [i(2, 6)]
  info: "teamDetect_info_ztdo" [i(3, 7)]
  info: "tree_info_zcto" [i(3, 1)]
  info: "flash_info_fd" [i(4, 12, 1)]
  info: "flash_info_fi" [i(4, 12, 2)]
  info: "building_info_b" [i(4, 6)]
  标记: "d.d" [控(1, 1)]
  标记: "fd.fd6_3.12s.6s" [控(4, 2, 1)]
  标记: "fd.fd12_6.12s.6s" [控(4, 2, 2)]
  标记: "fi.fi6.6s" [控(4, 2, 3)]
  标记: "zcto-2.zbt测1.测1" [附(4, 1)]
  标记: "zcto0.zbt测2.测2" [附(4, 2)]
  标记: "zcto3.zbt测3.测3" [附(4, 3)]

### 前缀-多文本城市

  "b"

### 必填参数-多文本城市

  附属建筑的所属队伍(team)

  附属建筑所依附的城市(ctd_cite)

### 选填参数-多文本城市

  ",u": 建筑单位类型，默认为虫塔。还可以添加其他建筑单位，比如su(supplyDepot补给站)等，具体可以在dictionary_info_d 参数里面查看简化情况。

  ",n": 是否改变默认的isneutralspawn 选项。

  ",w": 是否改变默认的isbugdisposable 选项。

  ",f": 使用其他非默认的flash标记刷新附属建筑。如果为fd系列的flash_info，请确保isbugdisposable 开启。如果是fi系列的flash_info，请确保isbugdisposable 关闭。

  ",o": 是否改变默认的isonlybuilding 选项。isonlybuilding开启时，使用onlyBuildings检测单位，而不是使用unitType。

  ",y": 是否改变默认的isbugTurretdeacti 选项。
  
### info中可改变的参数-多文本城市

  info : "dictionary_info_d" [i(1, 3)]

    su : "supplyDepot" // 简化补给站翻译

    bt : "bugTurret" // 简化虫塔翻译

    tu : "turret" // 简化炮塔翻译

    ...可以添加更多建筑翻译供,u使用。

  info : "building_info_b" [i(4, 6)]

    aunit_now : "bugTurret" // 默认单位类型，可修改成其他建筑，示例中默认为虫塔。

    isbugTurretdeacti : "true" // isbugTurretdeacti关闭时，附属建筑不再依附。（持续刷新，不受控制）。

    isneutralspawn : "true" // isneutralspawn开启时，附属建筑在依附城市中立或不存在时也会刷新。

    isbugdisposable : "true" // isbugdisposable开启时，附属建筑是重复刷新的，将会启用"fd6_3"(初始6s，每3s刷新一次)，否则启动"fi6"(初始6s后不再刷新)。

    fd_cite : "fd6_3" // 已部署的flash_info_fd标记，表明该建筑默认下开局6s刷新，3s再刷新一次(isbugdisposable 开启)

    fi_cite : "fd6_3" // 已部署的flash_info_fi标记，表明该建筑默认下仅开局6s刷新(isbugdisposable 关闭)

### 示例-多文本城市

  标记 : "b-2.b测1" [标(3, 1)] // "b测1"中立建筑刷附属建筑，附属建筑为敌对

  标记 : "b-1.b测1" [标(3, 2)] // "b测1"中立建筑刷附属建筑，附属建筑为中立

  标记 : "b0.b测2" [标(3, 3)] // "b测2"A队建筑或中立建筑刷附属建筑，附属建筑为1号

  标记 : "b3.b测3" [标(3, 4)] // "b测3"B队建筑或中立建筑刷附属建筑，附属建筑为4号

  标记 : "b0.b测2,ffd12_6" [标(3, 5)] // "b测2"A队建筑或中立建筑刷附属建筑，附属建筑为1号，刷新改为初始12s，持续6s

  标记 : "b0.b测2,usu" [标(3, 6)] // "b测2"A队建筑或中立建筑刷附属建筑，附属建筑为1号，单位为补给站

  标记 : "b0.b测2,utu,o" [标(3, 7)] // "b测2"A队建筑或中立建筑刷附属建筑，附属建筑为1号，单位为炮塔，转换为使用onlyBuildings检测。

  标记 : "b0.b测2,ure" [标(3, 8)] // "b测2"A队建筑或中立建筑刷附属建筑，附属建筑为1号，单位为修复湾

  标记 : "b-2.b测1,n" [标(3, 9)] // "b测1"中立建筑刷附属建筑，附属建筑为敌对

  标记 : "b0.b测2,n" [标(3, 8)] // "b测2"A队建筑刷附属建筑，附属建筑为1号

  标记 : "b3.b测3,n" [标(3, 9)] // "b测3"B队建筑刷附属建筑，附属建筑为4号

  标记 : "b3.b测3,w" [标(3, 9)] // "b测3"B队建筑或中立建筑刷附属建筑，附属建筑为4号。仅初始刷新（切换为"fi6""）

  标记 : "b3.b测3,y" [标(3, 9)] // 初始6s，持续3s刷新，不受控制。

## 注意事项

### team

-2为敌对，-1为中立，玩家从0开始，0代表1号玩家。

### 时间

所有时间必须以s为单位。

所有时间必须大于等于0s
