# -*- coding: utf-8 -*-

"""Transform XML source with XSLT."""


from __future__ import print_function

# Standard Python.
from argparse import ArgumentParser
import sys
#
# pylint: disable=no-name-in-module
# lxml ElementTree <https://lxml.de/>
from lxml.etree import XMLParser, tostring

# Import my own modules.
from .. import __version__
from ..log import setup_logger_console
from ..dom import build_xsl_transform, xml_transformer


def parse_cl():
    """Parse the command line for options, XSLT source and XML sources."""
    parser = ArgumentParser(
        #usage="%(prog)s xslt_source [-o] xml_source ...",
        description=__doc__)
    parser.add_argument(
        "-V", "--version", action="version",
        version="%(prog)s " + __version__)
    parser.add_argument("xslt_source", help="XSLT source (file, http://...)")
    parser.add_argument(
        "xml_sources", nargs='*',
        metavar='xml_source', help="XML source (file, <stdin>, http://...)")
    parser.add_argument(
        "-o", "--omit-declaration", action="store_false", default=True,
        dest="declaration", help="omit the XML declaration")
    return parser.parse_args()


def print_xslt(xml_source, transformer, parser, args):
    """Print the result of an XSL Transformation.

    xml_source -- XML file, file-like object or URL
    transformer -- XSL Transformer (lxml.etree.XSLT)
    parser -- XML parser (lxml.etree.XMLParser)
    args -- Command-line arguments
    """
    result = xml_transformer(xml_source, transformer, parser)
    if result:
        if result.getroot() is None:
            # Result is not an ElementTree. Print as text.
            print(result)
        else:
            # lxml.etree.tostring returns bytes (bytestring).
            etree_result = tostring(
                result, encoding='UTF-8', xml_declaration=args.declaration)
            try:
                if not isinstance(etree_result, str):
                    # Bytes => unicode string (Python 3).
                    etree_result = etree_result.decode("utf-8")
                print(etree_result)
            except IOError as e:
                # Catch 'IOError: [Errno 32] Broken pipe'.
                if e.errno != 32:
                    sys.stderr.write("IOError: %s [%s]\n" % (e.strerror, e.errno))


def main():
    """transform command line script entry point."""
    # Logging to the console.
    setup_logger_console()

    # Command line.
    args = parse_cl()

    # Check XSLT source.
    if args:
        # Build an XSL Transformer from an XSLT source.
        transformer = build_xsl_transform(args.xslt_source)
        if not transformer:
            sys.stderr.write('Invalid XSLT source specified\n')
            sys.exit(60)
    else:
        sys.stderr.write('No XSLT source specified\n')
        sys.exit(50)
    # Initialise XML parser.
    parser = XMLParser()

    # Transform XML sources with XSL Transformer.
    for xml_s in args.xml_sources:
        print_xslt(xml_s, transformer, parser, args)

    if not args.xml_sources:
        # Read from a pipe when no XML source is specified.
        if not sys.stdin.isatty():
            print_xslt(sys.stdin, transformer, parser, args)
        else:
            sys.stderr.write("Error: no XML source specified\n")
