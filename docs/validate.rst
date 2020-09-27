.. index::
   single: validate script
   single: scripts; validate
   single: XSD
   single: XML Schema Definition

validate -- Validate an XML source
==================================

Use ``validate`` to validate an :ref:`xml_source`.

XSD
---
Validate an XML source with an XSD [#]_ file:

.. code-block:: bash

   validate -x schema.xsd source.xml

.. index::
   single: DTD
   single: Document Type Definition

DTD
---
Validate an XML source with a DTD [#]_ file:

.. code-block:: bash

   validate -d doctype.dtd source.xml

RELAX NG
--------
Validate an XML source with a RELAX NG [#]_ file:

.. code-block:: bash

   validate -r relaxng.rng source.xml

Options
-------
``validate`` can be used with the following command-line options:

.. code-block:: console

   $ validate --help

   usage: validate [-h] [-V] (-x XSD_SOURCE | -d DTD_SOURCE | -r RELAXNG_SOURCE)
                  [xml_source [xml_source ...]]

   Validate XML source with XSD, DTD or RELAX NG.

   positional arguments:
   xml_source            XML source (file, <stdin>, http://...)

   optional arguments:
   -h, --help            show this help message and exit
   -V, --version         show program's version number and exit
   -x XSD_SOURCE, --xsd XSD_SOURCE
                         XML Schema Definition (XSD) source
   -d DTD_SOURCE, --dtd DTD_SOURCE
                         Document Type Definition (DTD) source
   -r RELAXNG_SOURCE, --relaxng RELAXNG_SOURCE
                         RELAX NG source

Examples
--------

--------------
XML Validation
--------------

Validate XHTML with the
:download:`XHTML 1.0 strict DTD <../examples/dtd/xhtml1-strict.dtd>`:

.. code-block:: bash

   curl -s https://www.webstandards.org/learn/reference/templates/xhtml10s/ | validate -d examples/dtd/xhtml1-strict.dtd

Validate XHTML with the
:download:`XHTML 1.0 strict XSD <../examples/xsd/xhtml1-strict.xsd>`:

.. code-block:: bash

   curl -s https://www.webstandards.org/learn/reference/templates/xhtml10s/ | validate -x examples/xsd/xhtml1-strict.xsd

--------------
XSD Validation
--------------

Validate an XSD file with the
:download:`XML Schema schema document <../examples/xsd/XMLSchema.xsd>`:

.. code-block:: bash

   validate -x examples/xsd/XMLSchema.xsd schema_file.xsd

Validate the XML Schema 1.1 XSD with the (identical) XML Schema schema document:

.. code-block:: bash

   validate -x examples/xsd/XMLSchema.xsd http://www.w3.org/2009/XMLSchema/XMLSchema.xsd

And vice versa:

.. code-block:: bash

   validate -x http://www.w3.org/2009/XMLSchema/XMLSchema.xsd examples/xsd/XMLSchema.xsd

Validate the XML Schema XSD with the
:download:`DTD for XML Schema <../examples/dtd/XMLSchema.dtd>`:

.. code-block:: bash

   validate -d examples/dtd/XMLSchema.dtd examples/xsd/XMLSchema.xsd


.. rubric:: Footnotes

.. [#] `XML Schema 1.0 and 1.1 <https://www.w3.org/XML/Schema>`_
.. [#] `XML Document Type Definition <https://www.w3.org/TR/xml/#dtd>`_
.. [#] `RELAX NG Specification <https://www.oasis-open.org/committees/relax-ng/spec.html>`_
