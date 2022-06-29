#!/usr/bin/env python3

from setuptools import setup
from food_diary.version import __version__


setup(
    name="food_diary",
    version=__version__,
    description="Keep a food diary to count calories, proteins, fats & carbohydrates.",
    long_description=open('README.md', encoding="utf-8-sig").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/vkostyanetsky/FoodDiary",
    license="MIT",
    python_requires=">=3.6",
    packages=["food_diary"],
    install_requires=["ConsoleMenu~=1.0.1", "PyYAML~=6.0"],
    entry_points={"console_scripts": [
        "food_diary=food_diary.food_diary:main"
    ]},
    author="Vlad Kostyanetsky",
    author_email="vlad@kostyanetsky.me",
    # https://pypi.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 3.6",
        "Topic :: Office/Business :: News/Diary",
        "Topic :: Utilities"
    ],
    keywords="food diary"
)
