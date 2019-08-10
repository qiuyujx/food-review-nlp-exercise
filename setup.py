'''setup.py: setup foodrw cli app with its dependencies'''

import re
import os
from setuptools import setup

# Get version
version = re.search(
    "^__version__\s*=\s*'(.*)'",
    open('foodrw/foodrw.py').read(),
    re.M
).group(1)

# Get Readme
with open("README.md", "rb") as f:
    long_descr = f.read().decode("utf-8")

# Get dependencies
if os.path.isfile('requirements.txt'):
    with open('requirements.txt') as rq_reader:
        pkgs = list(rq_reader.read().splitlines())

# Setup config
setup(
    name = "foodrw-cli",
    packages = ["foodrw"],
    entry_points = {
        "console_scripts": ['foodrw = foodrw.foodrw:main']
    },
    install_requires = pkgs,
    version = version,
    description = "Python cli tool for training and classifying food reviews sentiment target.",
    long_description = long_descr,
    author = "Christopher Tao",
    author_email = "me@christophertao.com",
    url = "https://www.linkedin.com/in/christopher-tao-5717a274/",
)