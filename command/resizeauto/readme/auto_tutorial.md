# 地图扩大参数说明

- [地图扩大参数说明](#地图扩大参数说明)
  - [目标](#目标)
  - [使用](#使用)
    - [命令](#命令)
    - [命令参数](#命令参数)

## 目标

地图扩大命令，目的是将一张地图整体放大

## 使用

### 命令

打开终端，输入如下指令：

    resizeauto {map_file}

该指令读入地图路径，将转换结果自动输到原路径。

### 命令参数

    -o --output 输出到不同路径（建议，防止覆盖后无法悔改）。

    -v --verbose 显示运行信息

    --ignorewarning 发生warning时，会继续执行，而不会退出程序。

    -y --isyes 自动同意程序的一切(y/n)请求

    --language 后仅允许跟"ch"(中文)/"eg"(英文)。语言设置将会被储存，之后使用延续上一次的修改。

    -s --resize 跟两个数字，第一个是地图高放大倍数，第二个是地图宽放大倍数，必须都是正整数，默认为1 1。