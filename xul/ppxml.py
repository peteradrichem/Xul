# coding=utf-8

"""Pretty print XML with UTF-8 encoding."""


# Standard Python
from sys import stdout
#
# pylint: disable=no-name-in-module
# lxml ElementTree <http://lxml.de/>
from lxml.etree import tostring


def no_color_pp(etree, xml_declaration=True):
    """Pretty print XML ElementTree without color.

    https://docs.python.org/2/library/xml.etree.elementtree.html#xml.etree.ElementTree.ElementTree.write
    """
    etree.write(
        stdout, encoding='UTF-8',
        xml_declaration=xml_declaration, pretty_print=True)


try:
    from pygments.lexers import get_lexer_by_name
    from pygments.formatters.terminal256 import Terminal256Formatter
    from pygments import highlight
except ImportError:
    # pylint: disable=unused-argument
    def prettyprint(etree, color=False, xml_declaration=True):
        """Redirect to no_color_pp."""
        return no_color_pp(etree, xml_declaration=xml_declaration)
else:
    lexer = get_lexer_by_name('xml', encoding='utf-8')
    formatter = Terminal256Formatter(encoding='utf-8', nobold=True)
    def prettyprint(etree, color=True, xml_declaration=True):
        """Pretty print XML ElementTree in (Pygments) color."""
        if color:
            etree_str = tostring(
                etree, encoding='UTF-8',
                xml_declaration=xml_declaration, pretty_print=True)
            print highlight(etree_str, lexer, formatter)
        else:
            return no_color_pp(etree, xml_declaration=xml_declaration)
