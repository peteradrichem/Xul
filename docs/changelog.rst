.. _changelog:

=========
Changelog
=========

This document records all notable changes to `Xul <https://xul.readthedocs.io/>`_.

`3.1.1 <https://github.com/peteradrichem/Xul/compare/3.1.0...3.1.1>`_ (2025-10-20)
==================================================================================
* :doc:`ppx <ppx>`: group output options in help

`3.1.0 <https://github.com/peteradrichem/Xul/compare/3.0.0...3.1.0>`_ (2025-10-12)
==================================================================================
* Added ``--count`` option to :doc:`xp <xp>`: only print the number of selected nodes.
* Last Python 3.9 release.

`3.0.0 <https://github.com/peteradrichem/Xul/compare/2.5.1...3.0.0>`_ (2025-01-27)
==================================================================================
* Drop support for Python < 3.9.
* :doc:`xp <xp>`: fix boolean result (Python >= 3.12).
* :doc:`xp <xp>`: fix string result representation (Python 3).
* :doc:`xp <xp>`: improved printing of namespaces.
* :doc:`transform <transform>`: syntax highlighting for terminal output.
* :doc:`transform <transform>`: added ``--no-syntax`` option for terminal output.
* :doc:`transform <transform>`: removed ``--xsl-output`` option (always for ``--file``).
* Fixed encoding issues.
* Clearer error messages.
* Improved documentation; grouped CLI options.
* Code checks: ruff, black, isort, mypy (GitHub Action).
* Test script for local testing with Docker Compose.
* Removed legacy code.
* Typing.
* Updated Sphinx configuration; Furo theme.
* Output formatting (f-strings).

`2.5.1 <https://github.com/peteradrichem/Xul/compare/2.5.0...2.5.1>`_ (2024-12-26)
==================================================================================
* Catch UnicodeDecodeError (Python 3).

`2.5.0 <https://github.com/peteradrichem/Xul/compare/2.4.2...2.5.0>`_ (2024-12-25)
==================================================================================
* Documentation updates.
* Tested on Python 3.11, 3.12, 3.13.
* :doc:`transform <transform>`: honor ``--file`` with a non-XML result.

`2.4.2 <https://github.com/peteradrichem/Xul/compare/2.4.1...2.4.2>`_ (2024-12-15)
==================================================================================
* Moved to `GitHub <https://github.com/peteradrichem/Xul>`_.
* Read the Docs configuration.
* Migrated to pyproject.toml.

`2.4.1 <https://bitbucket.org/peteradrichem/xul/branches/compare/2.4.1%0D2.4.0>`_ (2022-02-14)
==============================================================================================
* Fixed Changelog URL.

`2.4.0 <https://bitbucket.org/peteradrichem/xul/branches/compare/2.4.0%0D2.3.0>`_ (2022-02-14)
==============================================================================================
* Beter handling of encodings other than UTF-8 (e.g. ISO-8859, UTF-16, UCS-2, UCS-4).
* Added ``--file FILE`` option to :doc:`transform <transform>`: save result to file.
* :doc:`transform <transform>`: now only transforms a single file.
* Added ``--xsl-output`` option to :doc:`transform <transform>`: honor ``xsl:output``.
* Removed xul.dom module (legacy).

`2.3.0 <https://bitbucket.org/peteradrichem/xul/branches/compare/2.3.0%0D2.2.1>`_ (2021-01-28)
==============================================================================================
* Added ``--invalidated-files`` option to :doc:`validate <validate>`: only print names of invalidated files.
* Added ``--validated-files`` option to :doc:`validate <validate>`: only print names of validated XML files.
* :doc:`xp <xp>`: ``--files-with-hits`` and ``--files-without-hits`` options are mutually exclusive.
* Consistent broken pipes ``errno.EPIPE`` exit status (Python 2).

`2.2.1 <https://bitbucket.org/peteradrichem/xul/branches/compare/2.2.1%0D2.2.0>`_ (2021-01-14)
==============================================================================================
* :doc:`xp <xp>` ``--pretty-element`` fix: output multiple results to a pipe (Python 2).

`2.2.0 <https://bitbucket.org/peteradrichem/xul/branches/compare/2.2.0%0D2.1.0>`_ (2020-10-07)
==============================================================================================
* :doc:`xp <xp>`: handle `NaN` [#NaN]_ result as a false result (``--files-with|without-hits``).
* Renamed :doc:`xp <xp>` ``--files-without-results`` option to ``--files-without-hits``: only print names of files with a false or `NaN` [#NaN]_ result, or without any results.
* Renamed :doc:`xp <xp>` ``--files-with-results`` option to ``--files-with-hits``: only print names of files with a non-false and non-`NaN` [#NaN]_ result.
* Added ``--relaxng`` option to :doc:`validate <validate>`: validate an XML source with RELAX NG.
* Refactored :doc:`validate <validate>` script.
* README: documentation is on `Read The Docs <https://xul.readthedocs.io/>`_.

`2.1.0 <https://bitbucket.org/peteradrichem/xul/branches/compare/2.1.0%0D2.0.3>`_ (2020-09-09)
==============================================================================================
* Added ``--quiet`` option to :doc:`xp <xp>`: don't print the XML namespace list.
* Added ``--files-without-results`` option to :doc:`xp <xp>`: only print names of files with a false result or without any results.
* Added ``--files-with-results`` option to :doc:`xp <xp>`: only print names of files with XPath matches.

`2.0.3 <https://bitbucket.org/peteradrichem/xul/branches/compare/2.0.3%0D2.0.2>`_ (2020-06-10)
==============================================================================================
* Fix output encoding when piping output to a pager like less (Python 2).

`2.0.2 <https://bitbucket.org/peteradrichem/xul/branches/compare/2.0.2%0D2.0.1>`_ (2020-05-31)
==============================================================================================
* Fix: removed encoding from Pygments formatter so highlight returns Unicode strings.

`2.0.1 <https://bitbucket.org/peteradrichem/xul/branches/compare/2.0.1%0D2.0.0>`_ (2020-03-08)
==============================================================================================
* Added "syntax" install extra (Pygments): ``pip install Xul[syntax]``

2.0.0 (2020-03-07)
==================
Open sourced Xul.


.. rubric:: Footnotes

.. [#NaN] NaN stands for “Not a Number”.
