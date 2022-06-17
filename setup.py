# -*- coding: utf-8 -*-
"""setup with setuptools."""

from setuptools import setup, find_packages

setup(
    name='shared_memory_toolkit',
    version='0.1.1',
    keywords='SharedMemory',
    description='A Python shared memory toolkit for process picture between different processes.',
    author='Logic',
    author_email='logic.irl@outlook.com',
    url='https://github.com/TheStar-LikeDust/shared_memory_toolkit',
    python_requires='>=3.8',
    packages=find_packages(exclude=['tests*']),
    license='Apache License 2.0'
)
