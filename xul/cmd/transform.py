# -*- coding: utf-8 -*-

"""Transform XML source with XSLT."""


from __future__ import print_function

from argparse import ArgumentParser
import sys
import errno

# pylint: disable=no-name-in-module
# lxml ElementTree <https://lxml.de/>
from lxml.etree import XMLParser, tostring

# Import my own modules.
from .. import __version__
from ..log import setup_logger_console
from ..xsl import build_xsl_transform, xml_transformer


def parse_cl():
    """Parse the command line for options, XSLT source and XML sources."""
    parser = ArgumentParser(
        description=__doc__)
    parser.add_argument(
        "-V", "--version", action="version",
        version="%(prog)s " + __version__)
    parser.add_argument("xslt_source", help="XSLT source (file, http://...)")
    parser.add_argument(
        "xml_sources", nargs='*',
        metavar='xml_source', help="XML source (file, <stdin>, http://...)")
    output_group = parser.add_mutually_exclusive_group(required=False)
    output_group.add_argument(
        "-x", "--xsl-output", action="store_true", default=False,
        dest="xsl_output", help="honor xsl:output")
    output_group.add_argument(
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
    if not result:
        pass
    elif result.getroot() is None:
        # Result is not an ElementTree.
        print(result)

    # https://lxml.de/xpathxslt.html#xslt-result-objects
    # https://lxml.de/api/lxml.etree._XSLTResultTree-class.html
    #   _XSLTResultTree (./src/lxml/xslt.pxi):
    elif args.xsl_output:
        try:
            # https://lxml.de/api/lxml.etree.XSLT-class.html
            # XSLT.tostring(). Deprecated: use str(result_tree) instead.
            #
            # Python 2: str(_XSLTResultTree) == bytes(_XSLTResultTree).
            #
            # Python 3: str(_XSLTResultTree) != bytes(_XSLTResultTree).
            # Standard output: sys.stdout.encoding (UTF-8).
            # Document labelled UTF-16 but has UTF-8 content:
            #   str(result, result.docinfo.encoding) ==
            #       bytes(result).decode(result.docinfo.encoding)
            print(result)
        # io.TextIOWrapper catches Python 3 BrokenPipeError.
        except IOError as e:
            # Python 2: catch 'IOError: [Errno 32] Broken pipe'.
            if e.errno != errno.EPIPE:
                sys.stderr.write("IOError: %s [%s]\n" % (e.strerror, e.errno))
        except LookupError as e:
            # LookupError: unknown encoding: UCS-4.
            sys.stderr.write("LookupError (XSLT result): %s\n" % e)

    # https://lxml.de/parsing.html#serialising-to-unicode-strings
    # For normal byte encodings, the tostring() function automatically adds
    # a declaration as needed that reflects the encoding of the returned string.
    else:
        etree_result = tostring(
            result, encoding='UTF-8', xml_declaration=args.declaration)
        # lxml.etree.tostring returns bytes (bytestring).
        try:
            if not isinstance(etree_result, str):
                # Bytes => unicode string (Python 3).
                etree_result = etree_result.decode("utf-8")
            print(etree_result)
        except IOError as e:
            # Python 2: catch 'IOError: [Errno 32] Broken pipe'.
            if e.errno != errno.EPIPE:
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
            sys.exit(70)
