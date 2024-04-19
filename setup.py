# setup.py

import os
from setuptools import setup, find_packages

__version__ = '1.2.8'

def read_file(file:str):
    with open(file) as file:
        return file.read()

def readline_file(file:str):
    with open(file) as file:
        return file.readline()

DATA_PREFIX_MAPS = 'other_data/maps/'

setup(
    name = 'rwmapeditor_exgcdwu',
    version = __version__,
    author = 'exgcdwu',
    author_email = '1006605318@qq.com',
    license = read_file('LICENSE'),
    url = "https://github.com/exgcdwu/Rusted-Warfare-map-editor-for-city-occupation-play-",
    long_description = read_file('README.md'),
    long_description_content_type = "text/markdown",
    packages = find_packages(exclude=["tests"]),
    package_data={'rwmap': ['other_data/*.txt', DATA_PREFIX_MAPS + '*.tsx', DATA_PREFIX_MAPS + 'bitmaps/*.png',
                             DATA_PREFIX_MAPS + 'ridges/*.tsx', DATA_PREFIX_MAPS + 'terrain/*.tsx']},
    python_requires = '>=3.5.0',
    install_requires = readline_file("./rwmap/other_data/requirements.txt")
)
