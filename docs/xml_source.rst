.. index::
   single: XML source

.. _xml_source:

==========
XML source
==========

The Xul scripts require an XML source to operate on.
An XML source can be a local file, an URL or a pipe.


.. index::
   single: XML file

File
----
With ``xp`` you can select nodes in a local XML file with an XPath expression:

.. code-block:: bash

   xp 'node()' entity.xml


.. index::
   single: redirected output
   single: pipe

Pipe
----
Redirect output (pipe) to a Xul script:

.. code-block:: bash

   curl -s https://developer.apple.com/news/rss/news.rss | ppx


.. index::
   single: URL

URL
---
libxml2_ also supports loading XML through HTTP (and FTP).
For example, to pretty print an RSS feed:

.. code-block:: bash

   ppx http://feeds.launchpad.net/pytz/announcements.atom

Loading XML through HTTPS is not supported and will result in an
*failed to load external entity* error.


.. index::
   single: XHTML

XHTML
=====

XHTML [#]_ is part of the family of XML markup languages. It's obsolete.

Examples
--------
Pretty print an XHTML document:

.. code-block:: bash

   curl -s https://www.webstandards.org/learn/reference/templates/xhtml11/ | ppx

Validate an XHTML document with the
:download:`XHTML 1.0 strict DTD <../examples/dtd/xhtml1-strict.dtd>`:

.. code-block:: bash

   curl -s https://www.webstandards.org/learn/reference/templates/xhtml10t/ | validate -d examples/dtd/xhtml1-transitional.dtd

Print the link destinations in an XHTML document:

.. code-block:: bash

   xp -d html "//html:link/@href" http://www.w3.org/1999/xhtml/

More XSDs and DTDs examples_ can be found in the Xul Bitbucket repository.

.. seealso:: Xul scripts: :doc:`ppx <ppx>`, :doc:`xp <xp>`,
   :doc:`validate <validate>`, :doc:`transform <transform>`


.. rubric:: Footnotes

.. [#] `XHTML™ 1.0 The Extensible HyperText Markup Language
   <https://www.w3.org/TR/xhtml1>`_


.. _examples: https://bitbucket.org/peteradrichem/xul/src/master/examples/
.. _libxml2: http://www.xmlsoft.org/
