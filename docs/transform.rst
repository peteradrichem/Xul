.. index::
   single: transform script
   single: scripts; transform
   single: XSLT
   single: Extensible Stylesheet Language Transformations

transform -- Transform XML
==========================
``transform`` is a simple command-line script to apply XSLT [#]_ stylesheets to
an :ref:`xml_source`.
If you need a command-line XSLT processor with more options have a look at
`xsltproc <https://gnome.pages.gitlab.gnome.org/libxslt/xsltproc.html>`_

Transform an XML file:

.. code-block:: bash

   transform stylesheet.xsl file.xml

Transform an XML file and :doc:`pretty print <ppx>` the result:

.. code-block:: bash

   transform --xsl-output stylesheet.xsl file.xml | ppx

Options
-------
``transform`` can be used with the following command-line options:

.. code-block:: console

   $ transform --help

   usage: transform [-h] [-V] [-x | -o] [-f FILE] xslt_source xml_source

   Transform XML source with XSLT.

   positional arguments:
     xslt_source           XSLT source (file, http://...)
     xml_source            XML source (file, <stdin>, http://...)

   optional arguments:
     -h, --help            show this help message and exit
     -V, --version         show program's version number and exit
     -x, --xsl-output      honor xsl:output
     -o, --omit-declaration
                           omit the XML declaration
     -f FILE, --file FILE  save result to file

.. index::
   single: transform script; XML declaration
   single: XML declaration; transform

XSL output
----------

.. program:: transform
.. option:: -x, --xsl-output

You can honor the ``xsl:output`` element [#]_ with the ``--xsl-output`` option.

.. code-block:: bash

   transform --xsl-output stylesheet.xsl file.xml

Save transformation result to file
----------------------------------

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

Save the transformation result to a little-endian UTF-16 Unicode text file.

.. code-block:: bash

   transform --xsl-output to_utf16.xsl utf8.xml --file utf16.xml

When saving to file use the ``--xsl-output`` option to preserve the character encoding of the transformation.

XML declaration
---------------
XML documents should begin with an XML declaration which specifies the version of XML being used [#]_.

.. program:: transform
.. option:: -o, --omit-declaration

You can omit the XML declaration with the ``--omit-declaration`` option.

.. code-block:: bash

   transform --omit-declaration stylesheet.xsl file.xml


.. rubric:: Footnotes

.. [#] `XSL Transformations (XSLT) 1.0 <https://www.w3.org/TR/xslt-10/>`_
.. [#] `XSL Transformations: 16 Output <https://www.w3.org/TR/xslt-10/#output>`_
.. [#] Extensible Markup Language §2.8
   `Prolog and Document Type Declaration <https://www.w3.org/TR/xml/#sec-prolog-dtd>`_
