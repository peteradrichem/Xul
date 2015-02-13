"""
Setup script for building XML scripts
"""

import codecs
from os import path
from setuptools import setup

here = path.abspath(path.dirname(__file__))

def long_description():
    """ Get the long description from the README.rst file """
    with codecs.open(path.join(here, 'README.rst'), encoding='utf-8') as f:
        return f.read()

setup(
    name="XML_scripts",
    version="2.0.0",
    description="XML (XPath, XSD, XSLT) scripts",
    author='Peter Adrichem',
    author_email='Peter.Adrichem@gmail.com',
    url='http://docu.npoict.nl/applicatiebeheer/documentatie/xml_scripts',

    scripts=['prettyprint.py', 'transform.py', 'validate.py', 'xpath.py'],
    zip_safe=False,
    install_requires=[
        "TAB>=0.9.19",
        "lxml>=2.0"
    ],

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
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Text Processing :: Markup :: XML',
        'Topic :: Utilities'
    ],
    keywords='xml xpath xslt xsd dtd',
    license='MIT',
    platforms='CPython',
    long_description=long_description(),
    download_url='https://bitbucket.org/peteradrichem/xml-scripts',
    bugtrack_url='https://bitbucket.org/peteradrichem/xml-scripts/issues'
)
