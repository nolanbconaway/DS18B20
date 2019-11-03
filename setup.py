"""Set up the thermometer module."""
import sys

from setuptools import setup

TEST_DEPS = ["pylint", "pydocstyle", "pytest"]

assert sys.version_info.major > 2, "This package is not python 2 compatible!"

if sys.version_info.minor > 5:
    TEST_DEPS.append("black")

setup(
    name="thermometer",
    version="0.2",
    packages=["thermometer"],
    python_requires=">=3.5",
    extras_require={"test": ["pylint", "pydocstyle", "pytest"]},
    entry_points={"console_scripts": ["temperature=thermometer.cli:main"]},
)
