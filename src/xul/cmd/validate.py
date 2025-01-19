"""Validate an XML source with XSD, DTD or RELAX NG."""

import argparse
import sys
from typing import TextIO, Union

from lxml import etree

from .. import __version__
from ..utils import config_logger, get_source_name
from ..validate import build_dtd, build_relaxng, build_xml_schema, validate_xml


def parse_cl() -> argparse.Namespace:
    """Parse the command line for options and XML sources."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-V", "--version", action="version", version="%(prog)s " + __version__)
    validator_args_group = parser.add_argument_group(
        title="XML validator", description="choose an XML validator: XSD, DTD or RELAX NG"
    )
    validator_group = validator_args_group.add_mutually_exclusive_group(required=True)
    validator_group.add_argument(
        "-x", "--xsd", action="store", dest="xsd_source", help="XML Schema Definition (XSD) source"
    )
    validator_group.add_argument(
        "-d",
        "--dtd",
        action="store",
        dest="dtd_source",
        help="Document Type Definition (DTD) source",
    )
    validator_group.add_argument(
        "-r", "--relaxng", action="store", dest="relaxng_source", help="RELAX NG source"
    )
    file_group = parser.add_argument_group(
        title="file hit options", description="output filenames to standard output"
    )
    file_hit_group = file_group.add_mutually_exclusive_group(required=False)
    file_hit_group.add_argument(
        "-l",
        "-f",
        "--validated-files",
        action="store_true",
        default=False,
        dest="validated_files",
        help="only the names of validated XML files are written to standard output",
    )
    file_hit_group.add_argument(
        "-L",
        "-F",
        "--invalidated-files",
        action="store_true",
        default=False,
        dest="invalidated_files",
        help="only the names of invalidated XML files are written to standard output",
    )
    parser.add_argument(
        "xml_sources",
        nargs="*",
        metavar="xml_source",
        help="XML source (file, <stdin>, http://...)",
    )
    return parser.parse_args()


def apply_validator(
    xml_source: Union[TextIO, str],
    validator: Union[etree.XMLSchema, etree.DTD, etree.RelaxNG],
    args: argparse.Namespace,
) -> None:
    """Apply XML validator on an XML source.

    :param xml_source: XML file, file-like object or URL
    :param validator: XMLSchema, DTD or RELAX NG validator
    :param args: command-line arguments
    """
    if args.validated_files or args.invalidated_files:
        valid = validate_xml(xml_source, validator, silent=True)
        if (valid and args.validated_files) or (not valid and args.invalidated_files):
            print(get_source_name(xml_source))
    else:
        validate_xml(xml_source, validator)


def main() -> None:
    """Entry point for command line script validate."""
    # Logging to the console.
    config_logger()

    # Command line.
    args = parse_cl()

    # XSD, DTD or RelaxNG Validator?
    validator: Union[etree.XMLSchema, etree.DTD, etree.RelaxNG]
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
