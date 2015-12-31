transform -- Transform with XSLT
================================

Use ``transform`` to transform an XML source with `XSLT <http://www.w3.org/TR/xslt/>`_.


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
