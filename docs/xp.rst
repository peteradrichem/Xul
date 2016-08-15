.. index::
   single: xp script
   single: scripts; xp
   single: XPath

xp -- Select nodes with XPath
=============================

.. index::
   single: XPath expression

Select nodes in an :ref:`xml_source` with XPath [#]_ expressions.

XPath expression
----------------
Set the XPath expression with the ``--xpath`` option.

List all the attributes of an XML file:

.. code:: bash

   xp --xpath="//@*" file.xml

Or use the short option ``-x``.

List the latest Python PEPs:

.. code:: bash

   curl -s https://www.python.org/dev/peps/peps.rss/ | \
   xp -x "//item/title/text()"

Options
-------
``xp`` supports the following command-line options:

.. code:: bash

   $ xp --help

   Usage:  xp [options] -x xpath xml_source ...

   Select nodes in an XML source with XPath expressions.

   Options:
     --version             show program's version number and exit
     -h, --help            show this help message and exit
     -x XPATH_EXP, --xpath=XPATH_EXP
                           XML Path Language (XPath) expression
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
Use the ``--result-xpath`` option to print the XPath expression of each result element.
The result XPath expression will have an absolute location path.

.. sourcecode:: bash

   xp --result-xpath --xpath="//title" file.xml

If the result is a text or attribute node ``xp`` will print the XPath expression of the parent element.

.. sourcecode:: bash

   xp -rx "//@*" file.xml


.. index::
   single: XML Namespaces
   single: Namespaces

Namespaces in XML
-----------------
List all the XML namespaces [#]_ (prefix, URI) of the document element:

.. code:: bash

   xp -x 'namespace::*' file.xml

The default namespace of the document element:

.. code:: bash

   xp -x 'namespace::*[name()=""]' file.xml

The default XML namespace has no prefix (*None*) in an XML document.
To select nodes in an XML namespace XPath uses prefixed names (qualified names).
``xp`` will use 'd' as the prefix for the default XML namespace.

List the five most recent Python Insider posts:

.. code:: bash

   xp -x "descendant::d:entry[position()<=5]/d:title/text()" \
   http://feeds.feedburner.com/PythonInsider

Change the prefix for the default namespace with the ``--default-prefix`` option:

.. code:: bash

   xp -d p -x "descendant::p:entry[position()<=5]/p:title/text()" \
   http://feeds.feedburner.com/PythonInsider


.. index::
   single: EXSLT
   single: Extensions to XSLT

Extensions to XSLT
------------------
lxml supports the EXSLT [#]_ extensions through libxslt (requires libxslt 1.1.25 or higher).
``xp`` will add the EXSLT namespaces with the ``--exslt`` command-line option.

Find Python Insider posts published in or after 2015 with EXSLT (``date`` prefix):

.. code:: bash

   xp -ex "//d:entry[date:year(d:published) >= '2015']/d:title/text()" \
   http://feeds.feedburner.com/PythonInsider

Python Insider posts updated in December:

.. code:: bash

   xp -ex "//d:entry[date:month-name(d:updated) = 'December']/d:title/text()" \
   http://feeds.feedburner.com/PythonInsider

Use the power of regular expression (``re`` prefix).
Find Python PEPs with "build" or "built" in the title (case-insensitive):

.. code:: bash

   curl -s https://www.python.org/dev/peps/peps.rss/ | \
   xp -ex '//item/title[re:match(text(), "buil(d|t)", "i")]'

Pretty print result
-------------------
A result element can be pretty printed with the ``--pretty-element`` command-line option.


.. rubric:: Footnotes

.. [#] `XML Path Language (XPath) 1.0 <http://www.w3.org/TR/xpath>`_
.. [#] `Namespaces in XML 1.0 <http://www.w3.org/TR/xml-names/>`_
.. [#] `Extensions to XSLT (EXSLT) <http://exslt.org/>`_
