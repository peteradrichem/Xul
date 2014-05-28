#!/usr/local/bin/python -t
# coding=utf-8
# vim: set encoding=utf-8 :

""" XSLT tooltje """


# Import standaard Python modules
from optparse import OptionParser
from sys import stdout, stderr
#
# Import NPO ICT TAB modules
from tab.log import setup_logger_console
from tab.xml.etree import build_xsl_transform, xml_transformer


# Versie
__version_info__ = ('1', '8', '0')
__version__ = '.'.join(__version_info__)

description = "Transform XML file(s) with XSLT file"
epilog = "Documentation: http://docu.npoict.nl/applicatiebeheer/documentatie/xml_scripts"

def parse_cl():
    ''' Leest de opgegeven command-line options uit

        Resultaat tuple bevat:
        - XSLT file
        - XML files list
    '''
    usage = "%prog -x xslt_file xml_file ..."
    parser = OptionParser(usage=usage, description=description,
        epilog=epilog, version="%prog " + __version__)
    parser.add_option("-x", "--xslt",
        action="store", type="string", dest="xslt_file",
        help="XSLT file to transform XML file(s)")

    # Parse script's command line
    return parser.parse_args()


# Logging op het console
setup_logger_console()

# CLI parsen: XSLT & XML file(s)
(options, xml_files) = parse_cl()

# XSLT file
if options.xslt_file:
    transformer = build_xsl_transform(options.xslt_file)
else:
    stderr.write('No XSLT file specified\n')
    exit(105)
# XSLT transformer OK?
if not transformer:
    stderr.write('Invalid XSLT file specified\n')
    exit(105)
# XML bestand meegegeven?
if not xml_files:
    stderr.write("Valid XSLT file '%s' (no XML file to operate on)\n" % options.xslt_file)
    exit(0)

# Loop de XML files af
for xml_f in xml_files:
    result = xml_transformer(xml_f, transformer)
    if result:
        try:
            # UTF-8 en pretty print (#xml.etree.ElementTree.ElementTree.write)
            #   http://docs.python.org/2/library/xml.etree.elementtree.html
            result.write(stdout, encoding='UTF-8',
                    xml_declaration=True, pretty_print=True)
        # Vang AssertionError af
        except AssertionError as inst:
            stderr.write("Trouble with XSL transformation of %s\n" % xml_f)
            stderr.write("Cannot print XSLT result as XML: %s\n" % inst)
            print result
        except IOError as e:
            # [Errno 32] Broken pipe afvangen
            if e.errno == 32:
                pass
            else:
                stderr.write("%s\n" % e.strerror)
