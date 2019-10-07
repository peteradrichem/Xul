Xul documentation
=================

XML [#]_ utilities written in Python.

Current version: |release|


.. index::
   single: scripts

Xul scripts
-----------
.. toctree::
   :maxdepth: 2

   ppx
   xp
   validate
   transform

XML
---
.. toctree::
   :maxdepth: 2

   xml_source


Installing
----------
The Xul command line scripts can be installed with pip:

.. code:: bash

   pip install Xul

Install Pygments_ for XML syntax highlighting (optional).

.. code:: bash

   pip install Pygments

Dependencies
------------
Xul uses the excellent lxml_ XML toolkit, a Pythonic binding for the C libraries
libxml2_ and libxslt_.

Source
------
The Xul source can be found on Bitbucket_.


Indices and search
------------------
* :ref:`genindex`
* :ref:`search`


.. _lxml: http://lxml.de/
.. _libxml2: http://www.xmlsoft.org/
.. _libxslt: http://xmlsoft.org/libxslt/
.. _Pygments: http://pygments.org/
.. _Bitbucket: https://bitbucket.org/peteradrichem/xul


.. rubric:: Footnotes

.. [#] `Extensible Markup Language (XML) 1.0 <http://www.w3.org/TR/xml/>`_
