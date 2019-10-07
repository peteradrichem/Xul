# -*- coding: utf-8 -*-

"""Transform XML source with XSLT."""


from __future__ import print_function

# Standard Python.
from optparse import OptionParser
from sys import stderr, stdin
#
# pylint: disable=no-name-in-module
# lxml ElementTree <https://lxml.de/>
from lxml.etree import XMLParser, tostring

# Import my own modules.
from .. import __version__
from ..log import setup_logger_console
from ..dom import build_xsl_transform, xml_transformer


def parse_cl():
    """Parse the command line for XSLT source, options and XML sources."""
    cl_parser = OptionParser(
        usage="%prog xslt_source [-o] xml_source ...",
        description=__doc__,
        version="%prog " + __version__)
    cl_parser.add_option(
        "-o", "--omit-declaration", action="store_false", default=True,
        dest="declaration", help="omit the XML declaration")
    return cl_parser.parse_args()


def print_xslt(xml_source, transformer, parser, options):
    """Print the result of an XSL Transformation.

    xml_source -- XML file, file-like object or URL
    transformer -- XSL Transformer (lxml.etree.XSLT)
    parser -- XML parser (lxml.etree.XMLParser)
    options -- Command-line options
    """
    result = xml_transformer(xml_source, transformer, parser)
    if result:
        if result.getroot() is None:
            # Result is not an ElementTree. Print as text.
            print(result)
        else:
            # lxml.etree.tostring returns bytes (bytestring).
            etree_result = tostring(
                result, encoding='UTF-8', xml_declaration=options.declaration)
            try:
                if not isinstance(etree_result, str):
                    # Bytes => unicode string (Python 3).
                    etree_result = etree_result.decode("utf-8")
                print(etree_result)
            except IOError as e:
                # Catch 'IOError: [Errno 32] Broken pipe'.
                if e.errno != 32:
                    stderr.write("IOError: %s [%s]\n" % (e.strerror, e.errno))


def main():
    """Main command line entry point."""
    # Logging to the console.
    setup_logger_console()

    # Command line.
    (options, args) = parse_cl()

    # Check XSLT source.
    if args:
        xslt_source = args[0]
        # Build an XSL Transformer from an XSLT source.
        transformer = build_xsl_transform(xslt_source)
        if transformer:
            xml_sources = args[1:]
        else:
            stderr.write('Invalid XSLT source specified\n')
            exit(60)
    else:
        stderr.write('No XSLT source specified\n')
        exit(50)
    # Initialise XML parser.
    parser = XMLParser()

    # Transform XML sources with XSL Transformer.
    for xml_s in xml_sources:
        print_xslt(xml_s, transformer, parser, options)

    if not xml_sources:
        # Read from a pipe when no XML source is specified.
        if not stdin.isatty():
            print_xslt(stdin, transformer, parser, options)
        else:
            stderr.write("Error: no XML source specified\n")
