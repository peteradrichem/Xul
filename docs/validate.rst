.. index::
   single: validate
   single: scripts; validate

validate -- Validate an XML source
==================================

Use ``validate`` to validate an XML source.

With an XSD file:

.. code:: bash

   validate -x xsd.xml file.xml

.. index::
   single: DTD
   single: Document Type Definition

With a DTD file:

.. code:: bash

   validate -d dtd.xml file.xml


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

.. index::
   single: XSD
   single: XML Schema Definition

Validate `XML Schema <http://www.w3.org/XML/Schema>`_ with the XML Schema 1.0 XSD:

.. code:: bash

   validate -x http://www.w3.org/2001/XMLSchema.xsd http://www.w3.org/2001/XMLSchema.xsd
