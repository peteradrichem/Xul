#!/usr/local/bin/python -t
# coding=utf-8

""" Pretty print XML files """


# Import standaard Python modules
from optparse import OptionParser
from sys import stdout, stderr
#
# Import XMLParser van lxml.etree
from lxml.etree import XMLParser
#
# Import TAB modules
from tab import setup_logger_console
from tab.xml import build_xml_tree


# Versie
__version_info__ = ('0', '9', '0')
__version__ = '.'.join(__version_info__)

description = "Pretty print XML files"
epilog = "Documentation: http://docu.npoict.nl/applicatiebeheer/documentatie/xml_scripts"

def parse_cl():
    """ Lees de command-line options uit.
        Geef opties en bestanden lijst terug
    """
    usage = """\t%prog xml_file_1 ... xml_file_n"""
    cl_parser = OptionParser(
        usage=usage, description=description,
        epilog=epilog, version="%prog " + __version__)

    # Parse script's command line
    return cl_parser.parse_args()


# Logging op het console
setup_logger_console()

# Command-line parsen: XML files
(options, xml_files) = parse_cl()

# XML bestand meegegeven?
if not xml_files:
    stderr.write("No XML file(s) to operate on\n")
    exit(0)

# XML parser t.b.v pretty printing (remove_blank_text) initialiseren
#   http://lxml.de/FAQ.html#parsing-and-serialisation
parser = XMLParser(remove_blank_text=True)

# Loop de XML files af
for xml_f in xml_files:
    # Opm: build_xml_tree rapporteert XML fouten in xml_f
    xml_tree = build_xml_tree(xml_f, parser=parser)
    if xml_tree:
        try:
            xml_tree.write(
                stdout, encoding='UTF-8',
                xml_declaration=True, pretty_print=True)
            # Voorkom "close failed in file object destructor:" meldingen
            # bij meerdere XML bestanden en 'Broken pipe'
            stdout.flush()
        # 'IOError: [Errno 32] Broken pipe' afvangen
        except IOError as e:
            if e.errno != 32:
                stderr.write("IOError: %s [%s]\n" % (e.strerror, e.errno))
