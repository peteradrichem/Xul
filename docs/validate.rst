.. index::
   single: validate script
   single: scripts; validate

========================
validate -- Validate XML
========================
The ``validate`` script can check if an :ref:`xml_source` conforms to an XML schema language.
You can also use ``validate`` to search for XML files that validate against an XML schema language.


Examples
========
Validate XHTML with the
:download:`XHTML 1.0 strict XSD <../examples/xsd/xhtml1-strict.xsd>`:

.. code-block:: bash

   curl -s https://www.webstandards.org/learn/reference/templates/xhtml10s/ | \
      validate -x examples/xsd/xhtml1-strict.xsd

Validate XHTML with the
:download:`XHTML 1.0 strict DTD <../examples/dtd/xhtml1-strict.dtd>`:

.. code-block:: bash

   curl -s https://www.webstandards.org/learn/reference/templates/xhtml10s/ | \
      validate -d examples/dtd/xhtml1-strict.dtd

Options
=======
``validate`` can be used with the following command-line options:

.. code-block:: console

   $ validate --help

   usage: validate [-h] [-V] (-x XSD_SOURCE | -d DTD_SOURCE | -r RELAXNG_SOURCE) [-l | -L] [xml_source ...]

   Validate an XML source with XSD, DTD or RELAX NG.

   positional arguments:
     xml_source            XML source (file, <stdin>, http://...)

   options:
     -h, --help            show this help message and exit
     -V, --version         show program's version number and exit

   XML validator:
     choose an XML validator: XSD, DTD or RELAX NG

     -x XSD_SOURCE, --xsd XSD_SOURCE
                           XML Schema Definition (XSD) source
     -d DTD_SOURCE, --dtd DTD_SOURCE
                           Document Type Definition (DTD) source
     -r RELAXNG_SOURCE, --relaxng RELAXNG_SOURCE
                           RELAX NG source

   file hit options:
     output filenames to standard output

     -l, -f, --validated-files
                           only the names of validated XML files are written to standard output
     -L, -F, --invalidated-files
                           only the names of invalidated XML files are written to standard output


.. index::
   single: XML schema languages

XML schema languages
====================
``validate`` supports the following XML schema languages.


.. index::
   single: validate script; XSD
   single: XSD
   single: XML Schema Definition
   single: XML Schema

XML Schema Definition (XSD)
---------------------------
.. program:: validate
.. option:: -x <xml_schema>, --xsd <xml_schema>

Use the ``--xsd`` option to validate an XML source with an XSD [#]_ file:

.. code-block:: bash

   validate -x schema.xsd source.xml

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


.. index::
   single: validate script; DTD
   single: DTD
   single: Document Type Definition

Document Type Definition (DTD)
------------------------------
.. program:: validate
.. option:: -d <dtd_schema>, --dtd <dtd_schema>

Validate an XML source with a DTD [#]_ file with the ``--dtd`` option:

.. code-block:: bash

   validate -d doctype.dtd source.xml

Validate the XML Schema XSD with the
:download:`DTD for XML Schema <../examples/dtd/XMLSchema.dtd>`:

.. code-block:: bash

   validate -d examples/dtd/XMLSchema.dtd examples/xsd/XMLSchema.xsd


.. index::
   single: validate script; RELAX NG
   single: RELAX NG
   single: RNG

RELAX NG
--------
.. program:: validate
.. option:: -r <relax_ng_schema>, --relaxng <relax_ng_schema>

The ``--relaxng`` option validates an XML source with a RELAX NG [#]_ file:

.. code-block:: bash

   validate -r relaxng.rng source.xml

Validation Errors
=================
If an :ref:`xml_source` doesn't validate the ``validate`` script will show the
reason with some additional information:

.. code-block:: bash

   validate -x TV-Anytime.xsd NED120200816E.xml

   XML source 'NED120200816E.xml' does not validate
   line 92, column 0: Element '{urn:tva:metadata:2019}Broadcaster': This element is not expected.
   Expected is one of ( {urn:tva:metadata:2019}FirstShowing, {urn:tva:metadata:2019}LastShowing, {urn:tva:metadata:2019}Free ).


.. index::
   single: validate script; file names

Searching XML files
===================
``validate`` can print the names of validated or invalidated XML files to standard output.

Validated XML files
-------------------
.. program:: validate
.. option:: -l, -f, --validated-files

The ``--validated-files`` command-line option only prints the names of validated XML files
(similar to ``grep --files-with-matches``).

Find XML files that validate:

.. code-block:: bash

   validate -lx schema.xsd *.xml

Invalidated XML files
---------------------
.. program:: validate
.. option:: -L, -F, --invalidated-files

The ``--invalidated-files`` command-line option only prints the names of invalidated XML files
(similar to ``grep --files-without-match``).

Remove XML files that fail to validate:

.. code-block:: bash

   validate -Lx schema.xsd *.xml | xargs rm


.. rubric:: Footnotes

.. [#] `XML Schema 1.1 <https://www.w3.org/XML/Schema>`_
.. [#] `XML Document Type Definition <https://www.w3.org/TR/xml/#dtd>`_
.. [#] `RELAX NG Specification <https://www.oasis-open.org/committees/relax-ng/spec.html>`_
