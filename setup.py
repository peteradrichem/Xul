"""
Setup script for building XML scripts
"""

from setuptools import setup

long_desc = """**XML scripts**
Pretty print XML files in human readable form,
Use XPath expression to select nodes in XML file,
Transform XML files with XSL,
Validate XML files with a XSD or DTD"""

setup(
    name="XML_scripts",
    version="2.0.0",
    description="XML scripts",
    author='Peter Adrichem',
    author_email='Peter.Adrichem@gmail.com',
    url='http://docu.npoict.nl/applicatiebeheer/documentatie/xml_scripts',

    scripts=['prettyprint.py', 'transform.py', 'validate.py', 'xpath.py'],
    zip_safe=False,
    install_requires=[
        "TAB>=0.9.19",
        "lxml"
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
    long_description=long_desc,
    download_url='https://bitbucket.org/peteradrichem/xml-scripts',
    #bugtrack_url='https://bitbucket.org/peteradrichem/xml-scripts/issues'
)
