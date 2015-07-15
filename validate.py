#!/usr/local/bin/python -t
# coding=utf-8

"""Validate XML file(s) with an XSD or DTD file."""


# Standard Python
from optparse import OptionParser
from sys import stderr
#
# Xul modules
from xul.log import setup_logger_console
from xul.dom import build_etree, build_xml_schema, build_dtd


__version_info__ = ('2', '0', '0')
__version__ = '.'.join(__version_info__)

def parse_cl():
    """Parse the command-line for options and XML files."""
    parser = OptionParser(
        usage="""\t%prog -x xsd_file xml_file_1 ... xml_file_n
\t%prog -d dtd_file xml_file_1 ... xml_file_n""",
        description=__doc__,
        epilog="Documentation: " +
        "http://docu.npoict.nl/applicatiebeheer/documentatie/xml_scripts",
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


if __name__ == '__main__':
    # Logging to the console (TAB modules)
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
    if not xml_files:
        stderr.write("Valid %s file '%s'\n" % (val_type, val_file))
        stderr.write("No XML file(s) to operate on\n")
        exit(0)
    for xml_f in xml_files:
        # Opm: build_etree rapporteert XML fouten in xml_f
        xml_tree = build_etree(xml_f)
        if xml_tree:
            # Probeer de ElementTree te valideren
            if validator.validate(xml_tree):
                print "XML file '%s' validates against '%s'" % (xml_f, val_file)
            else:
                stderr.write(
                    "XML file '%s' does not validate against '%s':\n" %
                    (xml_f, val_file))
                for e in validator.error_log:
                    stderr.write(
                        "\tline %i, column %i: %s\n" % (e.line, e.column, e.message))
