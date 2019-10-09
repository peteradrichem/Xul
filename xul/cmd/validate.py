# -*- coding: utf-8 -*-

"""Validate XML source with XSD or DTD."""


from __future__ import print_function

# Standard Python.
from argparse import ArgumentParser
import sys

# Import my own modules.
from .. import __version__
from ..log import setup_logger_console
from ..dom import build_etree, build_xml_schema, build_dtd


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
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "-x", "--xsd",
        action="store", dest="xsd_source",
        help="XML Schema Definition (XSD) source")
    group.add_argument(
        "-d", "--dtd",
        action="store", dest="dtd_source",
        help="Document Type Definition (DTD) source")
    return parser.parse_args()


def validate_xml(xml_source, validator, val_source):
    """Validate XML source against an XSD or DTD validator.

    xml_source -- XML file, file-like object or URL
    validator -- XSD or DTD Validator
    val_source -- Validator source (XSD or DTD)
    """
    xml_dom = build_etree(xml_source)
    if xml_dom:
        if hasattr(xml_source, "name"):
            name = xml_source.name
        else:
            name = xml_source
        if validator.validate(xml_dom):
            print("'%s' validates against '%s'" % (name, val_source))
        else:
            sys.stderr.write(
                "'%s' does not validate against '%s':\n" % (name, val_source))
            for e in validator.error_log:
                sys.stderr.write(
                    "\tline %i, column %i: %s\n" % (e.line, e.column, e.message))


def main():
    """validate command line script entry point."""
    # Logging to the console.
    setup_logger_console()

    # Command line.
    args = parse_cl()

    # XSD or DTD Validator?
    if args.xsd_source:
        validator = build_xml_schema(args.xsd_source)
        val_source = args.xsd_source
        val_type = "XSD"
    elif args.dtd_source:
        validator = build_dtd(args.dtd_source)
        val_source = args.dtd_source
        val_type = "DTD"
    else:
        validator = None
        val_source = None
    # Check validator.
    if not validator:
        sys.stderr.write('Invalid %s source specified\n' % val_type)
        sys.exit(105)

    # Validate XML sources.
    for xml_s in args.xml_sources:
        validate_xml(xml_s, validator, val_source)

    if not args.xml_sources:
        # Read from a pipe when no XML source is specified.
        if not sys.stdin.isatty():
            validate_xml(sys.stdin, validator, val_source)
        else:
            sys.stderr.write("Error: no XML source specified\n")
