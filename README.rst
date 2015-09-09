XML Utilities
=============

Python scripts for XML files.

Pretty print XML files in human readable form,
transform XML files with XSL,
validate XML files with an XSD or DTD
or use XPath expression to select nodes in an XML file.

Scripts
-------
- prettyprint.py_: print XML files in human readable form
- transform.py_: transform XML files with XSL
- validate.py_: validate XML with XSD or DTD
- xpath.py_: use XPath expression to select nodes in XML

W3C
---
- `Extensible Markup Language <http://www.w3.org/TR/xml/>`_
- `XML Schema <http://www.w3.org/standards/xml/schema>`_
- `XSL Transformations <http://www.w3.org/TR/xslt/>`_
- `XML Path Language <http://www.w3.org/TR/xpath/>`_
- `Namespaces in XML 1.0 <http://www.w3.org/TR/xml-names/>`_

Requirements
------------
- `lxml <http://lxml.de/>`_
- `Pygments <http://pygments.org/>`_ (optional)

Installation
------------
**pip**

.. code:: tcsh

        pip install hg+https://bitbucket.org/peteradrichem/xul


.. _prettyprint.py:

Pretty print
------------
.. code:: tcsh

        % prettyprint.py --help

.. code::

        Usage:  prettyprint.py [-n] xml_file_1 ... xml_file_n

        Pretty print XML files.

        Options:
          --version       show program's version number and exit
          -h, --help      show this help message and exit
          -n, --no-color  disable colored output


.. _transform.py:

Transform
---------
.. code:: tcsh

        % transform.py --help

.. code::

        Usage: transform.py -x xslt_file xml_file ...

        Transform XML file(s) with an XSL file.

        Options:
          --version             show program's version number and exit
          -h, --help            show this help message and exit
          -x XSL_FILE, --xsl=XSL_FILE
                                XSL file to transform XML file(s)


.. _validate.py:

Validate
--------
.. code:: tcsh

        % validate.py --help

.. code::

        Usage:  validate.py -x xsd_file xml_file_1 ... xml_file_n
                validate.py -d dtd_file xml_file_1 ... xml_file_n

        Validate XML file(s) with an XSD or DTD file.

        Options:
          --version             show program's version number and exit
          -h, --help            show this help message and exit
          -x XSD_FILE, --xsd=XSD_FILE
                                XSD file to validate XML file(s)
          -d DTD_FILE, --dtd=DTD_FILE
                                DTD file to validate XML file(s)


.. _xpath.py:

XPath
-----
.. code:: tcsh

        % xpath.py --help

.. code::

        Usage: xpath.py [options] -x xpath xml_file_1 ... xml_file_n

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
