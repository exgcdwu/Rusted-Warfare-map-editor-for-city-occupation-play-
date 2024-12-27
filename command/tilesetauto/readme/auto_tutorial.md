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

    parser.add_argument('map_path', action = "store", metavar = 'file', type=str, 
                        help='The input path of RW map file.\n' + \
                            '铁锈地图文件的输入路径。')
    
    parser.add_argument("-o", "--output", 
                        action = "store", metavar = "file", type = str, nargs = "?", 
                        required = False, default = "|", 
                        const = "|", 
                        help = "The output path of RW map file.|input path\n" + \
                               "铁锈地图文件的输出路径。"
                        )

    parser.add_argument("-y", "--isyes", 
                        action = 'store_true', help = 'Requests are always y.\n' + \
                            "所有输入请求默认为y，继续执行。")
    
    parser.add_argument("-v", "--verbose", 
                        action = 'store_true', help = 'Detailed output of the prompt message.\n' + \
                            "提供运行信息。")

    parser.add_argument("--debug", 
                        action = 'store_true', help = 'Mode of debuging.\n' + \
                            "进入python debug模式。")

    parser.add_argument("--ignorewarning", 
                        action = 'store_true', help = 'Warning would not exit.\n' + \
                            "警告将不会退出。")
    
    parser.add_argument("--language", 
                        action = "store", metavar = "language", type = str, nargs = "?", 
                        required = False, default = "default", 
                        const = "default", 
                        help = "The language of prompt(ch/eg). The language configuration will be stored.(command/config.json)\n" + \
                        "命令行提示的语言(中文(ch),英文(eg))。语言设置将会被存储。(command/config.json)"
                        )

    parser.add_argument('-i', '--imagelayer', 
    parser.add_argument('-ct', '--colortileset'
    parser.add_argument('-c', '--color', 
    parser.add_argument('--name', '--colorname', 
    parser.add_argument('-cr', '--colorterrain', 
    parser.add_argument('-cw', '--colorwidth', 
    parser.add_argument('-cp', '--delta_lxc', 
    parser.add_argument('-kt', '--kmeantileset', 
    parser.add_argument('-s', '--ktilesetsize',
    parser.add_argument('-r', '--randseed', 
    parser.add_argument('--resizediv', 
    parser.add_argument('-m', '--kmeanstopmovenum',
    parser.add_argument('-cy', '--kmeanlimitcycle', 
    parser.add_argument('-j', '--config', 
    parser.add_argument('-n', '--noise', 

### 命令参数

    -o --output 输出到不同路径（建议，防止覆盖后无法悔改）。

    -v --verbose 显示运行信息

    --ignorewarning 发生warning时，会继续执行，而不会退出程序。

    -y --isyes 自动同意程序的一切(y/n)请求

    --language 后仅允许跟"ch"(中文)/"eg"(英文)。语言设置将会被储存，之后使用延续上一次的修改。

    -j --config 算法产生的地块集，应当如何添加属性。后面跟.json文件路径。该.json文件的"kmean-tileproperties"会从前往后执行，根据对应HSV范围来确定是否加入属性。后面的添加会覆盖前面的。可以没有该选项，那么不会添加属性。后面会有一些参数也可以在.json文件中配置。"purecolor-ntexist"是一个字典，将每一个颜色索引映射到地形索引，必填。形如：    
    
    ```json
    {
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
        ], 
        "purecolor-ntexist": {
            "0": 0, 
            "1": 1, 
            "2": 2, 
            "3": 2
        }, 
    }
    ```

    -n --noise 后面跟3个数字，分别是地块像素点在HSV的高斯噪声的标准差。

    如果直接产生纯色地块。

    -ct --colortileset 直接产生的纯色地块集名称。

    -c --color 产生的若干纯色，后面跟一个或多个RGB颜色，格式例子"#FFDD00"

    --name  --colorname 产生的若干纯色的名字，来在地形中显示名称。

    ```json
    {
        "purecolor-name": [
            "#000000:虚空,block-land|0;0;0", 
            "#090919:视域,block-land", 
            "#828583:FTL航线,water", 
            "#fdfcb6:星系,water-bridge"
    ]
    ```
    第一个为color, 第二个为name, 第三个为属性, 第四个为每个地形的HSV噪声

    -cr 每一个颜色的地形，为若干对非负整数，每一对非负整数表示不同颜色索引产生的新地形。

    ```json
    {
        "purecolor-colorpair": [
            [0, 1], 
            [1, 2], 
            [2, 3]
        ]
    }
    ```

    -cw 地块集的宽(实际要×3)，如果为-1则沿着地块集宽铺开。

    ```json
    {
        "purecolor-colorpair-y": -1
    }
    ```

    -cp 后面跟三个数字，分别是dl, dx, dc，均为0-1的小数。即边缘地形到外部过度的参数，dl为在何处开始过渡，dx指过渡区域的范围，dc指过渡区域的改变范围。

    ```json
    {
        "purecolor-delta-lxc": [
            [0, 0, 0], 
            [0, 0, 0], 
            [0, 0, 0]
        ]
    }
    ```
    每一种地形的dl, dx, dc。-cp将会覆盖config内容。

    也可以通过图像层产生纯色地块，使用kmean聚类算法。使用k-mean算法时建议添加-v选项观察进度。

    -i --imagelayer 图像层名称。

    -kt --kmeantileset 产生的k-mean纯色地块集名称。

    -s --ktilesetsize k-mean算法产生地块集大小（后跟两个数字，分别为高度和宽度）（例如"20 20"，产生20×20地块集）。

    -r --randseed k-mean算法初始随机数种子，不填当前时间为随机数种子。

    --resizediv k-mean算法采样周期。越大越快，准确度可能下降。

    -m --kmeanstopmovenum k-mean算法终止时的移动步数，默认为0。可以适当提高以提高速度。

    -cy --kmeanlimitcycle k-mean算法终止时的最大计算轮数，默认为16 × s.x × s.y。可以减少以防止长时间运行。

### k-mean聚类算法时间复杂度

设 $d = resizediv$, $s_x$ 是地块集高度方向地块数目, $s_y$ 是地块集宽度方向地块数目, $t_x$ 是一个地块的高度, $t_y$ 是一个地块的宽度, $i_x$为图像层与图层重叠部分高度方向地块数目, $i_y$为图像层与图层重叠部分宽度方向地块数目。$n$ k-mean为进行轮数，并且$n \leq cy$。

$\Theta(t_x t_y (i_x i_y + s_x s_y + \frac{i_x i_y s_x s_y}{resizediv^2}n))$

考虑到$n \leq cy$, 则为$O(t_x t_y (i_x i_y + s_x s_y + \frac{i_x i_y s_x s_y}{resizediv^2}cy))$。
