XML scripts
===========

Version 2.0.0

Python scripts for XML files.
Transform with XSL, validate with XSD (or DTD), use XPath and pretty print your XML files.

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

Requirements
------------
- `lxml <http://lxml.de/>`_
- `TAB <https://bitbucket.org/peteradrichem/tab>`_
- optional `Pygments <http://pygments.org/>`_

Installation
------------
**pip**

.. code:: tcsh

        pip install hg+https://bitbucket.org/peteradrichem/xml-scripts


.. _prettyprint.py:

Pretty print
------------
.. code:: tcsh

        % prettyprint.py --help
        Usage:  prettyprint.py [-n] xml_file_1 ... xml_file_n

        Pretty print XML files

        Options:
          --version       show program's version number and exit
          -h, --help      show this help message and exit
          -n, --no-color  disable colored output


.. _transform.py:

Transform
---------
.. code:: tcsh

        % transform.py --help
        Usage: transform.py -x xslt_file xml_file ...

        Transform XML file(s) with XSLT file

        Options:
          --version             show program's version number and exit
          -h, --help            show this help message and exit
          -x XSLT_FILE, --xslt=XSLT_FILE
                                XSLT file to transform XML file(s)


.. _validate.py:

Validate
--------
.. code:: tcsh

        % validate.py --help
        Usage:  validate.py -x xsd_file xml_file_1 ... xml_file_n
                validate.py -d dtd_file xml_file_1 ... xml_file_n

        Validate XML files with a XSD or DTD file

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
        Usage: xpath.py [options] -x xpath xml_file_1 ... xml_file_n

        Use XPath expression to select nodes in XML file(s).

        Options:
          --version             show program's version number and exit
          -h, --help            show this help message and exit
          -x XPATH_EXP, --xpath=XPATH_EXP
                                XPath expression
          -n, --namespace       enable XML namespace prefixes
          -p, --print-xpath     print the absolute XPath of a result (or parent)
                                element
          -e, --element-tree    print the XML tree of a result element
          -m, --method          use ElementTree.xpath method instead of XPath class
