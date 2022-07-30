#!/usr/bin/env python3

from setuptools import setup
from foodlog.version import __version__


setup(
    name="foodlog",
    version=__version__,
    description="A simple CLI timer to calculate fasting zones.",
    long_description=open('README.md', encoding="utf-8-sig").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/vkostyanetsky/Foodlog",
    license="MIT",
    python_requires=">=3.7",
    packages=["foodlog"],
    install_requires=["console_menu~=0.7.1", "PyYAML~=6.0"],
    entry_points={"console_scripts": [
        "foodlog=foodlog.foodlog:main"
    ]},
    author="Vlad Kostyanetsky",
    author_email="vlad@kostyanetsky.me",
    # https://pypi.org/pypi?:action=list_classifiers
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 3.7",
        "Topic :: Utilities",
    ],
    keywords="food diary"
)
