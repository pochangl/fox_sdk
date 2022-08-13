from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'fox_sdk'
LONG_DESCRIPTION = 'foxweiqi sdk'

setup(
    name='fox_sdk',
    version=VERSION,
    author='Charlie Lee',
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=['fox_sdk'],
    install_requires=['asgiref'],
)
