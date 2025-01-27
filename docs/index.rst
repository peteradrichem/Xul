=================
Xul documentation
=================
Xul: XML [#]_ utilities written in Python.
Current release: |release|

.. image:: https://img.shields.io/pypi/v/xul
   :target: https://pypi.org/project/Xul/
   :alt: PyPI version

.. image:: https://img.shields.io/pypi/wheel/xul.svg
   :target: https://pypi.org/project/Xul/
   :alt: Wheel

.. image:: https://img.shields.io/pypi/pyversions/xul.svg
   :target: https://pypi.org/project/Xul/
   :alt: Python versions

.. image:: https://img.shields.io/pypi/l/xul.svg
   :target: https://pypi.org/project/Xul/
   :alt: License

.. image:: https://readthedocs.org/projects/xul/badge/
   :target: https://xul.readthedocs.io/en/stable/
   :alt: Documentation

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
   :alt: Black code style

.. image:: https://img.shields.io/badge/type%20checked-mypy-039dfc
   :target: https://mypy-lang.org
   :alt: Typing checked by mypy

.. image:: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json
   :target: https://astral.sh/ruff
   :alt: Ruff linting

.. image:: https://img.shields.io/badge/imports-isort-1674b1
   :target: https://pycqa.github.io/isort/
   :alt: Imports sorted by isort

.. image:: https://github.com/peteradrichem/Xul/actions/workflows/code-checks.yml/badge.svg
   :target: https://github.com/peteradrichem/Xul/actions/workflows/code-checks.yml
   :alt: Code checks


.. index::
   single: scripts

Xul scripts
===========
Xul is a set of XML scripts written in Python.
The supported XML sources are documented in  :ref:`xml_source`.

.. toctree::
   :caption: Scripts
   :maxdepth: 2

   ppx
   xp
   validate
   transform


.. index::
   single: install
   single: install; syntax highlighting
   single: syntax highlighting; install

Installing
==========
Xul command-line scripts can be installed with pip:

.. code-block:: bash

   pip install Xul

Install Xul with Pygments_ for XML syntax highlighting.

.. code-block:: bash

   pip install Xul[syntax]


.. index::
   single: install; dependencies
   single: dependencies

Dependencies
------------
Xul uses the excellent lxml_ XML toolkit, a Pythonic binding for the C libraries
libxml2_ and libxslt_.


.. index::
   single: source

Source
------
The source can be found on GitHub_.

Other
=====
* :ref:`xml_source`
* :ref:`changelog`
* :ref:`Xul index <genindex>`

.. toctree::
   :caption: Other
   :hidden:

   xml_source
   changelog
   genindex


.. _lxml: https://lxml.de/
.. _libxml2: https://gitlab.gnome.org/GNOME/libxml2/-/wikis/
.. _libxslt: https://gitlab.gnome.org/GNOME/libxslt/-/wikis/
.. _Pygments: https://pygments.org/
.. _GitHub: https://github.com/peteradrichem/Xul


.. rubric:: Footnotes

.. [#] `Extensible Markup Language (XML) 1.0 <https://www.w3.org/TR/xml/>`_
