# coding=utf-8

"""Validate XML file(s) with an XSD or DTD file."""


# Standard Python
from optparse import OptionParser
from sys import stderr, stdin

# Import my own modules
from .. import __version__
from ..log import setup_logger_console
from ..dom import build_etree, build_xml_schema, build_dtd


def parse_cl():
    """Parse the command-line for options and XML files."""
    parser = OptionParser(
        usage="""\t%prog -x xsd_file xml_file_1 ... xml_file_n
\t%prog -d dtd_file xml_file_1 ... xml_file_n""",
        description=__doc__,
        version="%prog " + __version__)
    parser.add_option(
        "-x", "--xsd",
        action="store", type="string", dest="xsd_file",
        help="XSD file to validate XML file(s)")
    parser.add_option(
        "-d", "--dtd",
        action="store", type="string", dest="dtd_file",
        help="DTD file to validate XML file(s)")
    return parser.parse_args()


def validate_xml(xml_source, validator, val_file):
    """Validate XML source against an XSD or DTD validator.

    xml_source -- XML file or file-like object
    validator -- XMLSchema or DTD Validator
    val_file -- Validator file (XSD or DTD)
    """
    xml_dom = build_etree(xml_source)
    if xml_dom:
        if hasattr(xml_source, "name"):
            name = xml_source.name
        else:
            name = xml_source
        if validator.validate(xml_dom):
            print "'%s' validates against '%s'" % (name, val_file)
        else:
            stderr.write(
                "'%s' does not validate against '%s':\n" % (name, val_file))
            for e in validator.error_log:
                stderr.write(
                    "\tline %i, column %i: %s\n" % (e.line, e.column, e.message))


def main():
    """Main command line entry point."""
    # Logging to the console
    setup_logger_console()

    # Command-line
    (options, xml_files) = parse_cl()

    # XSD or DTD Validator?
    if options.xsd_file:
        validator = build_xml_schema(options.xsd_file)
        val_file = options.xsd_file
        val_type = "XSD"
    elif options.dtd_file:
        validator = build_dtd(options.dtd_file)
        val_file = options.dtd_file
        val_type = "DTD"
    else:
        validator = None
        val_file = None
    # Check validator
    if not val_file:
        stderr.write('No XSD or DTD file specified\n')
        exit(105)
    elif not validator:
        # Warnings via build_xml_schema of build_dtd
        stderr.write('Invalid %s file specified\n' % val_type)
        exit(105)

    # Validate XML files
    for xml_f in xml_files:
        validate_xml(xml_f, validator, val_file)

    # Read from standard input when no XML files are specified
    if not xml_files:
        validate_xml(stdin, validator, val_file)
