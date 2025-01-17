"""Pretty Print XML."""

import sys
from typing import Optional, TextIO, Union

from lxml import etree

from .etree import build_etree

__all__ = ["prettyprint", "pp_xml"]


def _private_pp(
    el_tree: etree._ElementTree, syntax: bool = True, xml_declaration: bool = True
) -> None:
    """Pretty print XML ElementTree with (optional) syntax highlighting.

    :param el_tree: ElementTree to pretty print
    :param syntax: syntax highlighting (or not)
    :param xml_declaration: print an XML declaration (or not)

    Serialising to Unicode strings
        https://lxml.de/parsing.html#serialising-to-unicode-strings
    For normal byte encodings, the tostring() function automatically adds
    a declaration as needed that reflects the encoding of the returned string.

    Pretty printing
        https://lxml.de/api.html#serialisation

    lxml.etree.tostring
        https://lxml.de/apidoc/lxml.etree.html#lxml.etree.tostring
    """
    try:
        encoding = "utf-8" if sys.stdout.encoding is None else sys.stdout.encoding
        # lxml.etree.tostring returns bytes.
        etree_string = etree.tostring(
            el_tree, encoding=encoding, xml_declaration=xml_declaration, pretty_print=True
        )

        if syntax:
            # pygments.highlight() will return an Unicode string.
            # https://pygments.org/docs/formatters/
            print(highlight(etree_string, lexer, Terminal256Formatter()))
        else:
            # Bytes => Unicode string.
            print(etree_string.decode(encoding))  # type: ignore[union-attr]

    # Catch Broken pipe errors.
    except BrokenPipeError:
        sys.stderr.close()


try:
    # pylint: disable=wrong-import-position
    from pygments import highlight
    from pygments.formatters import Terminal256Formatter
    from pygments.lexers import get_lexer_by_name
except ImportError:
    # pylint: disable=unused-argument
    def prettyprint(
        el_tree: etree._ElementTree, syntax: bool = False, xml_declaration: bool = True
    ) -> None:
        """Plain pretty print XML ElementTree (without syntax highlighting).

        :param el_tree: ElementTree to pretty print
        :param syntax: syntax highlighting (or not)
        :param xml_declaration: print an XML declaration (or not)
        """
        return _private_pp(el_tree, syntax=False, xml_declaration=xml_declaration)

else:
    lexer = get_lexer_by_name("xml")

    def prettyprint(
        el_tree: etree._ElementTree, syntax: bool = True, xml_declaration: bool = True
    ) -> None:
        """Pretty print XML ElementTree with (optional) syntax highlighting.

        :param el_tree: ElementTree to pretty print
        :param syntax: syntax highlighting (or not)
        :param xml_declaration: print an XML declaration (or not)
        """
        return _private_pp(el_tree, syntax=syntax, xml_declaration=xml_declaration)


def pp_xml(
    xml_source: Union[TextIO, str],
    parser: Optional[etree.XMLParser] = None,
    syntax: bool = True,
    xml_declaration: bool = True,
) -> None:
    """Pretty Print XML source.

    :param xml_source: XML file, file-like object or URL
    :param parser: (optional) XML parser
    :param syntax: syntax highlighting (or not)
    :param xml_declaration: print an XML declaration (or not)
    """
    if xml_tree := build_etree(xml_source, parser=parser):
        prettyprint(xml_tree, syntax=syntax, xml_declaration=xml_declaration)
