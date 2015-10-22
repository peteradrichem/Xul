# coding=utf-8

"""Pretty print XML with UTF-8 encoding."""


# Standard Python
from sys import stderr
#
# pylint: disable=no-name-in-module
# lxml ElementTree <http://lxml.de/>
from lxml.etree import tostring

# Import my own modules
from .dom import build_etree


__all__ = ['prettyprint', 'pp_xml']

def _private_pp(etree, color=True, xml_declaration=None):
    """Pretty print XML ElementTree in (optional) color.

    http://lxml.de/api.html#serialisation
    http://lxml.de/api/lxml.etree-module.html#tostring
    """
    try:
        etree_str = tostring(
            etree, encoding='UTF-8',
            xml_declaration=xml_declaration, pretty_print=True)
        if color:
            print highlight(etree_str, lexer, formatter)
        else:
            print etree_str
    except IOError as e:
        # Catch 'IOError: [Errno 32] Broken pipe' (multiple etrees).
        if e.errno != 32:
            stderr.write("IOError: %s [%s]\n" % (e.strerror, e.errno))


try:
    from pygments.lexers import get_lexer_by_name
    from pygments.formatters.terminal256 import Terminal256Formatter
    from pygments import highlight
except ImportError:
    # pylint: disable=unused-argument
    def prettyprint(etree, color=False, xml_declaration=None):
        """Plain pretty print XML ElementTree (without color)."""
        return _private_pp(etree, color=False, xml_declaration=xml_declaration)
else:
    lexer = get_lexer_by_name('xml', encoding='utf-8')
    formatter = Terminal256Formatter(encoding='utf-8', nobold=True)
    def prettyprint(etree, color=True, xml_declaration=None):
        """Pretty print XML ElementTree in (optional) color."""
        return _private_pp(etree, color=color, xml_declaration=xml_declaration)


def pp_xml(xml_source, parser=None, color=True):
    """Pretty print an XML file.

    xml_source -- XML file or file-like object
    parser -- (optional) XML parser (lxml.etree.XMLParser)
    color -- pretty print in color (or not)
    """
    xml_tree = build_etree(xml_source, parser=parser)
    if xml_tree:
        prettyprint(xml_tree, color=color, xml_declaration=True)
