# setup.py

import os
from setuptools import setup, find_packages

__version__ = '1.2.1'

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
    package_data={'rwmaps': ['_maps/*']},
    include_package_data=True,
    python_requires = '>=3.0.0',
)
