# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from setuptools import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='neverbounce',
    version='0.1.3',
    author='Martin Kosír',
    author_email='martin@martinkosir.net',
    packages=['neverbounce'],
    url='https://github.com/martinkosir/neverbounce-python',
    license='MIT',
    description='API library for the NeverBounce email verification service.',
    long_description=long_description,
    install_requires=['requests>=2.9.0'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Communications :: Email',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
