from distutils.core import setup
from setuptools import setup, find_packages

setup(
    name="Sea",
    version="0.1.3",
    author="Ultr4",
    author_email="ultra@ultra.io",
    packages=find_packages(),
    long_description=open("README.md").read(),
)
