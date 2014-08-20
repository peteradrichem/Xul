#!/usr/local/bin/python -t
# coding=utf-8
# vim: set encoding=utf-8 :

""" XPath utility """


# Import standaard Python modules
from optparse import OptionParser
from sys import stderr
#
# Import etree.tostring van lxml
#from lxml.etree import tostring
from lxml.etree import XPathEvalError, iselement
#
# Import TAB modules
from tab import setup_logger_console
from tab.xml import build_xml_tree, build_xpath, etree_xpath


# Versie
__version_info__ = ('2', '0', '0')
__version__ = '.'.join(__version_info__)

description = "Use XPath expression to select nodes in XML file(s)."
epilog = "Documentation: http://docu.npoict.nl/applicatiebeheer/documentatie/xml_scripts"


def parse_cl():
    """ Lees de command-line options van het XPath script uit.
        Geef opties en bestanden lijst terug
        - options.xpath_exp: XPath expression
        - options.lxml_method: lxml ElementTree.xpath method i.p.v. XPath class?
        - args: files list
    """
    usage = "%prog -p xpath xml_file_1 ... xml_file_n"
    parser = OptionParser(usage=usage, description=description,
        epilog=epilog, version="%prog " + __version__)
    parser.add_option("-x", "--xpath",
        action="store", type="string", dest="xpath_exp",
        help="XPath expression")
    parser.add_option("-m", "--method",
        action="store_true", default=False, dest="lxml_method",
        help="use ElementTree.xpath method instead of XPath class")

    # Parse script's command line
    return parser.parse_args()


