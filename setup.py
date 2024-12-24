# setup.py

import os
from setuptools import setup, find_packages
from setuptools import Command
import subprocess


__version__ = '1.8.0'

cmake_sh = 'cmake_install.sh'

class CMakeBuildCommand(Command):

    description = "Run cmake to build c extension."
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        this_dir = os.path.abspath(os.path.dirname(__file__))
        cmakel = readline_file(cmake_sh)
        for cmakel_now in cmakel:
            subprocess.check_call(' '.split(cmakel_now), cwd=this_dir)

ext_modules = [
]

def read_file(file:str):
    with open(file, encoding = 'utf-8') as file:
        return file.read()

def readline_file(file:str):
    with open(file, encoding = 'utf-8') as file:
        module_list = file.read().split("\n")
    return [module for module in module_list if module != ""]

DATA_PREFIX_MAPS = 'other_data/maps/'
ARGPARSE_FILE = "command"
ARGPARSE_FUNC = {
    "objectgroupauto": "objectgroupauto", 
    "tsindep": "tsindep", 
    "idrearrange": "idrearrange", 
    "layerauto": "layerauto", 
    "tilesetauto": "tilesetauto",
    "layerobauto": "layerobauto"
}

setup(
    name = 'rwmapeditor_exgcdwu',
    version = __version__,
    author = 'exgcdwu',
    author_email = '1006605318@qq.com',
    license = read_file('LICENSE'),
    url = "https://github.com/exgcdwu/Rusted-Warfare-map-editor-for-city-occupation-play-",
    long_description = read_file('README.md'),
    long_description_content_type = "text/markdown",
    packages = find_packages(exclude=["tests", "examples"]),
    package_data = {'rwmap': ['other_data/*.txt', DATA_PREFIX_MAPS + '*.tsx', DATA_PREFIX_MAPS + 'bitmaps/*.png',
                             DATA_PREFIX_MAPS + 'ridges/*.tsx', DATA_PREFIX_MAPS + 'terrain/*.tsx'], 
                    'command': ['*.json']},
    python_requires = '>=3.6.0',
    install_requires = readline_file("./rwmap/other_data/requirements.txt"), 
    entry_points={
        "console_scripts": [f"{name} = {ARGPARSE_FILE}:{value}" for name, value in ARGPARSE_FUNC.items()]
    }, 
    scripts=[cmake_sh],
    cmdclass={
        'runscript': CMakeBuildCommand,  # 注册自定义命令类
    },
    zip_safe = False
)

# MSYS2 windows模拟linux环境