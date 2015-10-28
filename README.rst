====================
Xul -- XML Utilities
====================

XML command-line scripts written in Python.

.. contents::

XML scripts
===========

- ``ppx``: pretty print XML source in human readable form.
- ``xp``: use XPath expression to select nodes in XML source(s).
- ``validate``: validate XML source with XSD or DTD.
- ``transform``: transform XML source with XSLT.

Requirements
------------

Xul uses the excellent lxml_ XML toolkit, a Pythonic binding for the C libraries
libxml2_ and libxslt_.

Installation
------------

Install the Xul scripts with **pip**:

.. code:: bash

        $ pip install hg+https://bitbucket.org/peteradrichem/xul

Install Pygments_ for XML syntax highlighting (optional).

.. code:: bash

        $ pip install Pygments

Options
-------

Use the ``--help`` option to print a script's command-line parameters:

.. code:: bash

        $ ppx --help

.. code::

        Usage:  ppx [-n] xml_source_1 ... xml_source_n

        Pretty Print XML source in human readable form.

        Options:
          --version             show program's version number and exit
          -h, --help            show this help message and exit
          -n, --no-syntax       no syntax highlighting
          -d, --disable-declaration
                                disable XML declaration


XML source
==========

The XML source can be a local file, a pipe or an URL.

File
----

Pretty print any local XML file with ``ppx``:

.. code::

        ppx data_dump.xml

Pipe
----
Redirect output (pipe) to a Xul script:

.. code::

        curl -s https://www.python.org/dev/peps/peps.rss/ | ppx

URL
---
libxml2_ also supports loading XML through HTTP (and FTP).
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


.. _lxml: http://lxml.de/
.. _libxml2: http://www.xmlsoft.org/
.. _libxslt: http://xmlsoft.org/libxslt/
.. _Pygments: http://pygments.org/
.. _XHTML: http://www.w3.org/TR/xhtml1
