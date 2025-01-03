# 图块自动化参数说明

- [图块自动化参数说明](#图块自动化参数说明)
  - [目标](#目标)
  - [使用](#使用)
    - [命令](#命令)
    - [命令参数](#命令参数)
    - [算法](#算法)

## 目标

图层自动化命令，目标是通过图像层自动获得图层。

## 使用

### 命令

打开终端，输入如下指令：

    layermapauto {map_file}

该指令读入地图路径，将转换结果自动输到原路径。

### 命令参数

    -o --output 输出到不同路径（建议，防止覆盖后无法悔改）。

    -v --verbose 显示运行信息

    --ignorewarning 发生warning时，会继续执行，而不会退出程序。

    -y --isyes 自动同意程序的一切(y/n)请求

    --language 后仅允许跟"ch"(中文)/"eg"(英文)。语言设置将会被储存，之后使用延续上一次的修改。

    -i --imagelayer 图像层名称。

    -l --layer 图层名称。

    -w --whitelist 图块集白名单，允许匹配的图块集。

### 算法

根据图像层和地块集每一块的RGB平均值的欧几里得距离确定图层上应当覆盖哪个地块（选择欧几里得距离最小的一个）。
