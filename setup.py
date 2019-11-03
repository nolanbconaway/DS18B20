"""Set up the thermometer module."""

from setuptools import find_packages, setup

setup(
    name="thermometer",
    version="0.1",
    packages=find_packages(),
    python_requires=">=3.5",
    extras_require={"test": ["black", "pylint", "pydocstyle", "pytest"]},
    entry_points={"console_scripts": ["temperature=thermometer.cli:main"]},
)
