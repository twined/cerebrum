# -*- coding: utf-8 -*-
from distutils.core import setup
from setuptools import find_packages

setup(
    name='cerebrum',
    version='1.1.0',
    author=u'Twined',
    author_email='www.twined.net',
    packages=find_packages(),
    include_package_data=True,
    url='http://github.com/twined/cerebrum',
    license='Do what thou wilt.',
    description='Admin for twined apps',
    long_description=open('README.md').read(),
    zip_safe=False,
    install_requires=[
        'six',
    ]
)
