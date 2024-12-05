from setuptools import setup, find_packages

setup(
    name="pytest-api",
    version="0.1",
    packages=find_packages(exclude=["tests"]),
)