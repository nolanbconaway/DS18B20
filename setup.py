"""Set up the thermometer module."""
import sys
from pathlib import Path

from setuptools import setup

assert sys.version_info.major > 2, "This package is not python 2 compatible!"

setup(
    name="thermometer",
    version="0.3.0",
    package_dir={"": "src"},
    packages=["thermometer"],
    python_requires=">=3.5",
    entry_points={"console_scripts": ["temperature=thermometer.cli:main"]},
)
