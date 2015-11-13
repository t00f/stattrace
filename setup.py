# -*- coding:utf-8 -*-

from setuptools import setup, find_packages

setup(
    name="stattrace",
    packages=find_packages(exclude=["*tests*"]),
    version="0.0.1",
    description="Easily create and query for statistics data",
    author="Christophe Serafin",
    author_email="christophe.serafin@gmail.com",
    classifiers=[],
    install_requires=[line for line in open("requirements.txt")],
)
