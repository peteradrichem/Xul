.. index::
   single: transform script
   single: scripts; transform
   single: XSLT
   single: Extensible Stylesheet Language Transformations

transform -- Transform XML with XSLT
====================================

Use ``transform`` to transform an :ref:`xml_source` with XSLT [#]_.

.. code:: bash

   transform --xslt=xslt.xml file.xml

Transform an XML file and :doc:`pretty print <ppx>` the result:

.. code:: bash

   transform -x xslt.xml file.xml | ppx

Options
-------

``transform`` supports the following command-line options:

.. code:: bash

   $ transform --help

   Usage: transform [-o] -x xslt_source xml_source ...

   Transform XML source with XSLT.

   Options:
     --version             show program's version number and exit
     -h, --help            show this help message and exit
     -x XSLT_SOURCE, --xslt=XSLT_SOURCE
                           XSLT source for transforming XML source(s)
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

   transform --omit-declaration -x xslt.xml file.xml


.. rubric:: Footnotes

.. [#] `XSL Transformations (XSLT) 1.0 <http://www.w3.org/TR/xslt>`_
.. [#] Extensible Markup Language §2.8
   `Prolog and Document Type Declaration <http://www.w3.org/TR/xml/#sec-prolog-dtd>`_
