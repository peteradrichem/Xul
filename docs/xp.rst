.. index::
   single: xp
   single: scripts; xp

xp -- Select nodes with XPath
=============================

.. index::
   single: XPath

Use XPath [#]_ expressions to select nodes in an :ref:`xml_source`.

List the latest Python PEPs:

.. code:: bash

   curl -s https://www.python.org/dev/peps/peps.rss/ | xp -x "//item/title/text()"

Options
-------

``xp`` supports the following command-line options:

.. code:: bash

   $ xp --help

   Usage:  xp [options] -x xpath xml_source ...

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
     -p, --print-xpath     print the absolute XPath of a result (or its parent)
     -l, --pretty-element  pretty print the result element
     -m, --method          use ElementTree.xpath method instead of XPath class

Namespaces in XML
-----------------

.. index::
   single: Namespaces

The default namespace of the document element:

.. code:: bash

   xp -x 'namespace::*[name()=""]' file.xml

There is no prefix for the default namespace.

List all document element namespaces (prefix, URI):

.. code:: bash

   xp -x 'namespace::*' file.xml

To select nodes in an XML namespace [#]_ XPath uses prefixed names (qualified names).
``xp`` uses 'd' for the default namespace prefix.

The five most recent Python Insider posts:

.. code:: bash

   xp -x "descendant::d:entry[position()<=5]/d:title/text()" http://feeds.feedburner.com/PythonInsider

You can change the prefix for the default namespace with the ``--default-prefix`` option.

Extensions to XSLT
------------------

.. index::
   single: EXSLT
   single: Extensions to XSLT

lxml has support for EXSLT [#]_ (requires libxslt 1.1.25 or higher).

Python Insider posts published in 2015 (EXSLT ``date`` prefix):

.. code:: bash

   xp -ex "//d:entry[date:year(d:published) >= '2015']/d:title/text()" http://feeds.feedburner.com/PythonInsider

Python Insider posts updated in December:

.. code:: bash

   xp -ex "//d:entry[date:month-name(d:updated) = 'December']/d:title/text()" http://feeds.feedburner.com/PythonInsider

Python PEPs about "build" or "built" (EXSLT ``re`` prefix):

.. code:: bash

   curl -s https://www.python.org/dev/peps/peps.rss/ | xp -ex '//item/title/text()[re:match(., "buil(d|t)", "i")]'


.. rubric:: Footnotes

.. [#] `XML Path Language (XPath) 1.0 <http://www.w3.org/TR/xpath>`_
.. [#] `Namespaces in XML 1.0 <http://www.w3.org/TR/xml-names/>`_
.. [#] `Extensions to XSLT (EXSLT) <http://exslt.org/>`_
