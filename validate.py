#!/usr/local/bin/python -t
# coding=utf-8
# vim: set encoding=utf-8 :

""" XSD/DTD validatie tooltje """


# Import standaard Python modules
from optparse import OptionParser
from sys import stderr
#
# Import NPO ICT TAB modules
from tab.log import setup_logger_console
from tab.xml.etree import build_xml_tree, build_xml_schema, build_dtd


# Versie
__version_info__ = ('1', '9', '0')
__version__ = '.'.join(__version_info__)

description = "Validate XML files against an XSD or DTD file"
epilog = "Documentation: http://docu.npoict.nl/applicatiebeheer/documentatie/xml_scripts"

def parse_cl():
    ''' Leest de opgegeven command-line options uit

        Resultaat tuple bevat:
        - XSD file
        - DTD file
        - XML files list
    '''
    usage = """\t%prog -x xsd_file xml_file_1 ... xml_file_n
\t%prog -d dtd_file xml_file_1 ... xml_file_n"""
    parser = OptionParser(usage=usage, description=description,
        epilog=epilog, version="%prog " + __version__)
    parser.add_option("-x", "--xsd",
        action="store", type="string", dest="xsd_file",
        help="XSD file to validate XML file(s)")
    parser.add_option("-d", "--dtd",
        action="store", type="string", dest="dtd_file",
        help="DTD file to validate XML file(s)")

    # Parse script's command line
    return parser.parse_args()


# Logging op het console
setup_logger_console()

# CLI parsen: XSD/DTD file & XML files
(options, xml_files) = parse_cl()

# XSD of DTD?
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
#
# Validator OK?
if not val_file:
    # Geen file meegegeven
    stderr.write('No XSD or DTD file specified\n')
    exit(105)
elif not validator:
    # Warnings via build_xml_schema of build_dtd
    stderr.write('Invalid %s file specified\n' % val_type)
    exit(105)
#
# XML bestand meegegeven?
if not xml_files:
    stderr.write("Valid %s file '%s' (no XML file to operate on)\n" % (val_type,
            val_file))
    exit(0)

# Loop de XML files af
for xml_f in xml_files:
    xml_tree = build_xml_tree(xml_f)
    if xml_tree:
        # Probeer de ElementTree te valideren
        if validator.validate(xml_tree):
            print "XML file '%s' validates against '%s'" % (xml_f, val_file)
        else:
            stderr.write("XML file '%s' does not validate against '%s':\n" % (xml_f,
                    val_file))
            for e in validator.error_log:
                stderr.write("\tline %i, column %i: %s\n" % (e.line, e.column, e.message))
