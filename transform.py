#!/usr/local/bin/python -t
# coding=utf-8

"""Transform XML file(s) with an XSL file."""


# Standard Python
from optparse import OptionParser
from sys import stdout, stderr
#
# Xul modules
from xul.log import setup_logger_console
from xul.dom import build_xsl_transform, xml_transformer


__version_info__ = ('2', '0', '0')
__version__ = '.'.join(__version_info__)

def parse_cl():
    """Parse the command-line for options and XML files."""
    parser = OptionParser(
        usage="%prog -x xsl_file xml_file ...",
        description=__doc__,
        version="%prog " + __version__)
    parser.add_option(
        "-x", "--xsl",
        action="store", type="string", dest="xsl_file",
        help="XSL file to transform XML file(s)")

    return parser.parse_args()


if __name__ == '__main__':
    # Logging to the console (TAB modules)
    setup_logger_console()

    # Command-line
    (options, xml_files) = parse_cl()

    # Build an XSL Transformer (XSLT) from an XSL file
    if options.xsl_file:
        transformer = build_xsl_transform(options.xsl_file)
    else:
        stderr.write('No XSL file specified\n')
        exit(105)
    if not transformer:
        stderr.write('Invalid XSL file specified\n')
        exit(105)

    # Transform XML files with XSL
    if not xml_files:
        stderr.write("Valid XSL file '%s'\n" % options.xsl_file)
        stderr.write("But no XML file(s) to operate on\n")
        exit(0)
    for xml_f in xml_files:
        # Opm: xml_transformer rapporteert XML fouten in xml_f etc.
        result = xml_transformer(xml_f, transformer)
        if result:
            try:
                # UTF-8 en pretty print (#xml.etree.ElementTree.ElementTree.write)
                #   http://docs.python.org/2/library/xml.etree.elementtree.html
                result.write(
                    stdout, encoding='UTF-8',
                    xml_declaration=True, pretty_print=True)
                # Voorkom "close failed in file object destructor:" meldingen
                # bij meerdere XML bestanden en 'Broken pipe'
                stdout.flush()
            except AssertionError:
                # Text result instead of XML
                print result
            except IOError as e:
                # 'IOError: [Errno 32] Broken pipe'
                if e.errno != 32:
                    stderr.write("IOError: %s [%s]\n" % (e.strerror, e.errno))
