Xul documentation
=================

XML [#]_ utilities written in Python.

Current version: |release|

.. image:: https://img.shields.io/pypi/pyversions/xul.svg
   :target: https://pypi.org/project/Xul/
   :alt: Python versions

.. image:: https://img.shields.io/pypi/wheel/xul.svg
   :target: https://pypi.org/project/Xul/
   :alt: Wheel

.. image:: https://img.shields.io/pypi/l/xul.svg
   :target: https://pypi.org/project/Xul/
   :alt: License

.. image:: https://img.shields.io/pypi/v/xul
   :target: https://pypi.org/project/Xul/
   :alt: PyPI version

.. index::
   single: scripts

Xul scripts
-----------
The supported XML sources are documented in  :ref:`xml_source`.

.. toctree::
   :maxdepth: 2

   ppx
   xp
   validate
   transform

Other
-----
.. toctree::
   :maxdepth: 2

   xml_source
   changelog


Installing
----------
The Xul command-line scripts can be installed with pip:

.. code-block:: bash

   pip install Xul

Install Xul with Pygments_ for XML syntax highlighting.

.. code-block:: bash

   pip install Xul[syntax]

Dependencies
------------
Xul uses the excellent lxml_ XML toolkit, a Pythonic binding for the C libraries
libxml2_ and libxslt_.

Changelog
---------
Xul :doc:`Changelog <changelog>`.

Source
------
The source can be found on GitHub_.


Indices and search
------------------
* :ref:`genindex`
* :ref:`search`


.. _lxml: https://lxml.de/
.. _libxml2: https://gitlab.gnome.org/GNOME/libxml2/-/wikis/
.. _libxslt: https://gitlab.gnome.org/GNOME/libxslt/-/wikis/
.. _Pygments: https://pygments.org/
.. _GitHub: https://github.com/peteradrichem/Xul


.. rubric:: Footnotes

.. [#] `Extensible Markup Language (XML) 1.0 <https://www.w3.org/TR/xml/>`_
