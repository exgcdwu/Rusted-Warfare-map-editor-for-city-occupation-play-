# 地块集自动化参数说明

- [地块集自动化参数说明](#地块集自动化参数说明)
  - [目标](#目标)
    - [命令](#命令)
    - [命令参数](#命令参数)
    - [k-mean聚类算法时间复杂度](#k-mean聚类算法时间复杂度)

## 目标

地块集自动化命令，目标是自动生成地块集。

### 命令

打开终端，输入如下指令：

    tilesetauto {map_file}

该指令读入地图路径，将转换结果自动输到原路径。

### 命令参数

    -o --output 输出到不同路径（建议，防止覆盖后无法悔改）。

    -v --verbose 显示运行信息

    --ignorewarning 发生warning时，会继续执行，而不会退出程序。

    -y --isyes 自动同意程序的一切(y/n)请求

    --language 后仅允许跟"ch"(中文)/"eg"(英文)。语言设置将会被储存，之后使用延续上一次的修改。

    -p --tileproperties 算法产生的地块集，应当如何添加属性。后面跟.json文件路径。该.json文件的"kmean-tileproperties"会从前往后执行，根据对应HSV范围来确定是否加入属性。后面的添加会覆盖前面的。可以没有该选项，那么不会添加属性。形如：

    ```json{
            "kmean-tileproperties": [
                {
                    "type": "HSV",
                    "name": "water", 
                    "H-range": [0.500, 0.667],
                    "S-range": [0.15, 1], 
                    "V-range": [0.15, 1]
                },
                {
                    "type": "HSV",
                    "name": "water", 
                    "H-range": [0.600, 0.68],
                    "S-range": [0.05, 0.15], 
                    "V-range": [0.7, 1]
                }
            ]
        }
    ```

    如果直接产生纯色地块。

    -ct --colortileset 直接产生的纯色地块集名称。

    -c --color 产生的若干纯色，后面跟一个或多个RGB颜色，格式例子"#FFDD00"

    也可以通过图像层产生纯色地块，使用kmean聚类算法。使用k-mean算法时建议添加-v选项观察进度。

    -i --imagelayer 图像层名称。

    -kt --kmeantileset 产生的k-mean纯色地块集名称。

    -s --ktilesetsize k-mean算法产生地块集大小（后跟两个数字，分别为高度和宽度）（例如"10 10"，产生20×10地块集）。

    -r --krandset k-mean算法初始随机数种子，不填当前时间为随机数种子。

    --resizediv k-mean算法采样周期。越大越快，准确度可能下降。

    -m --kmeanstopmovenum k-mean算法终止时的移动步数，默认为0。可以适当提高以提高速度。

    -cy --kmeanlimitcycle k-mean算法终止时的最大计算轮数，默认为16 × s.x × s.y。可以减少以防止长时间运行。

### k-mean聚类算法时间复杂度

设 $d = resizediv$, $s_x$ 是地块集高度方向地块数目, $s_y$ 是地块集宽度方向地块数目, $t_x$ 是一个地块的高度, $t_y$ 是一个地块的宽度, $i_x$为图像层与图层重叠部分高度方向地块数目, $i_y$为图像层与图层重叠部分宽度方向地块数目。$n$ k-mean为进行轮数，并且$n \leq cy$。

$\Theta(t_x t_y (i_x i_y + s_x s_y + \frac{i_x i_y s_x s_y}{resizediv^2}n))$

考虑到$n \leq cy$, 则为$O(t_x t_y (i_x i_y + s_x s_y + \frac{i_x i_y s_x s_y}{resizediv^2}cy))$。
