# -*- coding: utf-8 -*-

"""Setup script for building XML Utilities."""

import codecs
from os import path
from setuptools import setup, find_packages
from xul import __version__

here = path.abspath(path.dirname(__file__))

def long_description():
    """Get the long description from the README.rst file."""
    with codecs.open(path.join(here, 'README.rst'), encoding='utf-8') as f:
        return f.read()

setup(
    name="Xul",
    version=__version__,

    packages=find_packages(),
    zip_safe=False,
    install_requires=["lxml>=2.0"],

    author='Peter Adrichem',
    author_email='Peter.Adrichem@gmail.com',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Text Processing :: Markup :: XML',
        'Topic :: Utilities'
    ],
    description="XML (XPath, XSD, XSLT) Utilities",
    keywords='xml xpath xslt xsd dtd',
    license='MIT',
    long_description=long_description(),
    platforms='CPython',
    url='https://xul.readthedocs.io/',
    download_url='https://bitbucket.org/peteradrichem/xul',
    entry_points={
        'console_scripts': [
            'transform = xul.cmd.transform:main',
            'ppx = xul.cmd.ppx:main',
            'xp = xul.cmd.xp:main',
            'validate = xul.cmd.validate:main'
            ]
    }
)
