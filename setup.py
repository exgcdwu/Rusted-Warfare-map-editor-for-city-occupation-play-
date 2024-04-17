# setup.py

import os
from setuptools import setup, find_packages

__version__ = '1.2.3'

def read_file(file:str):
    with open(file) as file:
        return file.read()

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
    package_data={'rwmap': ['_maps/*.tsx', '_maps/bitmaps/*.png', '_maps/ridges/*.tsx', '_maps/ridges/bitmaps/*.png', '_maps/terrain/*.tsx', '_maps/ridges/terrain/*.png']},
    include_package_data=True,
    python_requires = '>=3.0.0',
)
