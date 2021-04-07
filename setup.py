"""
BottleCBV
-------------

Class based views for Bottle
"""
from setuptools import setup

setup(
    name='BottleCBV',
    version='0.1',
    url='https://github.com/techchunks/bottleCBV',
    license='BSD',
    author='Technology Chunks',
    author_email='aedil12155@gmail.com',
    description='Class based views for Bottle apps',
    long_description="Class Based View for Bottle (Inspired by flask-classy)",
    py_modules=['bottleCBV'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'bottle==0.12.19'
    ],
    keywords=['bottle', 'bottlepy', 'class-based-view'],
    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 4 - Beta",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        'Framework :: Bottle'
    ],
    test_suite='tests'
)