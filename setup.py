#!/usr/bin/env python

from __future__ import with_statement
from setuptools import setup, find_packages
from tow.version import version

long_description = """Tow provides a workflow for building docker images
                        with dynamics configuration files using templates.
                        The main concept is processing all configuration
                        templates outside of container and then build
                        image using pre-processed files."""


setup(
    name='tow',
    version=version,
    description='Tow is tool for automatization docker configuration managment workflow',
    long_description=long_description,
    author='Aleksei Kornev, Nikolay Yurin',
    author_email='aleksei.kornev@gmail.com, ',
    url='https://github.com/alekseiko/tow',
    packages=find_packages(),
    test_suite='nose.collector',
    tests_require=['nose'],
    install_requires=['jinja2'],
    package_data={
        '': ['*.tmpl'],
    },
    entry_points={
        'console_scripts': [
            'tow = tow.main:main',
        ]
    },
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development',
        'Topic :: Software Development :: Build Tools',
        'Topic :: System :: Clustering',
        'Topic :: System :: Software Distribution',
        'Topic :: System :: Systems Administration',
    ],

)
