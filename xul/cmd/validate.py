# -*- coding: utf-8 -*-

"""Validate XML source with XSD, DTD or RELAX NG."""


from __future__ import print_function

from argparse import ArgumentParser
import sys

# Import my own modules.
from .. import __version__
from ..log import setup_logger_console
from ..validate import build_xml_schema, build_dtd, build_relaxng
from ..validate import validate_xml


def parse_cl():
    """Parse the command line for options and XML sources."""
    parser = ArgumentParser(description=__doc__)
    parser.add_argument(
        "-V", "--version", action="version",
        version="%(prog)s " + __version__)
    lang_group = parser.add_mutually_exclusive_group(required=True)
    lang_group.add_argument(
        "-x", "--xsd",
        action="store", dest="xsd_source",
        help="XML Schema Definition (XSD) source")
    lang_group.add_argument(
        "-d", "--dtd",
        action="store", dest="dtd_source",
        help="Document Type Definition (DTD) source")
    lang_group.add_argument(
        "-r", "--relaxng",
        action="store", dest="relaxng_source",
        help="RELAX NG source")
    file_group = parser.add_mutually_exclusive_group(required=False)
    file_group.add_argument(
        "-f", "-l", "--validated-files",
        action="store_true", default=False, dest="validated_files",
        help="only the names of validated XML files are written to standard output")
    file_group.add_argument(
        "-F", "-L", "--invalidated-files",
        action="store_true", default=False, dest="invalidated_files",
        help="only the names of invalidated XML files are written to standard output")
    parser.add_argument(
        "xml_sources", nargs='*',
        metavar='xml_source', help="XML source (file, <stdin>, http://...)")
    return parser.parse_args()

def apply_validator(xml_source, validator, args):
    """Apply XML validator on an XML source."""
    if args.validated_files or args.invalidated_files:
        valid = validate_xml(xml_source, validator, silent=True)
        if (valid and args.validated_files) or (not valid and args.invalidated_files):
            if xml_source in ('-', sys.stdin):
                # <stdin>.
                print(sys.stdin.name)
            else:
                print(xml_source)
    else:
        validate_xml(xml_source, validator)

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
        sys.exit(60)

    # Validate XML sources.
    for xml_s in args.xml_sources:
        apply_validator(xml_s, validator, args)

    if not args.xml_sources:
        if not sys.stdin.isatty():
            # Read from a pipe when no XML source is specified.
            apply_validator(sys.stdin, validator, args)
        else:
            sys.stderr.write("Error: no XML source specified\n")
            sys.exit(70)
