====================
Xul -- XML Utilities
====================

.. image:: https://img.shields.io/pypi/pyversions/xul.svg
   :target: https://pypi.org/project/Xul/

.. image:: https://img.shields.io/pypi/v/xul
   :target: https://pypi.org/project/Xul/

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
The ``--help`` option displays the parameters of a script:

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

Pipe
----
You can redirect output (pipe) to a Xul script:

.. code::

        curl -s https://www.python.org/dev/peps/peps.rss/ | ppx

URL
---
libxml2_ supports loading XML through HTTP (and FTP).
For example, to pretty print an RSS feed:

.. code::

        ppx http://feeds.feedburner.com/PythonInsider

Loading XML through HTTPS is not supported and will result in an
*failed to load external entity* error.


XML standards
=============

W3C XML standards:

- `Extensible Markup Language (XML) 1.0 <http://www.w3.org/TR/xml/>`_
- `XML Schema 1.0 <http://www.w3.org/XML/Schema>`_
- `XSL Transformations (XSLT) 1.0 <http://www.w3.org/TR/xslt/>`_
- `XML Path Language (XPath) 1.0 <http://www.w3.org/TR/xpath/>`_
- `Namespaces in XML 1.0 <http://www.w3.org/TR/xml-names/>`_
- `Extensions to XSLT (EXSLT) <http://exslt.org/>`_


.. _Read The Docs: https://xul.readthedocs.io/
.. _lxml: http://lxml.de/
.. _libxml2: http://www.xmlsoft.org/
.. _libxslt: http://xmlsoft.org/libxslt/
.. _Pygments: https://pygments.org/
