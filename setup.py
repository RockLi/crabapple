# Copyright 2014 The crabapple Authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

from setuptools import setup

with open('README.md', 'r') as fp:
    long_description = fp.read()

setup(name='crabapple',
      version='0.1',
      author='Rock Lee',
      author_email='insfocus@gmail.com',
      url='http://pypi.python.org/pypi/crabapple/',
      packages=[
          'crabapple',
          'crabapple.helper',
          'crabapple.command',
          'crabapple.admin',
          'crabapple.notifier',
      ],
      scripts=[
          'bin/crabapple'
      ],
      install_requires=[
          'SQLAlchemy',
          'arrow'
      ],
      description='An automatic deployment tool which integrated with Github',
      long_description=long_description,
      license='BSD',
      classifiers=[
          "Programming Language :: Python :: 2",
          "Intended Audience :: Developers",
          "License :: OSI Approved :: BSD License",
          "Topic :: Software Development :: Libraries",
          "Topic :: Utilities",
      ])
