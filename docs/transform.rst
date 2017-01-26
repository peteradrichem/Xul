.. index::
   single: transform script
   single: scripts; transform
   single: XSLT
   single: Extensible Stylesheet Language Transformations

transform -- Transform XML with XSLT
====================================

``transform`` is a simple command line script to apply XSLT [#]_ stylesheets to
an :ref:`xml_source`.
If you need a command line XSLT processor with more options have a look at
`xsltproc <http://xmlsoft.org/XSLT/xsltproc.html>`_

Transform an XML file:

.. code:: bash

   transform xsl_transform.xml file.xml

Transform an XML file and :doc:`pretty print <ppx>` the result:

.. code:: bash

   transform xsl_transform.xml file.xml | ppx

Options
-------

``transform`` supports the following command-line options:

.. code:: bash

   $ transform --help

   Usage: transform xslt_source [-o] xml_source ...

   Transform XML source with XSLT.

   Options:
     --version             show program's version number and exit
     -h, --help            show this help message and exit
     -o, --omit-declaration
                           omit the XML declaration

.. index::
   single: XML declaration; transform

XML declaration
---------------

XML documents should begin with an XML declaration which specifies the version of XML being used [#]_.

By default ``transform`` will print an (UTF-8) XML declaration.
You can omit the XML declaration with the ``--omit-declaration`` option.

.. code:: bash

   transform --omit-declaration xsl_transform.xml file.xml


.. rubric:: Footnotes

.. [#] `XSL Transformations (XSLT) 1.0 <http://www.w3.org/TR/xslt>`_
.. [#] Extensible Markup Language §2.8
   `Prolog and Document Type Declaration <http://www.w3.org/TR/xml/#sec-prolog-dtd>`_
