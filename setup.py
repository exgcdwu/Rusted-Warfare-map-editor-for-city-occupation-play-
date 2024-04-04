# setup.py

from setuptools import setup, find_packages

__version__ = '1.0'
requirements = open(',/requirements.txt').readlines()

setup(
    name = 'rwmapeditor_exgcdwu',
    version = __version__,
    author = 'exgcdwu',
    author_email = '1006605318@qq.com',
    url = "https://github.com/exgcdwu/Rusted-Warfare-map-editor-for-city-occupation-play-",
    description = 'Python Setup',
    packages = find_packages(exclude=["tests"]),
    python_requires = '>=3.0.0',
    install_requires = requirements
        )