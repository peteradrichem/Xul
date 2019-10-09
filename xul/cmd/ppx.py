# -*- coding: utf-8 -*-

"""Pretty Print XML source in human readable form."""


# Standard Python.
from argparse import ArgumentParser
from sys import stdin, stderr
#
# pylint: disable=no-name-in-module
# lxml ElementTree <https://lxml.de/>
from lxml.etree import XMLParser

# Import my own modules.
from .. import __version__
from ..log import setup_logger_console
from ..ppxml import pp_xml


def parse_cl():
    """Parse the command line for options and XML sources."""
    parser = ArgumentParser(
        description=__doc__)
    parser.add_argument(
        "-V", "--version", action="version",
        version="%(prog)s " + __version__)
    parser.add_argument(
        "xml_sources", nargs='*',
        metavar='xml_source', help="XML source (file, <stdin>, http://...)")
    parser.add_argument(
        "-n", "--no-syntax", action="store_false", default=True,
        dest="syntax", help="no syntax highlighting")
    parser.add_argument(
        "-o", "--omit-declaration", action="store_false", default=True,
        dest="declaration", help="omit the XML declaration")
    return parser.parse_args()


def main():
    """ppx command line script entry point."""
    # Logging to the console.
    setup_logger_console()

    # Command line.
    args = parse_cl()

    # Initialise XML parser and remove blank text for 'pretty_print' formatting.
    #   https://lxml.de/FAQ.html#parsing-and-serialisation
    parser = XMLParser(remove_blank_text=True)

    # Pretty print XML sources.
    for xml_s in args.xml_sources:
        pp_xml(
            xml_s, parser=parser,
            syntax=args.syntax,
            xml_declaration=args.declaration)

    if not args.xml_sources:
        # Read from a pipe when no XML source is specified.
        if not stdin.isatty():
            pp_xml(
                stdin, parser=parser,
                syntax=args.syntax,
                xml_declaration=args.declaration)
        else:
            stderr.write("Error: no XML source specified\n")
