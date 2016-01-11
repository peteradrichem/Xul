.. index::
   single: transform
   single: scripts; transform

transform -- Transform XML with XSLT
====================================

.. index::
   single: XSLT
   single: Extensible Stylesheet Language Transformations

Use ``transform`` to transform an :ref:`xml_source` with XSLT [#]_.


Options
-------

``transform`` supports the following command-line options:

.. code:: bash

   $ transform --help

   Usage: transform -x xslt_source xml_source ...

   Transform XML source with XSLT.

   Options:
     --version             show program's version number and exit
     -h, --help            show this help message and exit
     -o, --omit-declaration
                           omit the XML declaration
     -x XSLT_SOURCE, --xslt=XSLT_SOURCE
                           XSLT source for transforming XML source(s)


XML declaration
---------------

XML documents should begin with an XML declaration which specifies the version of XML being used [#]_.

By default ``transform`` will print an (UTF-8) XML declaration.
Omit the XML declaration with the ``--omit-declaration`` option.


Examples
--------

.. code:: bash

   transform -x xslt.xml file.xml


.. rubric:: Footnotes

.. [#] `XSL Transformations (XSLT) 1.0 <http://www.w3.org/TR/xslt>`_
.. [#] Extensible Markup Language §2.8
   `Prolog and Document Type Declaration <http://www.w3.org/TR/xml/#sec-prolog-dtd>`_
