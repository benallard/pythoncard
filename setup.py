# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

version = '1.0'

setup(
    name='JavaCard',    # unfortunately, I'm not the first on PythonCard
    version=version,
    author='Benoît Allard',
    author_email='benoit.allard@gmx.de',
    description='A pure Python implementation of the JavaCard framework',
    long_description=open('README.rst').read(), 
    url='https://bitbucket.org/benallard/pythoncard',
    packages=find_packages(exclude=['test', 'pyDes']),
    install_requires=['pyDes', 'PyCrypto'],
    license='LGPL',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
        'Programming Language :: Python :: 2',
        'Topic :: Software Development :: Libraries :: Python Modules',
      ],
      keywords='java smartcard javacard sun',
)
