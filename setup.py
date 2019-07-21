from setuptools import find_packages, setup

setup(
    name="thermometer",
    version="0.1",
    packages=find_packages(),
    python_requires=">=3.5",
    install_requires=["sqlalchemy", "python-dotenv"],
    extras_require={"test": ["black", "pylint", "pydocstyle"]},
)
