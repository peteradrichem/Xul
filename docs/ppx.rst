.. index::
   single: ppx
   single: scripts; ppx

ppx -- Pretty Print XML
=======================

Use ``ppx`` to pretty print an :ref:`xml_source` in human readable form.

.. code:: bash

   ppx file.xml


.. _white_space:

.. index::
   single: white space

White Space
-----------

For greater readability ``ppx`` adds extra *white space*.

.. note:: White space can be significant in an XML document [#]_.
   So be careful with using ``ppx`` to rewrite XML files.

Options
-------

``ppx`` supports the following command-line options:

.. code:: bash

   $ ppx --help

   Usage:  ppx [-no] xml_source ...

   Pretty Print XML source in human readable form.

   Options:
     --version             show program's version number and exit
     -h, --help            show this help message and exit
     -n, --no-syntax       no syntax highlighting
     -o, --omit-declaration
                           omit the XML declaration


.. index::
   single: syntax highlighting

Syntax Highlighting
-------------------
``ppx`` will syntax highlight the XML source if you have Pygments_ installed.

You can disable syntax highlighting with the ``--no-syntax`` option.


.. index::
   single: XML declaration

XML declaration
---------------

XML documents should begin with an XML declaration which specifies the version of XML being used [#]_.

By default ``ppx`` will print an (UTF-8) XML declaration.
Omit the XML declaration with the ``--omit-declaration`` option.

Examples
--------

Pretty print any local XML file:

.. code:: bash

   ppx data_dump.xml

RSS feed:

.. code:: bash

   ppx http://feeds.feedburner.com/PythonInsider

Redirect output (pipe) to ``ppx``:

.. code:: bash

   curl -s https://www.python.org/dev/peps/peps.rss/ | ppx

:ref:`Rewrite XML <white_space>`:

.. code:: bash

   ppx -n data_dump.xml > pp_data_dump.xml


.. _Pygments: http://pygments.org/


.. rubric:: Footnotes

.. [#] Extensible Markup Language §2.10
   `White Space Handling <http://www.w3.org/TR/xml/#sec-white-space>`_
.. [#] Extensible Markup Language §2.8
   `Prolog and Document Type Declaration <http://www.w3.org/TR/xml/#sec-prolog-dtd>`_
