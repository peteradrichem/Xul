# -*- coding: utf-8 -*-

"""Validate XML source with XSD, DTD or RELAX NG."""


from __future__ import print_function

# Standard Python.
from argparse import ArgumentParser
import sys

# Import my own modules.
from .. import __version__
from ..log import setup_logger_console
from ..validate import build_xml_schema, build_dtd, build_relaxng
from ..validate import xml_validator


def parse_cl():
    """Parse the command line for options and XML sources."""
    parser = ArgumentParser(description=__doc__)
    parser.add_argument(
        "-V", "--version", action="version",
        version="%(prog)s " + __version__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "-x", "--xsd",
        action="store", dest="xsd_source",
        help="XML Schema Definition (XSD) source")
    group.add_argument(
        "-d", "--dtd",
        action="store", dest="dtd_source",
        help="Document Type Definition (DTD) source")
    group.add_argument(
        "-r", "--relaxng",
        action="store", dest="relaxng_source",
        help="RELAX NG source")
    parser.add_argument(
        "xml_sources", nargs='*',
        metavar='xml_source', help="XML source (file, <stdin>, http://...)")
    return parser.parse_args()


def main():
    """validate command line script entry point."""
    # Logging to the console.
    setup_logger_console()

    # Command line.
    args = parse_cl()

    # XSD or DTD Validator?
    if args.xsd_source:
        validator = build_xml_schema(args.xsd_source)
    elif args.dtd_source:
        validator = build_dtd(args.dtd_source)
    elif args.relaxng_source:
        validator = build_relaxng(args.relaxng_source)
    else:
        validator = None
    # Check validator.
    if not validator:
        sys.exit(105)

    # Validate XML sources.
    for xml_s in args.xml_sources:
        xml_validator(xml_s, validator)

    if not args.xml_sources:
        # Read from a pipe when no XML source is specified.
        if not sys.stdin.isatty():
            xml_validator(sys.stdin, validator)
        else:
            sys.stderr.write("Error: no XML source specified\n")
