#!/usr/local/bin/python -t
# coding=utf-8

"""Transform XML file(s) with an XSL file."""


# Standard Python
from optparse import OptionParser
from sys import stderr
#
# pylint: disable=no-name-in-module
# lxml ElementTree <http://lxml.de/>
from lxml.etree import XMLParser
#
# Xul modules
from xul import __version__
from xul.log import setup_logger_console
from xul.dom import build_xsl_transform, xml_transformer
from xul.ppxml import prettyprint


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


if __name__ == '__main__':
    # Logging to the console (TAB modules)
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

    # Transform XML files with XSL
    if not xml_files:
        stderr.write("Valid XSL file '%s'\n" % options.xsl_file)
        stderr.write("But no XML file(s) to operate on\n")
        exit(0)
    # Initialise XML parser
    parser = XMLParser()
    for xml_f in xml_files:
        # Opm: xml_transformer rapporteert XML fouten in xml_f etc.
        result = xml_transformer(xml_f, transformer, parser)
        if result:
            if result.getroot() is None:
                # XSLT result is not an ElementTree. Print as text
                print result
            else:
                prettyprint(result, xml_declaration=True)
