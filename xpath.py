#!/usr/local/bin/python -t
# coding=utf-8

"""Use XPath expression to select nodes in XML file(s)."""


# Standard Python
from optparse import OptionParser
from sys import stderr, stdin
#
# pylint: disable=no-name-in-module
# lxml ElementTree <http://lxml.de/>
from lxml.etree import XPathEvalError, iselement, tostring, XMLParser, parse
#
# Xul modules
from xul.log import setup_logger_console
from xul.dom import build_etree
from xul.xpath import build_xpath, etree_xpath, dom_namespaces


__version_info__ = ('2', '1', '1')
__version__ = '.'.join(__version_info__)

def parse_cl():
    """Parse the command-line for options and XML files."""
    parser = OptionParser(
        usage="%prog [options] -x xpath xml_file_1 ... xml_file_n",
        description=__doc__,
        version="%prog " + __version__)
    parser.add_option(
        "-x", "--xpath",
        action="store", type="string", dest="xpath_exp",
        help="XML Path Language (XPath) expression")
    parser.add_option(
        "-n", "--namespace",
        action="store_true", default=False, dest="namespaces",
        help="enable XML namespace prefixes")
    parser.add_option(
        "-d", "--default-prefix",
        action="store", type="string", default="d", dest="default_ns_prefix",
        help="set the prefix for the default namespace in XPath [default: '%default']")
    parser.add_option(
        "-p", "--print-xpath",
        action="store_true", default=False, dest="print_xpath",
        help="print the absolute XPath of a result (or parent) element")
    parser.add_option(
        "-e", "--element-tree",
        action="store_true", default=False, dest="element_tree",
        help="print the XML tree of a result element")
    parser.add_option(
        "-m", "--method",
        action="store_true", default=False, dest="lxml_method",
        help="use ElementTree.xpath method instead of XPath class")

    return parser.parse_args()


def class_xpath_dom(xml_dom):
    """XPath with lxml.etree.XPath class."""
    ns_map = dom_namespaces(xml_dom, options.namespaces, options.default_ns_prefix)
    xpath_obj = build_xpath(options.xpath_exp, ns_map)
    if not xpath_obj:
        return None
    else:
        return etree_xpath(xml_dom, xpath_obj)


def et_xpath_dom(xml_dom):
    """XPath with lxml.etree.ElementTree.xpath method."""
    try:
        xp_result = xml_dom.xpath(
            options.xpath_exp,
            namespaces=dom_namespaces(
                xml_dom, options.namespaces, options.default_ns_prefix))
    except XPathEvalError as e:
        stderr.write(
            "XPath '%s' evaluation error: %s\n" % (options.xpath_exp, e))
        return None
    # TypeError bij aanroepen EXSLT functie met onjuist aantal argumenten
    except TypeError as e:
        stderr.write("XPath '%s' type error: %s\n" % (options.xpath_exp, e))
        return None
    else:
        return xp_result


def node_repr(node):
    """Return node representation (UTF-8 encoded).

       Node examples:
       - element node -- /path/el, //*
       - comment node -- comment()
       - PI: processing instruction -- //processing-instruction()
    """
    # PI - lxml.etree._ProcessingInstruction -- node.target & node.tag()
    #   "/processing-instruction()"
    if hasattr(node, "target"):
        return "processing-instruction('%s') = %s" % (
            node.target, node.tag(node.text.encode('UTF-8', 'ignore')))

    # COMMENT node - lxml.etree._Comment -- node.tag() == <!---->
    elif not isinstance(node.tag, basestring):
        return node.tag(node.text.encode('UTF-8', 'ignore'))

    # ELEMENT - lxml.etree._Element -- node.tag
    elif node.text:
        # node.text is a string; not a 'smart' string
        if node.text.isdigit():
            return "<%s> contains %s" % (node.tag, node.text)
        elif not node.text.isspace():
            return "<%s> contains '%s'" % (node.tag, node.text.encode('UTF-8', 'ignore'))
        else:
            return "<%s> contains whitespace" % node.tag
    else:
        return "<%s> is empty" % node.tag


def print_node(node):
    """Print node (UTF-8 encoded).

       Print node, using node_repr(). When options.element_tree is True
       use lxml.etree.tostring() to print the whole element tree.
    """
    if options.element_tree:
        # Ignore tail text; often end-of-line (EOL)
        node_string = "'%s'" % tostring(node, encoding='UTF-8', with_tail=False)
    else:
        node_string = node_repr(node)
    print "%d:\t%s" % (node.sourceline, node_string)


def smart_with_parent(smart_string):
    """Return lxml 'smart' string representation (UTF-8 encoded) with parent relation.

       lxml 'smart' string is a text node (atomic value) or an attribute node:
       - text node (tail, entity): contains text; never empty
       - attribute node: contains the value of the attribute

       http://lxml.de/xpathxslt.html#xpath-return-values
    """
    smart_repr = None
    parent_rel = None

    # TEXT node -- text() -- Python str.isdigit()
    if smart_string.isdigit():
        smart_repr = smart_string
        parent_rel = "in"
    # TEXT node -- text() -- .is_text
    elif smart_string.is_text:
        parent_rel = "in"
        if smart_string.isspace():
            smart_repr = "whitespace"
        else:
            smart_repr = "'%s'" % smart_string.encode('UTF-8', 'ignore')
    # TAIL node -- text() -- .is_tail
    elif smart_string.is_tail:
        parent_rel = "after"
        if smart_string.isspace():
            smart_repr = "tail whitespace"
        else:
            smart_repr = "tail '%s'" % smart_string.encode('UTF-8', 'ignore')
    # ATTRIBUTE node -- @ -- .is_attribute
    elif smart_string.is_attribute:
        parent_rel = "of"
        smart_repr = "@%s = '%s'" % (smart_string.attrname, smart_string)

    return (smart_repr, parent_rel)


