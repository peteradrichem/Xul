.. index::
   single: xp script
   single: scripts; xp
   single: XPath

xp -- Select nodes with XPath
=============================

.. index::
   single: XPath expression

XPath expression
----------------
Select nodes in an :ref:`xml_source` with an XPath [#]_ expression.

List all attributes of an XML file:

.. code:: bash

   xp "//@*" file.xml

List the latest Python PEPs:

.. code:: bash

   curl -s https://www.python.org/dev/peps/peps.rss/ | \
   xp "//item/title/text()"

Options
-------
``xp`` supports the following command-line options:

.. code:: bash

   $ xp --help

   Usage:  xp xpath_expr [options] xml_source ...

   Select nodes in an XML source with an XPath expression.

   Options:
     --version             show program's version number and exit
     -h, --help            show this help message and exit
     -e, --exslt           add EXSLT XML namespace prefixes
     -d DEFAULT_NS_PREFIX, --default-prefix=DEFAULT_NS_PREFIX
                           set the prefix for the default namespace in XPath
                           [default: 'd']
     -r, --result-xpath    print the XPath expression of the result element (or
                           its parent)
     -p, --pretty-element  pretty print the result element
     -m, --method          use ElementTree.xpath method instead of XPath class

Print result's XPath
--------------------
Print the XPath expression of each result element with the ``--result-xpath`` option.
Each XPath expression will have an absolute location path.

.. sourcecode:: bash

   xp --result-xpath "//title" file.xml

If an XPath result is a text or attribute node ``xp`` will print the parent element's
XPath expression.

List the XPath expressions of all elements with attributes:

.. sourcecode:: bash

   xp -r "//@*" file.xml


.. index::
   single: XML Namespaces
   single: Namespaces

Namespaces in XML
-----------------
List all the XML namespaces [#]_ (prefix, URI) of the document element:

.. code:: bash

   xp 'namespace::*' file.xml

Print the default namespace of the document element, if it has one:

.. code:: bash

   xp 'namespace::*[name()=""]' file.xml

The default XML namespace in an XML document has no prefix (*None*).
To select nodes in an XML namespace XPath uses prefixed names (qualified names).
``xp`` will use 'd' as the prefix for the default XML namespace.

List the five most recent Python Insider posts:

.. code:: bash

   xp "descendant::d:entry[position()<=5]/d:title/text()" \
   http://feeds.feedburner.com/PythonInsider

Change the prefix for the default namespace with the ``--default-prefix`` option:

.. code:: bash

   xp -d p "descendant::p:entry[position()<=5]/p:title/text()" \
   http://feeds.feedburner.com/PythonInsider


.. index::
   single: EXSLT
   single: Extensions to XSLT

Extensions to XSLT
------------------
lxml supports the EXSLT [#]_ extensions through libxslt (requires libxslt 1.1.25 or higher).
``xp`` will add EXSLT namespaces with the ``--exslt`` command-line option.

Find Python Insider posts published in or after 2015 with EXSLT (``date`` prefix):

.. code:: bash

   xp -e "//d:entry[date:year(d:published) >= '2015']/d:title/text()" \
   http://feeds.feedburner.com/PythonInsider

Python Insider posts updated in December:

.. code:: bash

   xp -e "//d:entry[date:month-name(d:updated) = 'December']/d:title/text()" \
   http://feeds.feedburner.com/PythonInsider

Use the power of regular expression (``re`` prefix).
Find Python PEPs with "build" or "built" in the title (case-insensitive):

.. code:: bash

   curl -s https://www.python.org/dev/peps/peps.rss/ | \
   xp -e '//item/title[re:match(text(), "buil(d|t)", "i")]'

Pretty print result
-------------------
A result element can be pretty printed with the ``--pretty-element`` command-line option.

xpath method
------------
``xp`` uses `lxml.etree.XPath` class by default. You can choose the
`lxml.etree.ElementTree.xpath` method with the ``--method`` command-line option.
The results should be the same but error reporting can be different.


.. rubric:: Footnotes

.. [#] `XML Path Language (XPath) 1.0 <http://www.w3.org/TR/xpath>`_
.. [#] `Namespaces in XML 1.0 <http://www.w3.org/TR/xml-names/>`_
.. [#] `Extensions to XSLT (EXSLT) <http://exslt.org/>`_
