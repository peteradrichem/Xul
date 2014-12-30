#!/usr/local/bin/python -t
# coding=utf-8

""" Pretty print XML files """


# Import standaard Python modules
from optparse import OptionParser
from sys import stdout, stderr
#
# Import XMLParser van lxml.etree
from lxml.etree import XMLParser, tostring
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
    usage = """\t%prog [-n] xml_file_1 ... xml_file_n"""
    cl_parser = OptionParser(
        usage=usage, description=description,
        epilog=epilog, version="%prog " + __version__)
    cl_parser.add_option(
        "-n", "--no-color", action="store_false", default=True,
        dest="color", help="disable colored output")

    # Parse script's command line
    return cl_parser.parse_args()


def prettyprint(etree):
    """ Pretty print de XML etree; indien mogelijk in kleur """
    if options.color:
        lexer = get_lexer_by_name('xml', encoding='utf8')
        formatter = Terminal256Formatter(encoding='utf8')
        xml_str = tostring(
            etree, encoding='UTF-8',
            xml_declaration=True, pretty_print=True)
        print highlight(xml_str, lexer, formatter)
    else:
        etree.write(
            stdout, encoding='UTF-8',
            xml_declaration=True, pretty_print=True)


# Logging op het console
setup_logger_console()

# Command-line parsen: XML files
(options, xml_files) = parse_cl()

if options.color:
    try:
        from pygments import highlight
        from pygments.lexers import get_lexer_by_name
        from pygments.formatters.terminal256 import Terminal256Formatter
    except ImportError as inst:
        options.color = False

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
            prettyprint(xml_tree)
            # Voorkom "close failed in file object destructor:" meldingen
            # bij meerdere XML bestanden en 'Broken pipe'
            stdout.flush()
        # 'IOError: [Errno 32] Broken pipe' afvangen
        except IOError as e:
            if e.errno != 32:
                stderr.write("IOError: %s [%s]\n" % (e.strerror, e.errno))
