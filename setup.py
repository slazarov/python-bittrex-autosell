# !/usr/bin/python
from setuptools import setup, find_packages

install_requires = \
    ['python-bittrex']

setup(
    name='python_bittrex_autosell',
    version='0.0.1',
    packages=['python_bittrex_autosell'],
    entry_points={
        "console_scripts": ['pba = python_bittrex_autosell.main:main']
    },
    install_requires=install_requires,
    url='https://github.com/slazarov/python_bittrex_autosell',
    license='MIT',
    author='slazarov',
    author_email='s.a.lazarov@gmail.com',
    description='Auto sell script for Bittrex Exchange for indirect markets.',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Financial and Insurance Industry',
        'Intended Audience :: Information Technology',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ]
)
