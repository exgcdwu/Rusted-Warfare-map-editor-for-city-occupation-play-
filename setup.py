# setup.py

import os
from setuptools import setup, find_packages

__version__ = '1.6.4'


def read_file(file:str):
    with open(file) as file:
        return file.read()

def readline_file(file:str):
    with open(file) as file:
        module_list = file.read().split("\n")
    return [module for module in module_list if module != ""]

DATA_PREFIX_MAPS = 'other_data/maps/'
ARGPARSE_FILE = "auto"
ARGPARSE_FUNC = {
    "triggerauto": "triggerauto"
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
    package_data={'rwmap': ['other_data/*.txt', DATA_PREFIX_MAPS + '*.tsx', DATA_PREFIX_MAPS + 'bitmaps/*.png',
                             DATA_PREFIX_MAPS + 'ridges/*.tsx', DATA_PREFIX_MAPS + 'terrain/*.tsx']},
    python_requires = '>=3.6.0',
    install_requires = readline_file("./rwmap/other_data/requirements.txt"), 
    entry_points={
        "console_scripts": [f"{name} = {ARGPARSE_FILE}:{value}" for name, value in ARGPARSE_FUNC.items()]
    }
)
