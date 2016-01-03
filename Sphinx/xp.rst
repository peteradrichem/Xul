.. index::
   single: xp
   single: scripts; xp

xp -- Select nodes in XML source
================================

.. index::
   single: XPath

Use `XPath expressions <http://www.w3.org/TR/xpath/>`_ to select nodes in XML source.


Options
-------

``xp`` supports the following command-line options:

.. code:: bash

   $ xp --help

   Usage:  xp [options] -x xpath xml_source_1 ... xml_source_n

   Use XPath expression to select nodes in XML source.

   Options:
     --version             show program's version number and exit
     -h, --help            show this help message and exit
     -x XPATH_EXP, --xpath=XPATH_EXP
                           XML Path Language (XPath) expression
     -e, --exslt           add EXSLT XML namespace prefixes
     -d DEFAULT_NS_PREFIX, --default-prefix=DEFAULT_NS_PREFIX
                           set the prefix for the default namespace in XPath
                           [default: 'd']
     -p, --print-xpath     print the absolute XPath of a result (or parent)
                           element
     -t, --element-tree    print the XML tree of a result element
     -m, --method          use ElementTree.xpath method instead of XPath class

Examples
--------

.. code:: bash

   xp -x "//d:title/text()" http://feeds.feedburner.com/PythonInsider
