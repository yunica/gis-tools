from os import path as op
import io

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

here = op.abspath(op.dirname(__file__))

with io.open(op.join(here, "requirements.txt"), encoding="utf-8") as f:
    install_requires = f.read().split("\n")
    install_requires = [i for i in install_requires if not i.startswith("gis-tools")]

with open("README.md") as f:
    readme = f.read()

setup(
    name="gis-tools",
    version="1.1.0",
    description="Python scripts for process geo data ",
    author="yunica",
    packages=find_packages(),
    install_requires=install_requires,
    entry_points={
        "console_scripts": ["gfw=src.gfw.__init__:main", "ffda=src.ffda.__init__:main"]
    },
    long_description=readme,
)
