"""Transform XML source with XSLT."""

import argparse
import sys
from typing import TextIO, Union

from lxml import etree

from .. import __version__
from ..log import setup_logger_console
from ..xsl import build_xsl_transform, xml_transformer


def parse_cl() -> argparse.Namespace:
    """Parse the command line for options, XSLT source and XML sources."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-V", "--version", action="version", version="%(prog)s " + __version__)
    parser.add_argument("xslt_source", help="XSLT source (file, http://...)")
    parser.add_argument(
        "xml_source",
        nargs="?",
        default=sys.stdin,
        type=argparse.FileType("r"),
        help="XML source (file, <stdin>, http://...)",
    )
    output_group = parser.add_mutually_exclusive_group(required=False)
    output_group.add_argument(
        "-x",
        "--xsl-output",
        action="store_true",
        default=False,
        dest="xsl_output",
        help="honor xsl:output",
    )
    output_group.add_argument(
        "-o",
        "--omit-declaration",
        action="store_false",
        default=True,
        dest="declaration",
        help="omit the XML declaration",
    )
    parser.add_argument("-f", "--file", dest="file", help="save result to file")
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


def save_to_file(result, target_file: str) -> None:
    """Save transformation result to file."""
    try:
        with open(target_file, "bx") as file_object:
            file_object.write(result)
    except OSError as e:
        sys.stderr.write(f"Saving result to {target_file} failed: {e.strerror}\n")
        sys.exit(80)


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

    # https://lxml.de/apidoc/lxml.etree.html#lxml.etree._XSLTResultTree
    #   _XSLTResultTree (./src/lxml/xslt.pxi):
    if result.getroot() is None:
        # Result (lxml.etree._XSLTResultTree) is not an ElementTree.
        if args.file:
            save_to_file(result, args.file)
        else:
            print_result(result)
        return None

    # https://lxml.de/xpathxslt.html#xslt-result-objects
    if args.xsl_output:
        if args.file:
            save_to_file(result, args.file)
        else:
            # Standard output: sys.stdout.encoding.
            # Document labelled UTF-16 but has UTF-8 content:
            #   str(result, result.docinfo.encoding) ==
            #       bytes(result).decode(result.docinfo.encoding)
            print_result(result)

    # https://lxml.de/parsing.html#serialising-to-unicode-strings
    # For normal byte encodings, the tostring() function automatically adds
    # a declaration as needed that reflects the encoding of the returned string.
    else:
        # lxml.etree.tostring returns bytes.
        etree_result = etree.tostring(
            result, encoding=result.docinfo.encoding, xml_declaration=args.declaration
        )
        if args.file:
            save_to_file(etree_result, args.file)
        else:
            # Bytes => unicode string (Python 3).
            print_result(etree_result.decode(result.docinfo.encoding))  # type: ignore[arg-type,union-attr]

    return None


def main():
    """Entry point for command line script transform."""
    # Logging to the console.
    setup_logger_console()

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

    # Initialise XML parser.
    parser = etree.XMLParser()
    # Transform XML source with XSL Transformer.
    output_xslt(args.xml_source, transformer, parser, args)
