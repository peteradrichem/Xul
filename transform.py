#!/usr/local/bin/python -t
# coding=utf-8
# vim: set fileencoding=utf-8 :

""" XSLT tooltje """


# Import standaard Python modules
from optparse import OptionParser
from sys import stdout, stderr
#
# Import NPO ICT TAB modules
from tab.log import init_console_logging
from tab.xml.etree import build_xsl_transform, xml_transformer


# Versie
__version_info__ = ('1', '7', '0')
__version__ = '.'.join(__version_info__)

description = "Transform XML file(s) with XSLT file"
epilog = "Documentation: http://docu.npoict.nl/applicatiebeheer/documentatie/xml_scripts"

def parse_cli():
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
    (options, args) = parser.parse_args()

    return options.xslt_file, args


# Logging op het console
init_console_logging('info')

# CLI parsen: XSLT & XML file(s)
xslt_file, xml_files = parse_cli()

# XSLT file
if xslt_file:
    transformer = build_xsl_transform(xslt_file)
else:
    stderr.write('No XSLT file specified\n')
    exit(105)
# XSLT transformer OK?
if not transformer:
    stderr.write('Invalid XSLT file specified\n')
    exit(105)
# XML bestand meegegeven?
if not xml_files:
    stderr.write("Valid XSLT file '%s' (no XML file to operate on)\n" % xslt_file)
    exit(0)

# Loop de XML files af
for xml_f in xml_files:
    result = xml_transformer(xml_f, transformer)
    if result:
        try:
            # UTF-8 en pretty print
            #   http://docs.python.org/library/xml.etree.elementtree.html#xml.etree.ElementTree.ElementTree.write
            result.write(stdout, encoding='UTF-8',
                    xml_declaration=True, pretty_print=True)
        # Vang AssertionError af
        except AssertionError as inst:
            stderr.write("Trouble with XSL transformation of %s\n" % xml_f)
            stderr.write("Cannot print XSLT result as XML: %s\n" % inst)
            print result
        except IOError as inst:
            (err_code, err_mesg) = inst.args
            # [Errno 32] Broken pipe afvangen
            if err_code == 32:
                pass
            else:
                stderr.write("%s\n" % err_mesg)
