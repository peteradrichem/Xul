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

.. code:: bash

   validate -x schema.xsd file.xml

.. index::
   single: DTD
   single: Document Type Definition

DTD
---
Validate an XML source with a DTD [#]_ file:

.. code:: bash

   validate -d doctype.dtd file.xml

Options
-------
``validate`` supports the following command-line options:

.. code:: bash

   $ validate --help

   Usage:  validate -x xsd_source xml_source ...
           validate -d dtd_source xml_source ...

   Validate XML source with XSD or DTD.

   Options:
     --version             show program's version number and exit
     -h, --help            show this help message and exit
     -x XSD_SOURCE, --xsd=XSD_SOURCE
                           XML Schema Definition (XSD) source
     -d DTD_SOURCE, --dtd=DTD_SOURCE
                           Document Type Definition (DTD) source

Examples
--------

--------------
XML Validation
--------------

Validate XHTML with the
:download:`XHTML 1.0 strict DTD <../examples/dtd/xhtml1-strict.dtd>`:

.. code:: bash

   validate -d examples/dtd/xhtml1-strict.dtd http://www.w3.org/TR/xhtml1

Validate XHTML with the
:download:`XHTML 1.0 strict XSD <../examples/xsd/xhtml1-strict.xsd>`:

.. code:: bash

   validate -x examples/xsd/xhtml1-strict.xsd  http://www.w3.org/TR/xhtml1

--------------
XSD Validation
--------------

Validate an XSD file with the
:download:`XML Schema schema document <../examples/xsd/XMLSchema.xsd>`:

.. code:: bash

   validate -x examples/xsd/XMLSchema.xsd schema_file.xsd

Validate the XML Schema XSD with the (identical) XML Schema schema document:

.. code:: bash

   validate -x examples/xsd/XMLSchema.xsd http://www.w3.org/2009/XMLSchema/XMLSchema.xsd

And vice versa:

.. code:: bash

   validate -x http://www.w3.org/2009/XMLSchema/XMLSchema.xsd examples/xsd/XMLSchema.xsd

Validate the XML Schema XSD with the
:download:`DTD for XML Schema <../examples/dtd/XMLSchema.dtd>`:

.. code:: bash

   validate -d examples/dtd/XMLSchema.dtd examples/xsd/XMLSchema.xsd


.. rubric:: Footnotes

.. [#] `XML Schema 1.0 and 1.1 <http://www.w3.org/XML/Schema>`_
.. [#] `XML Document Type Definition <http://www.w3.org/TR/xml/#dtd>`_
