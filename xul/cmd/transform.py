# coding=utf-8

"""Transform XML file(s) with an XSL file."""


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
    """Parse the command-line for options and XML files."""
    cl_parser = OptionParser(
        usage="%prog -x xsl_file xml_file ...",
        description=__doc__,
        version="%prog " + __version__)
    cl_parser.add_option(
        "-x", "--xsl",
        action="store", type="string", dest="xsl_file",
        help="XSL file to transform XML file(s)")
    return cl_parser.parse_args()


def print_xslt(xml_source, transformer, parser):
    """XSL Transform an XML file object and print the result.

    xml_source -- XML file or file-like object
    transformer -- XSL Transformer (lxml.etree.XSLT)
    parser -- XML parser (lxml.etree.XMLParser)
    """
    result = xml_transformer(xml_source, transformer, parser)
    if result:
        if result.getroot() is None:
            # XSLT result is not an ElementTree. Print as text
            print result
        else:
            prettyprint(result, xml_declaration=True)


def main():
    """Main command line entry point."""
    # Logging to the console
    setup_logger_console()

    # Command-line
    (options, xml_files) = parse_cl()

    # Build an XSL Transformer (XSLT) from an XSL file
    if options.xsl_file:
        transformer = build_xsl_transform(options.xsl_file)
    else:
        stderr.write('No XSL file specified\n')
        exit(105)
    if not transformer:
        stderr.write('Invalid XSL file specified\n')
        exit(105)
    # Initialise XML parser
    parser = XMLParser()

    # Transform XML sources with XSL
    for xml_f in xml_files:
        print_xslt(xml_f, transformer, parser)

    if not xml_files:
        # Read from a pipe when no XML is specified
        if not stdin.isatty():
            print_xslt(stdin, transformer, parser)
        else:
            stderr.write("Error: no XML is given\n")
