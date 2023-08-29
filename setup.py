#!/usr/bin/env python3

"""
The package description.
"""

from setuptools import setup
from foodlog import constants

with open("README.md", encoding="utf-8-sig") as readme_file:
    long_description = readme_file.read()

setup(
    name="foodlog",
    version=constants.VERSION,
    description="A simple CLI timer to calculate fasting zones.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vkostyanetsky/Foodlog",
    license="MIT",
    python_requires=">=3.7",
    packages=["foodlog"],
    install_requires=[
        "PyYAML==6.0.1",
        "click==8.1.7",
    ],
    entry_points={"console_scripts": ["foodlog=foodlog.app:cli"]},
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
