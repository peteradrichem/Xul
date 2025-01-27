.. index::
   single: transform script
   single: scripts; transform
   single: XSLT
   single: Extensible Stylesheet Language Transformations

==========================
transform -- Transform XML
==========================
``transform`` is a simple command-line script to apply XSLT [#]_ stylesheets to
an :ref:`xml_source`.
If you need a command-line XSLT processor with more options have a look at
`xsltproc <https://gnome.pages.gitlab.gnome.org/libxslt/xsltproc.html>`_


Examples
========
Output a transformed XML file with syntax highlighting like :doc:`ppx <ppx>`:

.. code-block:: bash

   transform stylesheet.xsl file.xml

Transform an URL:

.. code-block:: bash

   curl -s https://example.com/path/file.xml | transform stylesheet.xsl

Save transformed XML to a file:

.. code-block:: bash

   transform stylesheet.xsl source.xml --file new.xml

Options
=======
``transform`` can be used with the following command-line options:

.. code-block:: console

   $ transform --help

   usage: transform [-h] [-V] [-f FILE | -s] [-o] xslt_source [xml_source]

   Transform an XML source with XSLT.

   positional arguments:
     xslt_source           XSLT source (file, http://...)
     xml_source            XML source (file, <stdin>, http://...)

   options:
     -h, --help            show this help message and exit
     -V, --version         show program's version number and exit
     -f FILE, --file FILE  save result to file

   terminal output options:
     -n, --no-syntax       no syntax highlighting
     -o, --omit-declaration
                           omit the XML declaration


Save result to file
===================
.. program:: transform
.. option:: -f FILE, --file FILE

Example stylesheet that converts an XML document to UTF-16 encoding:

.. code-block:: xml

   <?xml version="1.0" encoding="UTF-8"?>
   <xsl:stylesheet
     version="1.0" id="utf16"
     xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

     <xsl:output method="xml" version="1.0" encoding="UTF-16" indent="yes" />

     <xsl:template match="/">
      <xsl:copy-of select="." />
     </xsl:template>

   </xsl:stylesheet>

Save the transformation result to a little-endian UTF-16 XML file.

.. code-block:: bash

   transform to_utf16.xsl utf8.xml --file utf16.xml

Save to file will honor the ``xsl:output`` element [#]_.


Output options
==============
``transform`` options for terminal output.


.. index::
   single: transform script; syntax highlighting
   single: syntax highlighting; transform

Syntax highlighting
-------------------
``transform`` will syntax highlight the XML result if you have Pygments_ installed.

.. program:: transform
.. option:: -n, --no-syntax

Output the transformed XML *without* syntax highlighting:

.. code-block:: bash

   transform --no-syntax stylesheet.xsl file.xml


.. index::
   single: transform script; XML declaration
   single: XML declaration; transform

XML declaration
---------------
XML documents should begin with an XML declaration which specifies the version of XML being used [#]_.

.. program:: transform
.. option:: -o, --omit-declaration

You can omit the XML declaration with the ``--omit-declaration`` option.

.. code-block:: bash

   transform --omit-declaration stylesheet.xsl file.xml


.. _Pygments: https://pygments.org/


.. rubric:: Footnotes

.. [#] `XSL Transformations (XSLT) 1.0 <https://www.w3.org/TR/xslt-10/>`_
.. [#] `XSL Transformations: 16 Output <https://www.w3.org/TR/xslt-10/#output>`_
.. [#] Extensible Markup Language §2.8
   `Prolog and Document Type Declaration <https://www.w3.org/TR/xml/#sec-prolog-dtd>`_
