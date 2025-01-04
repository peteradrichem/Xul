"""Pretty Print XML."""

import sys

# pylint: disable=no-name-in-module
from lxml.etree import tostring

# Import my own modules.
from .etree import build_etree

__all__ = ["prettyprint", "pp_xml"]


def _private_pp(etree, syntax=True, xml_declaration=None):
    """Pretty print XML ElementTree with (optional) syntax highlighting.

    https://lxml.de/api.html#serialisation
    https://lxml.de/apidoc/lxml.etree.html#lxml.etree.tostring
    """
    try:
        if sys.stdout.encoding is None:
            encoding = "utf-8"
        else:
            encoding = sys.stdout.encoding
        # lxml.etree.tostring returns bytes (bytestring).
        etree_string = tostring(
            etree, encoding=encoding, xml_declaration=xml_declaration, pretty_print=True
        )

        if syntax:
            # pygments.highlight() will return a Unicode string …
            # https://pygments.org/docs/formatters/
            etree_string = highlight(etree_string, lexer, Terminal256Formatter())
        else:
            # Bytes(string) => Unicode object.
            etree_string = etree_string.decode(encoding)

        # Fix output encoding errors (Python 2) when piping multiple etree_string.
        # E.g.: % ppx Unicode_1.xml Unicode_2.xml | less
        #       % xp -q "//d:OtherIdentifier[position()<=12]/.." Unicode.xml -p | less
        if not sys.stdout.isatty() and sys.stdout.encoding is None:
            # Standard out is buffered.
            sys.stdout.flush()
            sys.stdout = open(
                # Do not close sys.stdout file descriptor.
                sys.stdout.fileno(),
                "w",
                encoding=encoding,
                closefd=False,
            )
            print(etree_string)
            # Restore sys.stdout (reuse file descriptor).
            sys.stdout = sys.__stdout__
        else:
            print(etree_string)
    # Catch Broken pipe errors.
    except BrokenPipeError:
        pass


try:
    # pylint: disable=wrong-import-position
    from pygments import highlight
    from pygments.formatters import Terminal256Formatter
    from pygments.lexers import get_lexer_by_name
except ImportError:
    # pylint: disable=unused-argument
    def prettyprint(etree, syntax=False, xml_declaration=None):
        """Plain pretty print XML ElementTree (without syntax highlighting)."""
        return _private_pp(etree, syntax=False, xml_declaration=xml_declaration)

else:
    lexer = get_lexer_by_name("xml")

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
    if xml_tree := build_etree(xml_source, parser=parser):
        prettyprint(xml_tree, syntax=syntax, xml_declaration=xml_declaration)
