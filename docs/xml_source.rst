.. _xml_source:

.. index::
   single: XML source

==========
XML source
==========
Xul scripts require an XML source to operate on.
An XML source can be a local file, an URL (HTTP or FTP) or a pipe.


.. index::
   single: XHTML

Examples
========
Pretty print an XHTML [#]_ document:

.. code-block:: bash

   curl -s https://www.webstandards.org/learn/reference/templates/xhtml11/ | ppx

Validate an XHTML document with the
:download:`XHTML 1.0 strict DTD <../examples/dtd/xhtml1-strict.dtd>`:

.. code-block:: bash

   curl -s https://www.webstandards.org/learn/reference/templates/xhtml10t/ | \
      validate -d examples/dtd/xhtml1-transitional.dtd

Print the link destinations in an XHTML document:

.. code-block:: bash

   curl -s https://www.w3.org/1999/xhtml/ | xp -d html "//html:link/@href"

More XSDs and DTDs examples_ can be found in the Xul GitHub repository.

.. seealso:: Xul scripts: :doc:`ppx <ppx>`, :doc:`xp <xp>`,
   :doc:`validate <validate>`, :doc:`transform <transform>`


.. index::
   single: XML file

File
====
With ``xp`` you can select nodes in a local XML file with an XPath expression:

.. code-block:: bash

   xp 'node()' entity.xml


.. index::
   single: redirected output
   single: pipe
   single: curl

Pipe
====
Redirect output (pipe) of an XML source to a Xul script:

.. code-block:: bash

   curl -s https://developer.apple.com/news/rss/news.rss | ppx


.. index::
   single: URL
   single: HTTP
   single: FTP

URL
===
libxml2_ also supports loading XML through HTTP (and FTP).
For example, to pretty print an RSS feed:

.. code-block:: bash

   ppx http://feeds.launchpad.net/pytz/announcements.atom

.. index::
   single: HTTPS

Loading XML through HTTPS is not supported and will result in an
*failed to load external entity* error.
Try redirecting the HTTPS URL output to a Xul script. See the ``curl`` example above.


.. rubric:: Footnotes

.. [#] `XHTML™ <https://www.w3.org/TR/xhtml1>`_ is part of the family of XML markup languages. It's obsolete.


.. _examples: https://github.com/peteradrichem/Xul/tree/main/examples
.. _libxml2: https://gitlab.gnome.org/GNOME/libxml2/-/wikis/
