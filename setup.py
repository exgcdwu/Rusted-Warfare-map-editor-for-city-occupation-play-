# setup.py

import os
from setuptools import setup, find_packages

__version__ = '1.2.1'

def readme():
    with open('README.md') as file:
        return file.read()

def requirements():
    with open('requirements.txt') as file:
        return file.readlines()

setup(
    name = 'rwmapeditor_exgcdwu',
    version = __version__,
    author = 'exgcdwu',
    author_email = '1006605318@qq.com',
    license = 'GPL-3.0',
    url = "https://github.com/exgcdwu/Rusted-Warfare-map-editor-for-city-occupation-play-",
    long_description = readme(),
    long_description_content_type = "text/markdown",
    packages = find_packages(exclude=["tests"]),
    data_files = {('.', './requirements.txt')},
    python_requires = '>=3.0.0',
    install_requires = requirements()
)
