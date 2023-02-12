#!/usr/bin/env python3

"""
The package description.
"""

from setuptools import setup
from foodlog.version import __version__

with open("README.md", encoding="utf-8-sig") as readme_file:
    long_description = readme_file.read()

setup(
    name="foodlog",
    version=__version__,
    description="A simple CLI timer to calculate fasting zones.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vkostyanetsky/Foodlog",
    license="MIT",
    python_requires=">=3.7",
    packages=["foodlog"],
    install_requires=[
        "PyYAML~=6.0",
        "keyboard~=0.13.5",
        "vkostyanetsky.cliutils~=0.2.0",
    ],
    entry_points={"console_scripts": ["foodlog=foodlog.app:main_menu"]},
    author="Vlad Kostyanetsky",
    author_email="vlad@kostyanetsky.me",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Utilities",
    ],
    keywords="food diary",
)
