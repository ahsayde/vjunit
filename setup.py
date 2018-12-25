#!/usr/bin/env python3
from setuptools import setup

setup(
    name='junit2html',
    version='0.1',
    description='Generate html file from junit reports',
    author='Ahmed El-Sayed',
    author_email='ahmed.m.elsayed93@gmail.com',
    url='http://github.com/ahmedelsayed-93/junit2html',
    install_requires=['xmltodict', 'jinja2'],
    packages=['junit2html'],
    package_data = {'junit2html': ['template.html']},
    include_package_data=True,
    entry_points={'console_scripts': ['junit2html=junit2html.__main__:main']}
)