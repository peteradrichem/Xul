# coding=utf-8

"""Pretty print XML files."""


# Standard Python
from optparse import OptionParser
from sys import stdin
#
# pylint: disable=no-name-in-module
# lxml ElementTree <http://lxml.de/>
from lxml.etree import XMLParser

# Import my own modules
from .. import __version__
from ..log import setup_logger_console
from ..ppxml import pp_xml


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


def main():
    """Main command line entry point."""
    # Logging to the console
    setup_logger_console()

    # Command-line
    (options, xml_files) = parse_cl()

    # Initialise XML parser and remove blank text for 'pretty_print' formatting
    #   http://lxml.de/FAQ.html#parsing-and-serialisation
    parser = XMLParser(remove_blank_text=True)

    # Pretty print XML files
    for xml_f in xml_files:
        pp_xml(xml_f, parser=parser, color=options.color)

    # Read from standard input when no XML files are specified
    if not xml_files:
        pp_xml(stdin, parser=parser, color=options.color)
