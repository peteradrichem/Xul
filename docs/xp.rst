.. index::
   single: xp script
   single: scripts; xp
   single: XPath
   single: XPath expression

=============================
xp -- Select nodes with XPath
=============================
``xp`` is a tool to fine-tune your XPath [#]_ expressions. You can also use ``xp`` to search for
XML files matching an XPath expression.


Examples
========
Select nodes in an :ref:`xml_source` with an XPath expression.

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
=======
``xp`` can be used with the following command-line options:

.. code-block:: console

   $ xp --help

   usage: xp [-h] [-V] [-l | -L] [-d DEFAULT_NS_PREFIX] [-e] [-q] [-c | -p] [-r] [-m] xpath_expr [xml_source ...]

   Select nodes in an XML source with an XPath expression.

   positional arguments:
     xpath_expr            XPath expression
     xml_source            XML source (file, <stdin>, http://...)

   options:
     -h, --help            show this help message and exit
     -V, --version         show program's version number and exit
     -m, --method          use ElementTree.xpath method instead of XPath class

   file hit options:
     output filenames to standard output

     -l, -f, --files-with-hits
                           only names of files with a result that is not false and
                           not NaN are written to standard output
     -L, -F, --files-without-hits
                           only names of files with a false or NaN result, or without a result,
                           are written to standard output

   namespace options:
     -d DEFAULT_NS_PREFIX, --default-prefix DEFAULT_NS_PREFIX
                           set the prefix for the default namespace in XPath [default: 'd']
     -e, --exslt           add EXSLT XML namespaces
     -q, --quiet           don't print XML source namespaces

   element output options:
     -c, --count           only print the number of selected nodes
     -p, --pretty-element  pretty print the result element
     -r, --result-xpath    print the XPath expression of the result element (or its parent)


.. index::
   single: xp script; file names

Searching XML files
===================
``xp`` can print file names matching an XPath expression. A matching result (hit) is *not* false or NaN (not a number).
``xp`` can also print file names not matching an XPath expression.
False and NaN are non-matching results.

Matching XML files
------------------
.. program:: xp
.. option:: -l, -f, --files-with-hits

The ``--files-with-hits`` command-line option only prints the names
of files *with* an XPath result that is *not* false and *not* NaN (not a number).
This is similar to ``grep --files-with-matches`` using XPath instead of regular expressions.

Find XML files with HTTP URL's:

.. code-block:: bash

   xp -l "//mpeg7:MediaUri[starts-with(., 'http://')]" *.xml

XML files where all the book prices are below € 25,-.

.. code-block:: bash

   xp -el "math:max(//book/price[@currency='€'])<25" *.xml

Non-matching XML files
----------------------
.. program:: xp
.. option:: -L, -F, --files-without-hits

The ``--files-without-hits`` command-line option only prints the names
of files *without* any XPath results, or with a false or NaN result.
This is similar to ``grep --files-without-match`` using XPath instead of regular expressions.

XML files without a person with the family name 'Bauwens':

.. code-block:: bash

   xp -L "//mpeg7:FamilyName[text()='Bauwens']" *.xml


.. index::
   single: xp script; namespaces
   single: XML namespaces
   single: namespaces

Namespaces in XML
=================
List all the XML namespaces [#]_ (prefix, URI) of the document element:

.. code-block:: bash

   xp 'namespace::*' file.xml

Print the default namespace of the document element, if it has one:

.. code-block:: bash

   xp 'namespace::*[name()=""]' file.xml


.. index::
   single: xp script; default namespace prefix
   single: namespace prefix

Default prefix
--------------
.. program:: xp
.. option:: -d <prefix>, --default-prefix <prefix>

The default XML namespace in an XML document has no prefix (*None*).
To select nodes in an XML namespace XPath needs prefixed names (qualified names).
Therefore ``xp`` uses ``d`` as the prefix for the default XML namespace.

List the five most recent Python Insider posts:

.. code-block:: bash

   curl -s https://feeds.feedburner.com/PythonInsider | \
      xp "descendant::d:entry[position()<=5]/d:title/text()"

You can change the prefix for the default namespace with the ``--default-prefix`` option:

.. code-block:: bash

   curl -s https://feeds.feedburner.com/PythonInsider | \
      xp -d p "descendant::p:entry[position()<=5]/p:title/text()" \


.. index::
   single: xp script; EXSLT
   single: EXSLT
   single: Extensions to XSLT

Extensions to XSLT
------------------
.. program:: xp
.. option:: -e, --exslt

lxml supports the EXSLT [#]_ extensions through libxslt (requires libxslt 1.1.25 or higher).
Add EXSLT namespaces with the ``--exslt`` command-line option.

Find Python Insider posts published in or after 2015 with EXSLT (``date`` prefix):

.. code-block:: bash

   curl -s https://feeds.feedburner.com/PythonInsider | \
      xp -e "//d:entry[date:year(d:published) >= '2015']/d:title/text()"

Python Insider posts updated in December:

.. code-block:: bash

   curl -s https://feeds.feedburner.com/PythonInsider | \
      xp -e "//d:entry[date:month-name(d:updated) = 'December']/d:title/text()"


.. index::
   single: xp script; quiet

Do not list namespaces
----------------------
.. program:: xp
.. option:: -q, --quiet

With the ``--quiet`` command-line option ``xp`` will not print the list with XML namespaces.

Find Python PEPs with four digits in the title (case-insensitive) using the power of
regular expression (EXSLT ``re`` prefix):

.. code-block:: bash

   curl -s https://peps.python.org/peps.rss | \
      xp -eq '//item/title[re:match(text(), "pep [0-9]{4}:", "i")]'


Result element output
=====================

.. index::
   single: xp script; result XPath

Print result's XPath
--------------------
.. program:: xp
.. option:: -r, --result-xpath

Print the XPath expression of each result element with the ``--result-xpath`` option.
Result XPath expressions will have an absolute location path.

.. code-block:: bash

   xp --result-xpath "//title" file.xml

If an XPath result is a text or attribute node ``xp`` will print the parent element's
XPath expression.

List the XPath expressions of all elements with attributes:

.. code-block:: bash

   xp -r "//@*" file.xml


.. index::
   single: xp script; pretty print

Pretty print result element
---------------------------
.. program:: xp
.. option:: -p, --pretty-element

A result element node can be pretty printed with the ``--pretty-element`` command-line option.

.. note:: The ``--pretty-element`` option removes all white space text nodes
   *before* applying the XPath expression. Therefore there will be no white space
   text nodes in the results.

Pretty print the latest Python PEP:

.. code-block:: bash

   curl -s https://peps.python.org/peps.rss | xp -p "//item[1]"


Other options
=============

.. index::
   single: xp script; node count

Node count
----------
.. program:: xp
.. option:: -c, --count

Only count the number of selected nodes with the ``--count`` command-line option.
This is similar to ``grep --count`` using XPath instead of regular expressions.

Count the number of series titles:

.. code-block:: bash

   xp --count "//d:Title[@type='parentSeriesTitle']" file1.xml file2.xml⋅file3.xml



.. index::
   single: xp script; xpath method

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
