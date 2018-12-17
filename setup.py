#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

requirements = [
    'PyQt5'
]

test_requirements = [
    'pyautogui', 'pyautogui',  # TODO: put package test requirements here
]

setup(
    name='easygraphics',
    version='0.9.1',
    description='"A TC Graphics style like Graphics Library"',
    long_description=readme + '\n\n' + history,
    author='Roy Qu',
    author_email='royqh1979@gmail.com',
    url='https://github.com/royqh1979/PyEasyGraphics',
    packages=[
        'easygraphics', 'easygraphics.dialog'
    ],
    package_dir={'easygraphics':
                     'easygraphics'},
    include_package_data=True,
    install_requires=['', 'PyQt5'],
    license="GPLv3",
    zip_safe=False,
    keywords='easygrphics',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Education',
        'License :: OSI Approved :: GPL License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
    #    test_suite='tests',
    #    tests_require=test_requirements
)
