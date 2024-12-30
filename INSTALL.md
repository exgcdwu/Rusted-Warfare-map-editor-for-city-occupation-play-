# rwmapeditor-exgcdwu 安装

## 电脑

### pip安装

建议安装vscode，请自行搜索如何在vscode上使用python并下载python包。然后使用

    pip install rwmapeditor-exgcdwu

来安装包，开始使用。

### 手动安装

使用git将本仓库克隆到本地，然后切换到仓库目录，运行

    cmake_intstall.sh
    python setup.py install

## 手机termux

还可以使用Termux来在手机上操作python和命令行。

[github Termux](https://github.com/termux/termux-app)

termux python环境及包下载：

`需要一段时间，保持网络畅通`

`感谢kend在使用termux安装python包方面的帮助`

`每一条均需要顺序执行，开头不得出现空格。请尽量复制粘贴后执行。`

`中间出现的提问选项，全部输入y再回车`

    pkg update -y
    pkg install -y python
    pkg install -y python-numpy
    pkg install -y python-pillow
    pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple #（如果清华镜像不可以，换成别的镜像比如https://pypi.mirrors.ustc.edu.cn/simple 也行）
    pip install asteval
    pip install regex # 1.6.3新加入
    pip install pybind11 # 1.8.0新加入
    pip install imageio # 1.8.0新加入
    pip install sortedcontainers # 1.8.0新加入

    pip install rwmapeditor-exgcdwu==1.8.5 --no-deps
    termux-setup-storage

然后点同意获取读取存储权限

之后就可以使用termux使用objectgroupauto, layerauto处理地图文件了。

如果想要更改版本，使用如下命令行。

    pip uninstall -y rwmapeditor-exgcdwu
    pip install rwmapeditor-exgcdwu==1.6.1 --no-deps #（新版本，大于等于1.6.1）
