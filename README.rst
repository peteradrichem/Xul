====================
Xul -- XML Utilities
====================

.. image:: https://img.shields.io/pypi/v/xul
   :target: https://pypi.org/project/Xul/
   :alt: PyPI version

.. image:: https://img.shields.io/pypi/wheel/xul.svg
   :target: https://pypi.org/project/Xul/
   :alt: Wheel

.. image:: https://img.shields.io/pypi/pyversions/xul.svg
   :target: https://pypi.org/project/Xul/
   :alt: Python versions

.. image:: https://img.shields.io/pypi/l/xul.svg
   :target: https://pypi.org/project/Xul/
   :alt: License

.. image:: https://readthedocs.org/projects/xul/badge/
   :target: https://xul.readthedocs.io/en/stable/
   :alt: Documentation

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
   :alt: Black code style

.. image:: https://img.shields.io/badge/type%20checked-mypy-039dfc
   :target: https://mypy-lang.org
   :alt: Typing checked by mypy

.. image:: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json
   :target: https://astral.sh/ruff
   :alt: Ruff linting

.. image:: https://img.shields.io/badge/imports-isort-1674b1
   :target: https://pycqa.github.io/isort/
   :alt: Imports sorted by isort

.. image:: https://github.com/peteradrichem/Xul/actions/workflows/code-checks.yml/badge.svg
   :target: https://github.com/peteradrichem/Xul/actions/workflows/code-checks.yml
   :alt: Code checks


Xul scripts
===========
Xul is a set of XML scripts written in Python.

- ``ppx``: pretty print XML
- ``xp``: select XML nodes with XPath
- ``transform``: transform XML with XSLT
- ``validate``: validate XML with XSD, DTD or RELAX NG

Installation
------------
Xul command line scripts can be installed with pip:

.. code:: text

        $ pip install Xul

Install Pygments_ for XML syntax highlighting (optional).

.. code:: text

        $ pip install Xul[syntax]

Dependencies
------------
Xul uses the excellent lxml_ XML toolkit, a Pythonic binding for the C libraries
libxml2_ and libxslt_.

Documentation
=============
Xul documentation can be found on `Read The Docs`_.

Options
-------
List the command-line options of a Xul script with ``--help``.
For example:

.. code-block:: console

   $ xp --help

   usage: xp [-h] [-V] [-l | -L] [-d DEFAULT_NS_PREFIX] [-e] [-q] [-c | -p] [-r] [-m] xpath_expr [xml_source ...]

   Select nodes in an XML source with an XPath expression.

   positional arguments:
     xpath_expr            XPath expression
     xml_source            XML source (file, <stdin>, http://...)

   options:
     -h, --help            show this help message and exit
     -V, --version         show program's version number and exit
     -m, --method          use ElementTree.xpath method instead of XPath class

   file hit options:
     output filenames to standard output

     -l, -f, --files-with-hits
                           only names of files with a result that is not false and
                           not NaN are written to standard output
     -L, -F, --files-without-hits
                           only names of files with a false or NaN result, or without a result,
                           are written to standard output

   namespace options:
     -d DEFAULT_NS_PREFIX, --default-prefix DEFAULT_NS_PREFIX
                           set the prefix for the default namespace in XPath [default: 'd']
     -e, --exslt           add EXSLT XML namespaces
     -q, --quiet           don't print XML source namespaces

   element output options:
     -c, --count           only print the number of selected nodes
     -p, --pretty-element  pretty print the result element
     -r, --result-xpath    print the XPath expression of the result element (or its parent)


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
