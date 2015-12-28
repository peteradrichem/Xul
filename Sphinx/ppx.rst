ppx -- Pretty Print XML
=======================

Use ``ppx`` to pretty print an XML source in human readable form.

.. code:: bash

   ppx file.xml


White Space
-----------

For greater readability ``ppx`` prints extra *white space*.
However white space can be significant so don't use ``ppx`` to rewrite XML files
unless you know what you are doing.

W3C: `2.10 White Space Handling <http://www.w3.org/TR/xml/#sec-white-space>`_


Options
-------

``ppx`` supports the following command-line options:

.. code:: bash

   ppx --help

.. code::

   Usage:  ppx [-n] xml_source_1 ... xml_source_n

   Pretty Print XML source in human readable form.

   Options:
     --version             show program's version number and exit
     -h, --help            show this help message and exit
     -n, --no-syntax       no syntax highlighting
     -d, --disable-declaration
                           disable XML declaration

Syntax Highlighting
-------------------
``ppx`` will syntax highlight the XML source if you have Pygments_ installed.

You can disable syntax highlighting with the ``--no-syntax`` option.

XML declaration
---------------

XML documents should begin with an XML declaration which specifies the version of XML being used.

W3C `2.8 Prolog and Document Type Declaration <http://www.w3.org/TR/xml/#sec-prolog-dtd>`_

By default ``ppx`` will print an (UTF-8) XML declaration.
Disable XML declaration printing with the ``--disable-declaration`` option.

Examples
--------

Pretty print any local XML file:

.. code::

   ppx data_dump.xml

RSS feed:

.. code::

   ppx http://feeds.feedburner.com/PythonInsider

Redirect output (pipe) to ``ppx``:

.. code::

   curl -s https://www.python.org/dev/peps/peps.rss/ | ppx


.. _Pygments: http://pygments.org/
