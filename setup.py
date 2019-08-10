'''setup.py: setup foodrw cli app with its dependencies'''

import re
from setuptools import setup

version = re.search(
    "^__version__\s*=\s*'(.*)'",
    open('foodrw/foodrw.py').read(),
    re.M
).group(1)

