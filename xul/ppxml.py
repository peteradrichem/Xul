# -*- coding: utf-8 -*-

"""Pretty Print XML with UTF-8 encoding."""


from __future__ import print_function

import sys
import codecs

# pylint: disable=no-name-in-module
# lxml ElementTree <https://lxml.de/>
from lxml.etree import tostring

# Import my own modules.
from .dom import build_etree


__all__ = ['prettyprint', 'pp_xml']

def _private_pp(etree, syntax=True, xml_declaration=None):
    """Pretty print XML ElementTree with (optional) syntax highlighting.

    https://lxml.de/api.html#serialisation
    https://lxml.de/api/lxml.etree-module.html#tostring
    """
    try:
        # lxml.etree.tostring returns bytes (bytestring).
        # https://docs.python.org/3/library/xml.etree.elementtree.html#xml.etree.ElementTree.tostring
        etree_string = tostring(
            etree, encoding='UTF-8',
            xml_declaration=xml_declaration, pretty_print=True)

        if syntax:
            # pygments.highlight() will return a Unicode string …
            # https://pygments.org/docs/formatters/
            etree_string = highlight(etree_string, lexer, Terminal256Formatter())
        else:
            # Bytes(string) => unicode string.
            etree_string = etree_string.decode("utf-8")

        # Fix output encoding (piping Python2 output to less).
        if sys.stdout.encoding is None:
            sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
        print(etree_string)
    except IOError as e:
        # Catch 'IOError: [Errno 32] Broken pipe' (multiple etrees).
        if e.errno != 32:
            sys.stderr.write("IOError: %s [%s]\n" % (e.strerror, e.errno))


try:
    # pylint: disable=wrong-import-position
    from pygments.lexers import get_lexer_by_name
    from pygments.formatters import Terminal256Formatter
    from pygments import highlight
except ImportError:
    # pylint: disable=unused-argument
    def prettyprint(etree, syntax=False, xml_declaration=None):
        """Plain pretty print XML ElementTree (without syntax highlighting)."""
        return _private_pp(etree, syntax=False, xml_declaration=xml_declaration)
else:
    lexer = get_lexer_by_name('xml')
    def prettyprint(etree, syntax=True, xml_declaration=None):
        """Pretty print XML ElementTree with (optional) syntax highlighting."""
        return _private_pp(etree, syntax=syntax, xml_declaration=xml_declaration)


def pp_xml(xml_source, parser=None, syntax=True, xml_declaration=None):
    """Pretty Print XML source.

    xml_source -- XML file, file-like object or URL
    parser -- (optional) XML parser (lxml.etree.XMLParser)
    syntax -- syntax highlighting (or not)
    xml_declaration -- print XML declaration (or not)
    """
    xml_tree = build_etree(xml_source, parser=parser)
    if xml_tree:
        prettyprint(xml_tree, syntax=syntax, xml_declaration=xml_declaration)
