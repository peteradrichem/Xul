.. index::
   single: XML source

.. _xml_source:

XML source
==========

The Xul scripts require an XML source to operate on.
An XML source can be a local file, an URL or a pipe.

File
----
With ``xp`` you can select nodes in a local XML file with an XPath expression:

.. code::

   xp -x 'node()' entity.xml

URL
---
libxml2_ also supports loading XML through HTTP (and FTP).
For example, to pretty print an RSS feed:

.. code::

   ppx http://feeds.feedburner.com/PythonInsider

Loading XML through HTTPS is not supported and will result in an
*failed to load external entity* error.


Pipe
----
Redirect output (pipe) to a Xul script:

.. code::

   curl -s https://developer.apple.com/news/rss/news.rss | ppx


.. index::
   single: XHTML

XHTML
=====

XHTML [#]_ is part of the family of XML markup languages.

Examples
--------
Pretty print an XHTML document:

.. code::

   ppx http://www.w3.org/TR/xhtml1

Validate an XHTML document with the
:download:`XHTML 1.0 strict DTD <../examples/dtd/xhtml1-strict.dtd>`:

.. code::

   validate -d examples/dtd/xhtml1-strict.dtd http://www.w3.org/TR/xhtml1

Print the link destinations in an XHTML document:

.. code::

   xp -d html -x "//html:link/@href" http://www.w3.org/1999/xhtml

More XSDs and DTDs examples_ can be found in the Xul Bitbucket repository.

.. seealso:: Xul scripts: :doc:`ppx <ppx>`, :doc:`xp <xp>`,
   :doc:`validate <validate>`, :doc:`transform <transform>`


.. rubric:: Footnotes

.. [#] `XHTML™ 1.0 The Extensible HyperText Markup Language
   <http://www.w3.org/TR/xhtml1>`_


.. _examples: https://bitbucket.org/peteradrichem/xul/src/tip/examples/
.. _libxml2: http://www.xmlsoft.org/
