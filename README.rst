====================
Xul -- XML Utilities
====================

.. image:: https://img.shields.io/pypi/pyversions/xul.svg
   :target: https://pypi.org/project/Xul/
   :alt: Python versions

.. image:: https://readthedocs.org/projects/xul/badge/?version=latest
   :target: https://xul.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

.. image:: https://img.shields.io/pypi/v/xul
   :target: https://pypi.org/project/Xul/
   :alt: PyPI version

Xul is a set of XML scripts written in Python.
Documentation can be found on `Read The Docs`_.


Xul scripts
===========

- ``ppx``: pretty print XML
- ``xp``: select nodes in XML source
- ``transform``: transform XML with XSLT
- ``validate``: validate an XML source

Installation
------------
The Xul command line scripts can be installed with **pip**:

.. code:: text

        $ pip install Xul

Install Pygments_ for XML syntax highlighting (optional).

.. code:: text

        $ pip install Pygments

Dependencies
------------
Xul uses the excellent lxml_ XML toolkit, a Pythonic binding for the C libraries
libxml2_ and libxslt_.

Options
-------
List the command-line options of a Xul script with ``--help``.
For example:

.. code::

   $ ppx --help

   usage: ppx [-h] [-V] [-n] [-o] [xml_source [xml_source ...]]

   Pretty Print XML source in human readable form.

   positional arguments:
   xml_source            XML source (file, <stdin>, http://...)

   optional arguments:
   -h, --help            show this help message and exit
   -V, --version         show program's version number and exit
   -n, --no-syntax       no syntax highlighting
   -o, --omit-declaration
                         omit the XML declaration

Documentation
=============
The Xul documentation can be found on `Read The Docs`_.

W3C standards
-------------
- `Extensible Markup Language (XML) 1.0 <http://www.w3.org/TR/xml/>`_
- `XML Schema 1.0 <http://www.w3.org/XML/Schema>`_
- `XSL Transformations (XSLT) 1.0 <http://www.w3.org/TR/xslt/>`_
- `XML Path Language (XPath) 1.0 <http://www.w3.org/TR/xpath/>`_
- `Namespaces in XML 1.0 <http://www.w3.org/TR/xml-names/>`_

Related
-------
- `Extensions to XSLT (EXSLT) <http://exslt.org/>`_
- `RELAX NG <https://relaxng.org/>`_


.. _Read The Docs: https://xul.readthedocs.io/
.. _lxml: http://lxml.de/
.. _libxml2: http://www.xmlsoft.org/
.. _libxslt: http://xmlsoft.org/libxslt/
.. _Pygments: https://pygments.org/
