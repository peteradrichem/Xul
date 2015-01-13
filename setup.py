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
    name="XML scripts",
    version="2.0.0",

    scripts=['prettyprint.py', 'transform.py', 'validate.py', 'xpath.py'],
    zip_safe=False,
    install_requires=[
        "TAB>=0.9.19",
        "lxml"
    ],

    # Metadata (for upload to PyPI)
    author='Peter Adrichem',
    author_email='Peter.Adrichem@gmail.com',
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Topic :: Text Processing :: Markup :: XML",
        "Topic :: Utilities"
    ],
    description="XML scripts",
    keywords='xml xpath xslt xsd dtd',
    license='BSD',
    long_description=long_desc,
    platforms='any',
    url='http://docu.npoict.nl/applicatiebeheer/documentatie/xml_scripts',
    download_url='https://bitbucket.org/peteradrichem/xml-scripts'
)
