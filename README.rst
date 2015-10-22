Xul -- XML Utilities
====================

XML scripts in Python.

- ppx_: pretty print XML
- xp_: use XPath on XML
- validate_: validate XML with an XSD or DTD
- transform_: transform XML with XSL

Requirements
------------

Xul uses the excellent `lxml <http://lxml.de/>`_ XML toolkit.
And `Pygments <http://pygments.org/>`_ for XML syntax highlighting (optional).


Installation
------------

Install the Xul scripts with **pip**:

.. code:: tcsh

        pip install hg+https://bitbucket.org/peteradrichem/xul


.. _ppx:

ppx
---

Pretty print XML in human readable form.

.. code:: tcsh

        ppx --help

.. code::

        Usage:  ppx [-n] xml_file_1 ... xml_file_n

        Pretty Print XML.

        Options:
          --version       show program's version number and exit
          -h, --help      show this help message and exit
          -n, --no-color  disable colored output


.. _xp:

xp
--

Use XPath expression to select nodes or node-sets in an XML document.

.. code:: tcsh

        xp --help

.. code::

        Usage: xp [options] -x xpath xml_file_1 ... xml_file_n

        Use XPath expression to select nodes in XML file(s).

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


.. _validate:

validate
--------

Validate XML with an XSD or DTD.

.. code:: tcsh

        validate --help

.. code::

        Usage:  validate -x xsd_file xml_file_1 ... xml_file_n
                validate -d dtd_file xml_file_1 ... xml_file_n

        Validate XML file(s) with an XSD or DTD file.

        Options:
          --version             show program's version number and exit
          -h, --help            show this help message and exit
          -x XSD_FILE, --xsd=XSD_FILE
                                XSD file to validate XML file(s)
          -d DTD_FILE, --dtd=DTD_FILE
                                DTD file to validate XML file(s)


.. _transform:

transform
---------

Transform XML with XSL.

.. code:: tcsh

        transform --help

.. code::

        Usage: transform -x xslt_file xml_file ...

        Transform XML file(s) with an XSL file.

        Options:
          --version             show program's version number and exit
          -h, --help            show this help message and exit
          -x XSL_FILE, --xsl=XSL_FILE
                                XSL file to transform XML file(s)


W3C
---

W3C XML links:

- `Extensible Markup Language <http://www.w3.org/TR/xml/>`_
- `XML Schema <http://www.w3.org/standards/xml/schema>`_
- `XSL Transformations <http://www.w3.org/TR/xslt/>`_
- `XML Path Language <http://www.w3.org/TR/xpath/>`_
- `Namespaces in XML 1.0 <http://www.w3.org/TR/xml-names/>`_
