# -*- coding: utf-8 -*-
"""setup with setuptools."""

from setuptools import setup, find_packages

setup(
    name='stream_watcher',
    version='0.1',
    keywords='Stream',
    description='A Pythonic way to manage streams in one file.',
    author='Logic',
    author_email='logic.irl@outlook.com',
    url='https://github.com/TheStar-LikeDust/shared_memory_toolkit.git',
    python_requires='>=3.8',
    packages=find_packages(exclude=['tests*']),
    license='Apache License 2.0'
)
