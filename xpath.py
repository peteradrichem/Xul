#!/usr/local/bin/python -t
# coding=utf-8
# vim: set fileencoding=utf-8 :

""" XPath tooltje """


# Import standaard Python modules
from optparse import OptionParser
from sys import stderr
#
# Import etree.tostring van lxml
#from lxml.etree import tostring
#
# Import NPO ICT TAB modules
from tab.log import init_console_logging
from tab.xml.etree import xml_xpath


# Versie
__version_info__ = ('1', '4', '2')
__version__ = '.'.join(__version_info__)

description = "Use XPath expression to select nodes in XML file(s)."
epilog = "Documentation: http://docu.npoict.nl/applicatiebeheer/documentatie/xml_scripts"

def parse_cl():
    ''' Lees de command-line options van het XPath script uit

        Resultaat tuple bevat:
        - XPath expression
        - XML file(s)
    '''

    usage = "%prog -p xpath xml_file_1 ... xml_file_n"
    parser = OptionParser(usage=usage, description=description,
        epilog=epilog, version="%prog " + __version__)
    parser.add_option("-x", "--xpath",
        action="store", type="string", dest="xpath_exp",
        help="XPath expression")

    # Parse script's command line
    return parser.parse_args()


def print_node(node):
    """ Print de node (UTF-8):
        - comment node -- comment()
        - element node -- /path/el, node()
        - PI: processing instruction -- processing-instruction()
    """
    # lxml.etree.tostring print standaard het hele element
    #   - met method="text" alleen tekst
    #   - met with_tail=False vervalt de tail; vaak end-of-line (EOL)
    #
    # PI - lxml.etree._ProcessingInstruction -- node.target & node.tag()
    #   "/processing-instruction()"
    if hasattr(node, "target"):
        s = node.text.encode('UTF-8', 'ignore')
        print "%d:\tprocessing-instruction('%s') = %s" % (node.sourceline,
                node.target, node.tag(s))
    # COMMENT - lxml.etree._Comment -- node.tag() == <!---->
    elif not isinstance(node.tag, basestring):
        s = node.text.encode('UTF-8', 'ignore')
        print "%d:\t%s" % (node.sourceline, node.tag(s))
    # ELEMENT - lxml.etree._Element -- node.tag
    elif node.text and not node.text.isspace():
        s = node.text.encode('UTF-8', 'ignore')
        print "%d:\t%s = '%s'" % (node.sourceline, node.tag, s)
        #print "%d:\t%s = '%s'" % (node.sourceline, node.tag,
                #tostring(node, encoding='UTF-8', method="text", with_tail=False))
    elif node.text:
        print "%d:\t%s = space" % (node.sourceline, node.tag)
    else:
        print "%d:\t%s = empty" % (node.sourceline, node.tag)


def print_result_list(result_list):
    """ Print de items uit de XPath result list
        Aanname: terminal kan character encoding UTF-8 aan
    """
    for item in result_list:
        # Is het resultaat een node? (comment, element, processing instruction)
        if hasattr(item, "tag"):
            print_node(item)
        # Is het resultaat een attribuut? -- @ -- attribute node
        elif hasattr(item, "is_attribute") and item.is_attribute:
            # ATTRIBUTE - lxml.etree._ElementStringResult -- .is_attribute
            el = item.getparent()
            print "%d:\t@%s = '%s'" % (el.sourceline, item.attrname, item)
        # Is het resultaat een smart string? -- text() -- text node
        elif (hasattr(item, "is_text") or hasattr(item, "is_tail")) and (
                    item.is_text or item.is_tail):
            el = item.getparent()
            # is el een comment node?
            if not isinstance(el.tag, basestring):
                el_tag = el.tag()
            else:
                el_tag = "<%s>" % el.tag
            # TEXT / TAIL - lxml.etree._ElementStringResult /
            #               lxml.etree._ElementUnicodeResult
            # "/nebo_gids_export/zender/dag/uitzending/aflevering/text()"
            #   boom structuur die als lijst print_result_list() binnen komt
            if item and not item.isspace():
                s = item.encode('UTF-8', 'ignore')
                print "%d:\t'%s'" % (el.sourceline, s)
            # spatie tekst / tail
            elif item.is_text and item.is_tail:
                print "%d:\tspace+tail text %s" % (el.sourceline, el_tag)
            elif item.is_text:
                print "%d:\tspace text %s" % (el.sourceline, el_tag)
            elif item.is_tail:
                print "%d:\tspace tail %s" % (el.sourceline, el_tag)
            else:
                print "**text node DEBUG fallback**"
                print_node(el)
        else:
            # ?
            print "**DEBUG fallback**"
            print item


# Logging op het console
init_console_logging('info', "%(message)s")

# CLI parsen: XPath expression & XML file(s)
(options, xml_files) = parse_cl()

# XPath expression
if not options.xpath_exp:
    stderr.write('No XPath expression specified\n')
    exit(50)
# XML bestand meegegeven?
if not xml_files:
    stderr.write("No XML file to use XPath '%s' on\n" % options.xpath_exp)
    exit(0)

# Loop de XML files af
for xml_f in xml_files:
    print "XML file: %s" % xml_f
    print "XPath: %s" % options.xpath_exp
    xp_result = xml_xpath(xml_f, options.xpath_exp)
    if xp_result is None:
        print "no result (error)"
    # STRING - string - lxml.etree._ElementStringResult - smart string (.is_text/.is_tail)
    # "string(/voorspellingen/@startdatum)"
    elif hasattr(xp_result, "is_text") or hasattr(xp_result, "is_tail"):
        print "XPath string: '%s'" % xp_result
    # LIST - list - node-set
    #   Lijst met elementen of text of attributen
    #elif isinstance(xp_result, list):
    elif hasattr(xp_result, "index"):
        xp_r_len = len(xp_result)
        if xp_r_len == 0:
            print "no result"
        elif xp_r_len == 1:
            print "result on line",
        else:
            print "%d results on lines:" % xp_r_len
        try:
            print_result_list(xp_result)
        except IOError as e:
            # [Errno 32] Broken pipe afvangen
            if e.errno == 32:
                stderr.write("%s\n" % e.strerror)
            else:
                stderr.write("%s\n" % e.strerror)
                exit(75)
    # FLOAT - float - .is_integer()
    # "number(/html/nummer)"    "count(/nebo_xml)"
    # Opm: nan == NaN == not a number
    elif hasattr(xp_result, "is_integer"):
        print "XPath number: %s" % xp_result
    # BOOLEAN - bool - boolean
    # true(), false(), not()
    # "count(/nebo_xml) = 1"
    elif isinstance(xp_result, bool):
        print "XPath test: %s" % xp_result
    # http://lxml.de/xpathxslt.html#xpath-return-values
    else:
        print "Unknown XPath result: %s" % xp_result
