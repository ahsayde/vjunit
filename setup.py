#!/usr/bin/env python3
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="vjunit",
    version="0.3",
    description="Generate html file from junit reports",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Ahmed El-Sayed",
    author_email="ahmed.m.elsayed93@gmail.com",
    url="http://github.com/ahelsayd/vjunit",
    install_requires=["jinja2"],
    packages=["vjunit"],
    package_data={"vjunit": ["template.html"]},
    include_package_data=True,
    entry_points={"console_scripts": ["vjunit=vjunit.__main__:main"]},
)
