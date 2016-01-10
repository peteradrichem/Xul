.. index::
   single: XML source

.. _xml_source:

XML source
==========

The Xul scripts require an XML source to operate on.
An XML source can be a local file, an URL or a pipe.

File
----
With ``xp`` you can use an XPath expression on any local XML file:

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

XHTML
=====

XHTML_ is also part of the family of XML markup languages.

.. code::

   ppx http://www.w3.org/TR/xhtml1

   validate -d examples/dtd/xhtml1-strict.dtd http://www.w3.org/TR/xhtml1

   xp -d html -x "//html:link/@href" http://www.w3.org/1999/xhtml


.. _XHTML: http://www.w3.org/TR/xhtml1
.. _libxml2: http://www.xmlsoft.org/
