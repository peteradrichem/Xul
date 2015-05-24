#!/usr/local/bin/python -t
# coding=utf-8

"""Pretty print XML files"""


# Standard Python
from optparse import OptionParser
from sys import stdout, stderr, stdin
#
# lxml ElementTree <http://lxml.de/>
from lxml.etree import XMLParser, tostring, parse
#
# TAB modules
from tab import setup_logger_console
from tab.xml import build_xml_tree


__version_info__ = ('1', '1', '0')
__version__ = '.'.join(__version_info__)

def parse_cl():
    """Parse the command-line for options and XML files."""
    cl_parser = OptionParser(
        usage="\t%prog [-n] xml_file_1 ... xml_file_n",
        description=__doc__,
        epilog="Documentation: " +
        "http://docu.npoict.nl/applicatiebeheer/documentatie/xml_scripts",
        version="%prog " + __version__)
    cl_parser.add_option(
        "-n", "--no-color", action="store_false", default=True,
        dest="color", help="disable colored output")

    return cl_parser.parse_args()


def prettyprint(etree):
    """Pretty print XML ElementTree in optional (Pygments) color"""
    if options.color:
        xml_str = tostring(
            etree, encoding='UTF-8',
            xml_declaration=True, pretty_print=True)
        print highlight(xml_str, lexer, formatter)
    else:
        etree.write(
            stdout, encoding='UTF-8',
            xml_declaration=True, pretty_print=True)


if __name__ == '__main__':
    # Logging to the console (TAB modules)
    setup_logger_console()

    # Command-line
    (options, xml_files) = parse_cl()

    if options.color:
        try:
            from pygments.lexers import get_lexer_by_name
            lexer = get_lexer_by_name('xml', encoding='utf-8')
            from pygments.formatters.terminal256 import Terminal256Formatter
            formatter = Terminal256Formatter(encoding='utf-8', nobold=True)
            from pygments import highlight
        except ImportError:
            options.color = False

    # Initialise XML parser and remove blank text for 'pretty_print' formatting
    #   http://lxml.de/FAQ.html#parsing-and-serialisation
    parser = XMLParser(remove_blank_text=True)

    # Pretty print XML files
    for xml_f in xml_files:
        # Opm: build_xml_tree rapporteert XML fouten in xml_f
        xml_tree = build_xml_tree(xml_f, parser=parser)
        if xml_tree:
            try:
                prettyprint(xml_tree)
                # Voorkom "close failed in file object destructor:" meldingen
                # bij meerdere XML bestanden en 'Broken pipe'
                stdout.flush()
            except IOError as e:
                # 'IOError: [Errno 32] Broken pipe' afvangen
                if e.errno != 32:
                    stderr.write("IOError: %s [%s]\n" % (e.strerror, e.errno))

    # Read from standard input when no XML files are specified
    if not xml_files:
        xml_tree = parse(stdin, parser)
        prettyprint(xml_tree)
