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

.. code-block:: bash

   xp "//@*" file.xml

List the latest Python PEPs:

.. code-block:: bash

   curl -s https://peps.python.org/peps.rss | xp "//item/title/text()"

List the latest Python PEPs with their link:

.. code-block:: bash

   curl -s https://peps.python.org/peps.rss | \
   xp "//item/*[name()='title' or name()='link']/text()"

Options
-------
``xp`` can be used with the following command-line options:

.. code-block:: console

   $ xp --help

   usage: xp [-h] [-V] [-e] [-d DEFAULT_NS_PREFIX] [-q] [-p] [-r] [-f | -F] [-m] xpath_expr [xml_source ...]

   Select nodes in an XML source with an XPath expression.

   positional arguments:
   xpath_expr            XPath expression
   xml_source            XML source (file, <stdin>, http://...)

   options:
   -h, --help            show this help message and exit
   -V, --version         show program's version number and exit
   -e, --exslt           add EXSLT XML namespaces
   -d DEFAULT_NS_PREFIX, --default-prefix DEFAULT_NS_PREFIX
                         set the prefix for the default namespace in XPath [default: 'd']
   -q, --quiet           don't print XML source namespaces
   -p, --pretty-element  pretty print the result element
   -r, --result-xpath    print the XPath expression of the result element (or its parent)
   -f, -l, --files-with-hits
                         only the names of files with a non-false and non-NaN result are written to standard output
   -F, -L, --files-without-hits
                         only the names of files with a false or NaN result, or without any results are written to
                         standard output
   -m, --method          use ElementTree.xpath method instead of XPath class


.. index::
   single: xp script; result XPath

Print result's XPath
--------------------
.. program:: xp
.. option:: -r, --result-xpath

Print the XPath expression of each result element with the ``--result-xpath`` option.
Each XPath expression will have an absolute location path.

.. code-block:: bash

   xp --result-xpath "//title" file.xml

If an XPath result is a text or attribute node ``xp`` prints the parent element's
XPath expression.

List the XPath expressions of all elements with attributes:

.. code-block:: bash

   xp -r "//@*" file.xml


.. index::
   single: xp script; namespaces
   single: XML Namespaces
   single: Namespaces

Namespaces in XML
-----------------
List all the XML namespaces [#]_ (prefix, URI) of the document element:

.. code-block:: bash

   xp 'namespace::*' file.xml

Print the default namespace of the document element, if it has one:

.. code-block:: bash

   xp 'namespace::*[name()=""]' file.xml

The default XML namespace in an XML document has no prefix (*None*).
To select nodes in an XML namespace XPath needs prefixed names (qualified names).
Therefore ``xp`` uses ``d`` as the prefix for the default XML namespace.

List the five most recent Python Insider posts:

.. code-block:: bash

   xp "descendant::d:entry[position()<=5]/d:title/text()" \
   http://feeds.feedburner.com/PythonInsider

.. program:: xp
.. option:: -d <prefix>, --default-prefix <prefix>

You can change the prefix for the default namespace with the ``--default-prefix`` option:

.. code-block:: bash

   xp -d p "descendant::p:entry[position()<=5]/p:title/text()" \
   http://feeds.feedburner.com/PythonInsider


.. index::
   single: xp script; EXSLT
   single: EXSLT
   single: Extensions to XSLT

Extensions to XSLT
------------------
.. program:: xp
.. option:: -e, --exslt

lxml supports the EXSLT [#]_ extensions through libxslt (requires libxslt 1.1.25 or higher). Add EXSLT namespaces with the ``--exslt`` command-line option.

Find Python Insider posts published in or after 2015 with EXSLT (``date`` prefix):

.. code-block:: bash

   xp -e "//d:entry[date:year(d:published) >= '2015']/d:title/text()" \
   http://feeds.feedburner.com/PythonInsider

Python Insider posts updated in December:

.. code-block:: bash

   xp -e "//d:entry[date:month-name(d:updated) = 'December']/d:title/text()" \
   http://feeds.feedburner.com/PythonInsider

.. index::
   single: xp script; quiet

.. program:: xp
.. option:: -q, --quiet

The ``--quiet`` command-line option will not print the list with XML namespaces.

Use the power of regular expression (``re`` prefix).
Find Python PEPs with four digits in the title (case-insensitive):

.. code-block:: bash

   curl -s https://peps.python.org/peps.rss | \
   xp -e '//item/title[re:match(text(), "pep [0-9]{4}:", "i")]' -q


.. index::
   single: xp script; pretty print

Pretty print element result
---------------------------
.. program:: xp
.. option:: -p, --pretty-element

A result element node can be pretty printed with the ``--pretty-element`` command-line option.

.. warning:: The ``--pretty-element`` option removes all white space text nodes
   *before* applying the XPath expression. Therefore there will be no white space
   text nodes in the results.

Pretty print the latest Python PEP:

.. code-block:: bash

   curl -s https://peps.python.org/peps.rss | xp "//item[1]" -p


.. index::
   single: xp script; file names

Print file names
----------------
.. program:: xp
.. option:: -f, -l, --files-with-hits

The ``--files-with-hits`` command-line option only prints the names
of files with an XPath result that is not false and not NaN (not a number).

Find XML files with HTTP URL's:

.. code-block:: bash

   xp "//mpeg7:MediaUri[starts-with(., 'http://')]" *.xml -f

XML files where all the book prices are below € 25,-.

.. code-block:: bash

   xp -el "math:max(//book/price[@currency='€'])<25" *.xml

.. program:: xp
.. option:: -F, -L, --files-without-hits

The ``--files-without-hits`` command-line option only prints the names
of files without any XPath results, or with a false or NaN result.

XML files without a person with the family name 'Bauwens':

.. code-block:: bash

   xp "//mpeg7:FamilyName[text()='Bauwens']" *.xml -F

xpath method
------------
.. program:: xp
.. option:: -m, --method

``xp`` uses the `lxml.etree.XPath` class by default. You can choose the
`lxml.etree.ElementTree.xpath` method with the ``--method`` command-line option.
The results should be the same but error reporting can be different.


.. rubric:: Footnotes

.. [#] `XML Path Language (XPath) 1.0 <https://www.w3.org/TR/xpath-10/>`_
.. [#] `Namespaces in XML 1.0 <https://www.w3.org/TR/xml-names/>`_
.. [#] `Extensions to XSLT (EXSLT) <https://exslt.github.io/>`_
