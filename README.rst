====================
Xul -- XML Utilities
====================

.. contents::

Xul scripts
===========

XML utilities written in Python.

- ``ppx``: pretty print XML
- ``xp``: select nodes in XML source
- ``transform``: transform XML with XSLT
- ``validate``: validate an XML source

Installation
------------
The Xul command line scripts can be installed with **pip**:

.. code:: bash

        $ pip install Xul

Install Pygments_ for XML syntax highlighting (optional).

.. code:: bash

        $ pip install Pygments

Dependencies
------------
Xul uses the excellent lxml_ XML toolkit, a Pythonic binding for the C libraries
libxml2_ and libxslt_.

Options
-------
Use the ``--help`` option to print a command line script's parameters:

.. code::

        $ ppx --help

        Usage:  ppx [-nr] xml_source_1 ... xml_source_n

        Pretty Print XML source in human readable form.

        Options:
          --version             show program's version number and exit
          -h, --help            show this help message and exit
          -n, --no-syntax       no syntax highlighting
          -r, --remove-declaration
                                remove the XML declaration


XML source
==========

An XML source can be a local file, an URL or a pipe.

File
----

Pretty print any local XML file with ``ppx``:

.. code::

        ppx data_dump.xml

URL
---
libxml2_ also supports loading XML through HTTP (and FTP).
For example, to pretty print an RSS feed:

.. code::

        ppx http://feeds.feedburner.com/PythonInsider

Loading XML through HTTPS is not supported and will result in an
*failed to load external entity* error.

Pipe
----
Redirect output (pipe) to a Xul script:

.. code::

        curl -s https://www.python.org/dev/peps/peps.rss/ | ppx


XML standards
=============

W3C XML standards:

- `Extensible Markup Language (XML) 1.0 <http://www.w3.org/TR/xml/>`_
- `XML Schema 1.0 <http://www.w3.org/XML/Schema>`_
- `XSL Transformations (XSLT) 1.0 <http://www.w3.org/TR/xslt/>`_
- `XML Path Language (XPath) 1.0 <http://www.w3.org/TR/xpath/>`_
- `Namespaces in XML 1.0 <http://www.w3.org/TR/xml-names/>`_


.. _lxml: http://lxml.de/
.. _libxml2: http://www.xmlsoft.org/
.. _libxslt: http://xmlsoft.org/libxslt/
.. _Pygments: http://pygments.org/
.. _XHTML: http://www.w3.org/TR/xhtml1
