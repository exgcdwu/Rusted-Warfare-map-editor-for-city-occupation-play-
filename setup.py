# setup.py

import os
from setuptools import setup, Extension, find_packages
from setuptools.command.install import install
import subprocess
import sys

__version__ = '1.8.3.1'

class PostInstallCommand(install):
    def run(self):
        install.run(self)
        subprocess.check_call([sys.executable, '-c', 'import subprocess; '
                               'subprocess.check_call(["cmake", "-B", "build", "-S", "c_extension"])'])
        subprocess.check_call([sys.executable, '-c', 'import subprocess; '
                               'subprocess.check_call(["cmake", "--build", "build", "--config", "Release"])'])

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
    "layermapauto": "layermapauto", 
    "tilesetauto": "tilesetauto",
    "layerobauto": "layerobauto",
    "resizeauto": "resizeauto"
}
STE_VERSION = ["v10", "v100"]



for ste in STE_VERSION:
    ARGPARSE_FUNC["stellaris_" + ste] = "stellaris_" + ste

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
    cmdclass={
        'install': PostInstallCommand,
    }
)