def print_smart_string(smart_string, xml_dom):
    """Print lxml 'smart' string with parent element tag.

       smart_string -- XPath string result that provides a getparent() method.
          - string: lxml.etree._ElementStringResult
          - Unicode: lxml.etree._ElementUnicodeResult
       xml_dom -- XML DOM (ElementTree)
    """
    # XPath result parent element
    par_el = smart_string.getparent()
    # string() and concat() results do not have an origin
    if par_el is None:
        print "XPath string: '%s'" % smart_string
        return
    # comment: tag is a method (lxml.etree._Comment)
    if not isinstance(par_el.tag, basestring):
        par_el_str = "comment"
    # tag is a string (lxml.etree._Element)
    else:
        par_el_str = "<%s>" % par_el.tag

    smart_repr, parent_rel = smart_with_parent(smart_string)
    if smart_repr:
        print "%d:\t%s %s %s" % (par_el.sourceline, smart_repr, parent_rel, par_el_str)
    else:
        print "**smart string DEBUG fallback**"
        print_node(par_el)

    # Print parent element XPath expression
    if options.print_xpath:
        print "\tParent XPath: %s" % xml_dom.getpath(par_el)


def print_result_list(result_list, xml_dom):
    """Print all nodes from the list of XPath results."""
    # Alle nodes -- //node()
    for node in result_list:
        # Een element inclusief comment, processing instruction (node.tag)
        if iselement(node):
            print_node(node)
            # Print node XPath expression
            if options.print_xpath:
                print "\tXPath: %s" % xml_dom.getpath(node)

        # Een attribute, entity, text (atomic value)
        # Smart string -- .getparent()
        elif hasattr(node, "getparent"):
            print_smart_string(node, xml_dom)

        # Namespaces -- namespace::
        elif isinstance(node, tuple):
            # Geen regel nummer
            print "\tprefix: %s,\tURI: %s" % node

        # ?
        else:
            print "**DEBUG fallback**"
            print type(node)
            print node


def print_result_header(list_result):
    """Print header for list of XPath results."""
    xp_r_len = len(list_result)
    if xp_r_len == 0:
        print "no result (empy list)"
    elif xp_r_len == 1:
        if isinstance(list_result[0], tuple):
            print "Namespace result:"
        else:
            print "1 result on line:"
    else:
        if isinstance(list_result[0], tuple):
            print "%d namespace results:" % xp_r_len
        else:
            print "%d results on lines:" % xp_r_len


def print_xpath_result(xml_dom):
    """Print XPath results.

    XPath return values:
        http://lxml.de/xpathxslt.html#xpath-return-values
    """
    # Use XPath expression on XML DOM
    xp_result = xpath_dom(xml_dom)
    if xp_result is None:
        stderr.write("XPath failed\n")
        return

    # STRING - string (basestring) - smart string
    #   "string(/voorspellingen/@startdatum)"
    # Namespace URI
    #   "namespace-uri(*)"
    if isinstance(xp_result, basestring):
        print_smart_string(xp_result, xml_dom)

    # LIST - list - node-set
    elif isinstance(xp_result, list):
        print_result_header(xp_result)
        try:
            print_result_list(xp_result, xml_dom)
        except IOError as e:
            # 'IOError: [Errno 32] Broken pipe' afvangen
            if e.errno != 32:
                stderr.write("IOError: %s [%s]\n" % (e.strerror, e.errno))

    # FLOAT - float
    #   "number(/html/nummer)"    "count(/nebo_xml)"
    # Opm: nan == NaN == not a number
    elif hasattr(xp_result, "is_integer"):
        # Python float.is_integer()
        if xp_result.is_integer():
            print "XPath number: %i" % xp_result
        else:
            print "XPath number: %s" % xp_result

    # BOOLEAN - bool - boolean
    #   true(), false(), not(), "count(/nebo_xml) = 1"
    elif isinstance(xp_result, bool):
        print "XPath test: %s" % xp_result
    else:
        print "Unknown XPath result: %s" % xp_result


if __name__ == '__main__':
    # Logging to the console (TAB modules)
    setup_logger_console()

    # Command-line
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

    if options.lxml_method:
        # lxml.ElementTree.xpath method
        xpath_dom = et_xpath_dom
    else:
        # lxml.etree.XPath class (default)
        xpath_dom = class_xpath_dom

    # Initialise XML parser
    xml_parser = XMLParser()


    # Use XPath on XML files
    for xml_f in xml_files:
        print "\nFile: %s" % xml_f
        # Bouw XML DOM (Document Object Model) Node Tree (ElementTree)
        xml_dom_node_tree = build_etree(
            xml_f,
            parser=xml_parser,
            lenient=False)
        if xml_dom_node_tree is None:
            continue
        print_xpath_result(xml_dom_node_tree)

    # Read from standard input when no XML files are specified
    if not xml_files:
        print_xpath_result(parse(stdin, xml_parser))
