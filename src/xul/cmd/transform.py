"""Transform an XML source with XSLT."""

import argparse
import sys
from typing import TextIO, Union

from lxml import etree

from .. import __version__
from ..ppxml import prettyprint
from ..utils import config_logger
from ..xsl import build_xsl_transform, xml_transformer


def parse_cl() -> argparse.Namespace:
    """Parse the command line for options, XSLT source and XML sources."""
    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument("-V", "--version", action="version", version="%(prog)s " + __version__)
    parser.add_argument("xslt_source", help="XSLT source (file, http://...)")
    parser.add_argument(
        "xml_source", nargs="?", default=sys.stdin, help="XML source (file, <stdin>, http://...)"
    )
    parser.add_argument("-f", "--file", dest="file", help="save result to file")

    output_group = parser.add_argument_group("terminal output options")
    output_group.add_argument(
        "-n",
        "--no-syntax",
        action="store_false",
        default=True,
        dest="syntax",
        help="no syntax highlighting",
    )
    output_group.add_argument(
        "-o",
        "--omit-declaration",
        action="store_false",
        default=True,
        dest="declaration",
        help="omit the XML declaration",
    )

    return parser.parse_args()


def print_result(result) -> None:
    """Print transformation result (catch broken pipe and lookup errors)."""
    try:
        print(result)
    except BrokenPipeError:
        pass
    except LookupError as e:
        # LookupError: unknown encoding: UCS-4.
        sys.stderr.write(f"Cannot print XSLT result (LookupError): {e}\n")


def output_xslt(
    xml_source: Union[TextIO, str],
    transformer: etree.XSLT,
    parser: etree.XMLParser,
    args: argparse.Namespace,
) -> None:
    """Print or save the result of an XSL Transformation.

    :param xml_source: XML file, file-like object or URL
    :param transformer: XSL Transformer
    :param parser: XML parser
    :param args: command-line arguments
    """
    result = xml_transformer(xml_source, transformer, parser)
    if not result:
        return None

    # Result is an lxml.etree._XSLTResultTree.
    # https://lxml.de/apidoc/lxml.etree.html#lxml.etree._XSLTResultTree

    if args.file:
        return result.write_output(args.file)  # type: ignore[attr-defined]

    # https://lxml.de/xpathxslt.html#xslt-result-objects
    if result.getroot() is None:
        # Result is not an ElementTree.
        return print_result(result)

    prettyprint(result, syntax=args.syntax, xml_declaration=args.declaration)


def main():
    """Entry point for command line script transform."""
    # Logging to the console.
    config_logger()

    # Command line.
    args = parse_cl()

    # Check XSLT source.
    if args:
        # Build an XSL Transformer from an XSLT source.
        transformer = build_xsl_transform(args.xslt_source)
        if not transformer:
            sys.stderr.write("Invalid XSLT source specified\n")
            sys.exit(60)
    else:
        sys.stderr.write("No XSLT source specified\n")
        sys.exit(50)

    # Transform XML source with XSL Transformer.
    output_xslt(args.xml_source, transformer, etree.XMLParser(), args)
