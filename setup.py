# setup.py

#import os
from setuptools import setup, find_packages

__version__ = '1.1'
#current_dir = os.path.dirname(__file__)
#requirements = open(current_dir + '/requirements.txt').readlines()

def readme():
    with open('README.md') as file:
        return file.read()

strreadme = readme()

setup(
    name = 'rwmapeditor_exgcdwu',
    version = __version__,
    author = 'exgcdwu',
    author_email = '1006605318@qq.com',
    url = "https://github.com/exgcdwu/Rusted-Warfare-map-editor-for-city-occupation-play-",
    long_description = strreadme,
    long_description_content_type = "text/markdown",
    packages = find_packages(exclude=["tests"]),
    python_requires = '>=3.0.0'
    #,install_requires = requirements
)