# coding=utf-8

"""Transform XML source with XSLT."""


# Standard Python
from optparse import OptionParser
from sys import stderr, stdin
#
# pylint: disable=no-name-in-module
# lxml ElementTree <http://lxml.de/>
from lxml.etree import XMLParser

# Import my own modules
from .. import __version__
from ..log import setup_logger_console
from ..dom import build_xsl_transform, xml_transformer
from ..ppxml import prettyprint


def parse_cl():
    """Parse the command-line for options and XML sources."""
    cl_parser = OptionParser(
        usage="%prog [-o] -x xslt_source xml_source ...",
        description=__doc__,
        version="%prog " + __version__)
    cl_parser.add_option(
        "-x", "--xslt",
        action="store", type="string", dest="xslt_source",
        help="XSLT source for transforming XML source(s)")
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
            # Result is not an ElementTree. Print as text
            print result
        else:
            prettyprint(result, xml_declaration=options.declaration)


def main():
    """Main command line entry point."""
    # Logging to the console
    setup_logger_console()

    # Command-line
    (options, xml_sources) = parse_cl()

    if options.xslt_source:
        # Build an XSL Transformer from an XSLT source
        transformer = build_xsl_transform(options.xslt_source)
    else:
        stderr.write('No XSLT source specified\n')
        exit(105)
    if not transformer:
        stderr.write('Invalid XSLT source specified\n')
        exit(105)
    # Initialise XML parser
    parser = XMLParser()

    # Transform XML sources with XSL Transformer
    for xml_s in xml_sources:
        print_xslt(xml_s, transformer, parser, options)

    if not xml_sources:
        # Read from a pipe when no XML source is specified
        if not stdin.isatty():
            print_xslt(stdin, transformer, parser, options)
        else:
            stderr.write("Error: no XML source specified\n")
