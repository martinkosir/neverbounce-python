# -*- coding: utf-8 -*-
import re
from __future__ import unicode_literals
from setuptools import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

with open('neverbounce/__init__.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('Cannot find version information')

setup(
    name='neverbounce',
    version=version,
    author='Martin Kosír',
    author_email='martin@martinkosir.net',
    packages=['neverbounce'],
    url='https://github.com/martinkosir/neverbounce-python',
    download_url='https://github.com/martinkosir/neverbounce-python/tarball/{}'.format(version),
    license='MIT',
    description='API library for the NeverBounce email verification service.',
    long_description=long_description,
    install_requires=['requests>=2.9.0'],
    keywords=['api', 'email', 'verification'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Communications :: Email',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    tests_require=['pytest>=3.0.0', 'responses>=0.5.0']
)
