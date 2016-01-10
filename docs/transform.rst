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
     -x XSLT_SOURCE, --xslt=XSLT_SOURCE
                           XSLT source for transforming XML source(s)


Examples
--------

.. code:: bash

   transform -x xslt.xml file.xml


.. rubric:: Footnotes

.. [#] `XSL Transformations (XSLT) 1.0 <http://www.w3.org/TR/xslt>`_
