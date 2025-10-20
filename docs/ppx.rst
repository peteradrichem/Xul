.. index::
   single: ppx script
   single: scripts; ppx
   single: pretty print

=======================
ppx -- Pretty Print XML
=======================
``ppx`` pretty prints an :ref:`xml_source` in human readable form.

Examples
========
``ppx`` will try to use the character encoding of your terminal and defaults to UTF-8.

Pretty print any local XML file:

.. code-block:: bash

   ppx file.xml

Page a syntax hightlighted XML file with less:

.. code-block:: bash

   ppx xml/large.xml | less -RX

Redirect output (pipe) to ``ppx``:

.. code-block:: bash

   curl -s https://peps.python.org/peps.rss | ppx

Pretty print an RSS feed:

.. code-block:: bash

   curl -s https://feeds.feedburner.com/PythonInsider | ppx

Options
=======
``ppx`` can be used with the following command-line options:

.. code-block:: console

   $ ppx --help

   usage: ppx [-h] [-V] [-n] [-o] [xml_source ...]

   Pretty Print XML source in human readable form.

   positional arguments:
     xml_source            XML source (file, <stdin>, http://...)

   options:
     -h, --help            show this help message and exit
     -V, --version         show program's version number and exit

   output options:
     -n, --no-syntax       no syntax highlighting
     -o, --omit-declaration
                           omit the XML declaration


.. _white_space:

.. index::
   single: white space
   single: rewrite XML

White Space
===========
For greater readability ``ppx`` removes and adds *white space*.

Rewrite an XML file:

.. code-block:: bash

   ppx -n data_dump.xml > pp_data_dump.xml

.. warning:: White space can be significant in an XML document [#]_.

So be careful when using ``ppx`` to rewrite XML files.


Output options
==============
``ppx`` terminal output options.


.. index::
   single: ppx script; syntax highlighting
   single: syntax highlighting; ppx

Syntax Highlighting
-------------------
``ppx`` will syntax highlight the XML source if you have Pygments_ installed.

Pretty print the XML Schema 1.0 schema document:

.. code-block:: bash

   ppx http://www.w3.org/2001/XMLSchema.xsd

.. program:: ppx
.. option:: -n, --no-syntax

You can disable syntax highlighting with the ``--no-syntax`` option:

.. code-block:: bash

   ppx --no-syntax http://www.w3.org/2001/XMLSchema.xsd


.. index::
   single: ppx script; XML declaration
   single: XML declaration; ppx

XML declaration
---------------
XML documents should begin with an XML declaration which specifies the version of XML being used [#]_.

By default ``ppx`` will print an (UTF-8) XML declaration.

.. program:: ppx
.. option:: -o, --omit-declaration

Omit the XML declaration with the ``--omit-declaration`` option:

.. code-block:: bash

   ppx --omit-declaration file.xml


.. _Pygments: https://pygments.org/


.. rubric:: Footnotes

.. [#] Extensible Markup Language §2.10
   `White Space Handling <https://www.w3.org/TR/xml/#sec-white-space>`_
.. [#] Extensible Markup Language §2.8
   `Prolog and Document Type Declaration <https://www.w3.org/TR/xml/#sec-prolog-dtd>`_
