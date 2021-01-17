.. index::
   single: transform script
   single: scripts; transform
   single: XSLT
   single: Extensible Stylesheet Language Transformations

transform -- Transform XML
==========================
``transform`` is a simple command-line script to apply XSLT [#]_ stylesheets to
an :ref:`xml_source`.
If you need a command-line XSLT processor with more options have a look at
`xsltproc <http://xmlsoft.org/XSLT/xsltproc.html>`_

Transform an XML file:

.. code-block:: bash

   transform xsl_transform.xml file.xml

Transform an XML file and :doc:`pretty print <ppx>` the result:

.. code-block:: bash

   transform xsl_transform.xml file.xml | ppx

Options
-------
``transform`` can be used with the following command-line options:

.. code-block:: console

   $ transform --help

   usage: transform [-h] [-V] [-o] xslt_source [xml_source [xml_source ...]]

   Transform XML source with XSLT.

   positional arguments:
     xslt_source           XSLT source (file, http://...)
     xml_source            XML source (file, <stdin>, http://...)

   optional arguments:
     -h, --help            show this help message and exit
     -V, --version         show program's version number and exit
     -o, --omit-declaration
                           omit the XML declaration

.. index::
   single: transform script; XML declaration
   single: XML declaration; transform

XML declaration
---------------
XML documents should begin with an XML declaration which specifies the version of XML being used [#]_.

By default ``transform`` will print an (UTF-8) XML declaration.

.. program:: transform
.. option:: -o, --omit-declaration

You can omit the XML declaration with the ``--omit-declaration`` option.

.. code-block:: bash

   transform --omit-declaration xsl_transform.xml file.xml


.. rubric:: Footnotes

.. [#] `XSL Transformations (XSLT) 1.0 <https://www.w3.org/TR/xslt>`_
.. [#] Extensible Markup Language §2.8
   `Prolog and Document Type Declaration <https://www.w3.org/TR/xml/#sec-prolog-dtd>`_
