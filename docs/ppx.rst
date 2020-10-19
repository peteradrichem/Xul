.. index::
   single: ppx script
   single: scripts; ppx
   single: pretty print

ppx -- Pretty Print XML
=======================
Use ``ppx`` to pretty print an :ref:`xml_source` in human readable form.

.. code-block:: bash

   ppx file.xml


.. _white_space:

.. index::
   single: white space

White Space
-----------
For greater readability ``ppx`` removes and adds *white space*.

.. warning:: White space can be significant in an XML document [#]_.
   So be careful when using ``ppx`` to rewrite XML files.


Options
-------
``ppx`` can be used with the following command-line options:

.. code-block:: console

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


.. index::
   single: ppx script; syntax highlighting
   single: syntax highlighting

Syntax Highlighting
-------------------
``ppx`` will syntax highlight the XML source if you have Pygments_ installed.

Pretty print the XML Schema 1.0 schema document:

.. code-block:: bash

   ppx http://www.w3.org/2001/XMLSchema.xsd

.. program:: ppx
.. option:: -n, --no-syntax

You can disable syntax highlighting with the ``--no-syntax`` option.


.. index::
   single: ppx script; XML declaration
   single: XML declaration
   single: XML declaration; ppx

XML declaration
---------------
XML documents should begin with an XML declaration which specifies the version of XML being used [#]_.

By default ``ppx`` will print an (UTF-8) XML declaration.

.. program:: ppx
.. option:: -o, --omit-declaration

Omit the XML declaration with the ``--omit-declaration`` option.

.. code-block:: bash

   ppx --omit-declaration file.xml

Examples
--------
Pretty print any local XML file:

.. code-block:: bash

   ppx data_dump.xml

RSS feed:

.. code-block:: bash

   ppx http://feeds.feedburner.com/PythonInsider

Page XML file with less:

.. code-block:: bash

   ppx xml/large.xml | less -RX

Redirect output (pipe) to ``ppx``:

.. code-block:: bash

   curl -s https://www.python.org/dev/peps/peps.rss/ | ppx

:ref:`Rewrite XML <white_space>`:

.. code-block:: bash

   ppx -n data_dump.xml > pp_data_dump.xml


.. _Pygments: https://pygments.org/


.. rubric:: Footnotes

.. [#] Extensible Markup Language §2.10
   `White Space Handling <https://www.w3.org/TR/xml/#sec-white-space>`_
.. [#] Extensible Markup Language §2.8
   `Prolog and Document Type Declaration <https://www.w3.org/TR/xml/#sec-prolog-dtd>`_
