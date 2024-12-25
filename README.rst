====================
Xul -- XML Utilities
====================

.. image:: https://img.shields.io/pypi/pyversions/xul.svg
   :target: https://pypi.org/project/Xul/
   :alt: Python versions

.. image:: https://img.shields.io/pypi/l/xul.svg
   :target: https://pypi.org/project/Xul/
   :alt: License

.. image:: https://img.shields.io/pypi/v/xul
   :target: https://pypi.org/project/Xul/
   :alt: PyPI version

.. image:: https://img.shields.io/pypi/wheel/xul.svg
   :target: https://pypi.org/project/Xul/
   :alt: Wheel

.. image:: https://readthedocs.org/projects/xul/badge/
   :target: https://xul.readthedocs.io/en/stable/
   :alt: Documentation

Xul is a set of XML scripts written in Python.
Documentation can be found on `Read The Docs`_.


Xul scripts
===========

- ``ppx``: pretty print XML
- ``xp``: select XML nodes with XPath
- ``transform``: transform XML with XSLT
- ``validate``: validate XML with XSD, DTD or RELAX NG

Installation
------------
Xul command line scripts can be installed with **pip**:

.. code:: text

        $ pip install Xul

Install Pygments_ for XML syntax highlighting (optional).

.. code:: text

        $ pip install Xul[syntax]

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
Xul documentation can be found on `Read The Docs`_.

W3C standards
-------------
- `Extensible Markup Language (XML) 1.0 <https://www.w3.org/TR/xml/>`_
- `XML Schema 1.1 <https://www.w3.org/XML/Schema>`_
- `XSL Transformations (XSLT) 1.0 <https://www.w3.org/TR/xslt-10/>`_
- `XML Path Language (XPath) 1.0 <https://www.w3.org/TR/xpath-10/>`_
- `Namespaces in XML 1.0 <https://www.w3.org/TR/xml-names/>`_

Related
-------
- `Extensions to XSLT (EXSLT) <https://exslt.github.io/>`_
- `RELAX NG <https://relaxng.org/>`_


.. _Read The Docs: https://xul.readthedocs.io/
.. _lxml: https://lxml.de/
.. _libxml2: https://gitlab.gnome.org/GNOME/libxml2/-/wikis/
.. _libxslt: https://gitlab.gnome.org/GNOME/libxslt/-/wikis/
.. _Pygments: https://pygments.org/
