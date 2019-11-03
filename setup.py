"""Set up the thermometer module."""

from setuptools import find_packages, setup

setup(
    name="thermometer",
    version="0.2",
    packages=find_packages(),
    python_requires=">=3.5",
    extras_require={"test": ["pylint", "pydocstyle", "pytest"]},
    entry_points={"console_scripts": ["temperature=thermometer.cli:main"]},
)
