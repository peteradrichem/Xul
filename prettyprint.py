#!/usr/local/bin/python -t
# coding=utf-8

"""Pretty print XML files."""


# Standard Python
from optparse import OptionParser
from sys import stdin
#
# pylint: disable=no-name-in-module
# lxml ElementTree <http://lxml.de/>
from lxml.etree import XMLParser
#
# Xul modules
from xul.log import setup_logger_console
from xul.dom import build_etree
from xul.ppxml import prettyprint


__version_info__ = ('1', '1', '0')
__version__ = '.'.join(__version_info__)

def parse_cl():
    """Parse the command-line for options and XML files."""
    cl_parser = OptionParser(
        usage="\t%prog [-n] xml_file_1 ... xml_file_n",
        description=__doc__,
        version="%prog " + __version__)
    cl_parser.add_option(
        "-n", "--no-color", action="store_false", default=True,
        dest="color", help="disable colored output")

    return cl_parser.parse_args()


if __name__ == '__main__':
    # Logging to the console (TAB modules)
    setup_logger_console()

    # Command-line
    (options, xml_files) = parse_cl()

    # Initialise XML parser and remove blank text for 'pretty_print' formatting
    #   http://lxml.de/FAQ.html#parsing-and-serialisation
    parser = XMLParser(remove_blank_text=True)

    # Pretty print XML files
    for xml_f in xml_files:
        # Opm: build_etree rapporteert XML fouten in xml_f
        xml_tree = build_etree(xml_f, parser=parser)
        if xml_tree:
            prettyprint(xml_tree, color=options.color, xml_declaration=True)

    # Read from standard input when no XML files are specified
    if not xml_files:
        xml_tree = build_etree(stdin, parser=parser)
        if xml_tree:
            prettyprint(xml_tree, color=options.color, xml_declaration=True)
