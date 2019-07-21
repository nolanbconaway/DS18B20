from setuptools import find_packages, setup

setup(
    name="thermometer",  # Required
    version="0.1",
    packages=find_packages(),  # Required
    python_requires=">=3.5",
    install_requires=["sqlalchemy", "python-dotenv"],  # Optional
    extras_require={"test": ["black", "pylint", "pydocstyle"]},  # Optional
)
