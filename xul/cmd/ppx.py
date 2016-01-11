# coding=utf-8

"""Pretty Print XML source in human readable form."""


# Standard Python
from optparse import OptionParser
from sys import stdin, stderr
#
# pylint: disable=no-name-in-module
# lxml ElementTree <http://lxml.de/>
from lxml.etree import XMLParser

# Import my own modules
from .. import __version__
from ..log import setup_logger_console
from ..ppxml import pp_xml


def parse_cl():
    """Parse the command-line for options and XML sources."""
    parser = OptionParser(
        usage="\t%prog [-no] xml_source ...",
        description=__doc__,
        version="%prog " + __version__)
    parser.add_option(
        "-n", "--no-syntax", action="store_false", default=True,
        dest="syntax", help="no syntax highlighting")
    parser.add_option(
        "-o", "--omit-declaration", action="store_false", default=True,
        dest="declaration", help="omit the XML declaration")
    return parser.parse_args()


def main():
    """Main command line entry point."""
    # Logging to the console
    setup_logger_console()

    # Command-line
    (options, xml_sources) = parse_cl()

    # Initialise XML parser and remove blank text for 'pretty_print' formatting
    #   http://lxml.de/FAQ.html#parsing-and-serialisation
    parser = XMLParser(remove_blank_text=True)

    # Pretty print XML sources
    for xml_s in xml_sources:
        pp_xml(
            xml_s, parser=parser,
            syntax=options.syntax,
            xml_declaration=options.declaration)

    if not xml_sources:
        # Read from a pipe when no XML source is specified
        if not stdin.isatty():
            pp_xml(
                stdin, parser=parser,
                syntax=options.syntax,
                xml_declaration=options.declaration)
        else:
            stderr.write("Error: no XML source specified\n")