def print_el(node):
    """ Print (UTF-8) het element / de node:
        - comment node -- comment()
        - element node -- /path/el, //*
        - PI: processing instruction -- //processing-instruction()
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
    elif node.text and node.text.isdigit():
        # Python str.isdigit()
        print "%d:\t%s = %s" % (node.sourceline, node.tag, node.text)
    elif node.text and not node.text.isspace():
        s = node.text.encode('UTF-8', 'ignore')
        print "%d:\t%s = '%s'" % (node.sourceline, node.tag, s)
        #print "%d:\t%s = '%s'" % (node.sourceline, node.tag,
                #tostring(node, encoding='UTF-8', method="text", with_tail=False))
    elif node.text:
        print "%d:\t%s = whitespace" % (node.sourceline, node.tag)
    else:
        print "%d:\t%s = empty" % (node.sourceline, node.tag)


def print_smart_string(smart_string):
    """ Print (UTF-8) de 'smart' string in relatie met zijn parent
        - smart_string: `string' met getparent method
            string: lxml.etree._ElementStringResult
            Unicode: lxml.etree._ElementUnicodeResult

        http://lxml.de/xpathxslt.html#xpath-return-values
    """
    # Wat is het parent element?
    par_el = smart_string.getparent()
    # None komt voor bij string() en concat()
    if par_el is None:
        print "XPath string: '%s'" % smart_string
        return
    # comment: tag is een method (lxml.etree._Comment)
    if not isinstance(par_el.tag, basestring):
        par_el_str = "comment"
    # tag is een string (lxml.etree._Element)
    else:
        par_el_str = "<%s/>" % par_el.tag

    # ATTRIBUTE node -- @ -- .is_attribute
    if smart_string.is_attribute:
        print "%d:\t@%s = '%s' in %s" % (par_el.sourceline, smart_string.attrname,
                smart_string, par_el_str)
    # Python str.isdigit()
    elif smart_string.isdigit():
        print "%d:\t%s in %s" % (par_el.sourceline, smart_string, par_el_str)
    # TEXT node -- text() -- .is_text
    elif smart_string.is_text:
        if smart_string.isspace():
            print "%d:\twhitespace in %s" % (par_el.sourceline, par_el_str)
        else:
            text_node = smart_string.encode('UTF-8', 'ignore')
            print "%d:\t'%s' in %s" % (par_el.sourceline, text_node, par_el_str)
    # TAIL node -- text() -- .is_tail
    elif smart_string.is_tail:
        if smart_string.isspace():
            print "%d:\ttail whitespace after %s" % (par_el.sourceline, par_el_str)
        else:
            tail_node = smart_string.encode('UTF-8', 'ignore')
            print "%d:\ttail '%s' after %s" % (par_el.sourceline, tail_node, par_el_str)
    else:
        print "**smart string DEBUG fallback**"
        print_el(par_el)


def print_result_list(result_list):
    """ Print de nodes uit de XPath result list
        Aanname: terminal kan character encoding UTF-8 aan
    """
    # Alle nodes -- //node()
    for item in result_list:
        # Is de resultaat node (item) een element? (item.tag)
        #   element, comment, processing instruction
        if iselement(item):
            print_el(item)
        # Of een attribute, namespace, entity, text (atomic value)

        # Smart string -- .getparent()
        elif hasattr(item, "getparent"):
            print_smart_string(item)

        # Namespaces -- namespace::
        elif isinstance(item, tuple):
            # Geen regel nummer
            print "\tprefix: %s,\tURI: %s" % item

        else:
            # ?
            print "**DEBUG fallback**"
            print type(item)
            print item


def xml_namespaces(xml_dom):
    """ Geef root namespaces in XML DOM (ElementTree) terug """
    root = xml_dom.getroot()
    ns_map = {'re': "http://exslt.org/regular-expressions"}
    # Zijn er XML namespace (xmlns) in het root element gedefinieerd?
    if root.nsmap:
        print "root:\t%s" % root.tag
        for key in root.nsmap:
            if key:
                ns_map[key] = root.nsmap[key]
            else:
                # default (None) namespace: root.nsmap.get(root.prefix)
                # prefix t.b.v XPath: 'r'
                ns_map['r'] = root.nsmap[key]
    # Toon de XML namespaces
    print "XML namespaces:"
    for key in ns_map:
        print "\t%s: %s" % (key, ns_map[key])
    return ns_map


# Logging op het console
setup_logger_console()

# Command-line parsen: XPath expression & XML file(s)
(options, xml_files) = parse_cl()

# XPath expression
if options.xpath_exp:
    if build_xpath(options.xpath_exp):
        print "XPath: %s" % options.xpath_exp
    else:
        exit(60)
else:
    stderr.write('No XPath expression specified\n')
    exit(50)

# Zijn er XML bestand(en) meegegeven?
if not xml_files:
    stderr.write("No XML file(s) to use XPath on\n")
    exit(0)

# lxml.ElementTree.xpath method gebruiken?
if options.lxml_method:
    def xpath_dom(xml_dom):
        """ Gebruik de lxml.etree.ElementTree.xpath method """
        try:
            result = xml_dom.xpath(options.xpath_exp,
                    namespaces=xml_namespaces(xml_dom))
        except XPathEvalError as e:
            stderr.write("XPath '%s' evaluation error: %s\n" %
                    (options.xpath_exp, e))
            return None
        # Als EXSLT functie met onjuist aantal argumenten wordt aangeroepen
        except TypeError as e:
            stderr.write("XPath '%s' type error: %s\n" % (options.xpath_exp, e))
            return None
        else:
            return result
# Default is lxml.etree.XPath class
else:
    def xpath_dom(xml_dom):
        """ Gebruik de lxml.etree.XPath class """
        # Welke XML namespace (xmlns) prefixes zijn er gedefinieerd?
        ns_map = xml_namespaces(xml_dom)
        xpath_obj = build_xpath(options.xpath_exp, ns_map)
        if not xpath_obj:
            return None
        else:
            return etree_xpath(xml_dom, xpath_obj)


## Loop de XML bestanden af
for xml_f in xml_files:
    print "\nFile: %s" % xml_f
    # Bouw XML DOM (Document Object Model)
    xml_dom = build_xml_tree(xml_f, lenient=False)
    if xml_dom is None:
        continue
    # Pas XPath toe op XML DOM
    xp_result = xpath_dom(xml_dom)
    if xp_result is None:
        stderr.write("XPath failed on %s\n" % xml_f)
        continue

    ## XPath return values
    #   http://lxml.de/xpathxslt.html#xpath-return-values
    #
    # STRING - string (basestring) - smart string
    #   "string(/voorspellingen/@startdatum)"
    # Namespace URI
    #   "namespace-uri(*)"
    if isinstance(xp_result, basestring):
        print_smart_string(xp_result)
    # LIST - list - node-set
    #   Lijst met elementen of text of attributen
    elif isinstance(xp_result, list):
        # Resultaat header
        xp_r_len = len(xp_result)
        if xp_r_len == 0:
            print "no result (empy list)"
        elif xp_r_len == 1:
            if isinstance(xp_result[0], tuple):
                print "Namespace result:"
            else:
                print "result on line",
        else:
            if isinstance(xp_result[0], tuple):
                print "%d namespace results:" % xp_r_len
            else:
                print "%d results on lines:" % xp_r_len
        try:
            print_result_list(xp_result)
        except IOError as e:
            # 'IOError: [Errno 32] Broken pipe' afvangen
            if e.errno != 32:
                stderr.write("IOError: %s [%s]\n" % (e.strerror, e.errno))
    # FLOAT - float
    # "number(/html/nummer)"    "count(/nebo_xml)"
    # Opm: nan == NaN == not a number
    elif hasattr(xp_result, "is_integer"):
        # Python float.is_integer()
        if xp_result.is_integer():
            print "XPath number: %i" % xp_result
        else:
            # float
            print "XPath number: %s" % xp_result
    # BOOLEAN - bool - boolean
    # true(), false(), not()
    # "count(/nebo_xml) = 1"
    elif isinstance(xp_result, bool):
        print "XPath test: %s" % xp_result
    else:
        print "Unknown XPath result: %s" % xp_result
