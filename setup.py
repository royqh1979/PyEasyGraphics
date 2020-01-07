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
    version='1.0.18',
    description='"A TC Graphics style like Graphics Library"',
    long_description=readme + '\n\n' + history,
    author='Roy Qu',
    author_email='royqh1979@gmail.com',
    url='https://github.com/royqh1979/PyEasyGraphics',
    packages=[
        'easygraphics', 'easygraphics.dialog', 'easygraphics._utils', 'easygraphics.legacy',
        'easygraphics.music', 'easygraphics.turtle', 'easygraphics.widget','easygraphics.processing',
    ],
    package_dir={'easygraphics':
                     'easygraphics'},
    package_data={'easygraphics.turtle': ['*.png']},
    include_package_data=True,
    install_requires=['', 'PyQt5', 'pygame', 'qimage2ndarray', 'apng'],
    license="BSD",
    zip_safe=False,
    keywords=['easygraphics', 'computer graphics', 'Turbo C graphics', 'Borland Graphics Interface'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: BSD License',
        'Intended Audience :: Education',
        'Topic :: Multimedia :: Graphics',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    #    test_suite='tests',
    #    tests_require=test_requirements
)
