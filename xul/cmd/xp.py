# -*- coding: utf-8 -*-

"""Select nodes in an XML source with an XPath expression."""


from __future__ import print_function

# Standard Python.
from argparse import ArgumentParser
import sys
#
# pylint: disable=no-name-in-module
# lxml ElementTree <https://lxml.de/>
from lxml.etree import XPathEvalError, XMLParser
from lxml.etree import iselement, PI, Comment

# Import my own modules.
from .. import __version__
from ..log import setup_logger_console
from ..dom import build_etree
from ..xpath import build_xpath, etree_xpath, dom_namespaces
from ..ppxml import prettyprint


def parse_cl():
    """Parse the command line for options, XPath expression and XML sources."""
    parser = ArgumentParser(
        description=__doc__)
    parser.add_argument(
        "-V", "--version", action="version",
        version="%(prog)s " + __version__)
    parser.add_argument("xpath_expr", help="XPath expression")
    parser.add_argument(
        "xml_sources", nargs='*',
        metavar='xml_source', help="XML source (file, <stdin>, http://...)")
    parser.add_argument(
        "-e", "--exslt",
        action="store_true", default=False, dest="exslt",
        help="add EXSLT XML namespace prefixes")
    parser.add_argument(
        "-d", "--default-prefix",
        action="store", default="d", dest="default_ns_prefix",
        help="set the prefix for the default namespace in XPath [default: '%(default)s']")
    parser.add_argument(
        "-r", "--result-xpath",
        action="store_true", default=False, dest="result_xpath",
        help="print the XPath expression of the result element (or its parent)")
    parser.add_argument(
        "-p", "--pretty-element",
        action="store_true", default=False, dest="pretty_element",
        help="pretty print the result element")
    parser.add_argument(
        "-m", "--method",
        action="store_true", default=False, dest="lxml_method",
        help="use ElementTree.xpath method instead of XPath class")

    return parser.parse_args()


def xp_prepare(args):
    """Return DOM XPath function and XML parser.

    args -- Command-line arguments
    """
    # ElementTree.xpath method or XPath class (default).
    if args.lxml_method:
        dom_xpath = et_dom_xpath
    else:
        dom_xpath = class_dom_xpath

    # Initialise XML parser.
    if args.pretty_element:
        # Pretty print preparation (removes whitespace nodes!).
        xml_parser = XMLParser(remove_blank_text=True)
    else:
        xml_parser = XMLParser()

    return dom_xpath, xml_parser


def class_dom_xpath(xml_dom, xpath_exp, ns_map):
    """XPath with lxml.etree.XPath class."""
    xpath_obj = build_xpath(xpath_exp, ns_map)
    if not xpath_obj:
        return None
    return etree_xpath(xml_dom, xpath_obj)


def et_dom_xpath(xml_dom, xpath_exp, ns_map):
    """XPath with lxml.etree.ElementTree.xpath method."""
    try:
        xp_result = xml_dom.xpath(xpath_exp, namespaces=ns_map)
    except XPathEvalError as e:
        sys.stderr.write(
            "XPath '%s' evaluation error: %s\n" % (xpath_exp, e))
        return None
    # EXSLT function call errors (re:test positional arguments).
    except TypeError as e:
        sys.stderr.write("XPath '%s' type error: %s\n" % (xpath_exp, e))
        return None
    else:
        return xp_result


def print_xmlns(ns_map, root):
    """Print XML namespaces."""
    if None in root.nsmap:
        print("Default XML namespace URI: %s" % root.nsmap[None])
    if ns_map:
        # Print all XML namespaces -- prefix: namespace URI.
        print("XML namespaces:")
        for key in ns_map:
            print("%8s: %s" % (key, ns_map[key]))


def element_repr(node, content=True):
    """Return element representation (UTF-8 Unicode).

    node -- lxml.etree._Element instance -- iselement(node)

    Node types:
     * element node -- /path/el, //*
     * comment node -- comment()
     * processing instruction node -- processing-instruction()
    """
    if not content:
        # Return lxml.etree._Element representation without content.
        if node.tag is PI:
            elem_str = node.tag(node.target)
        elif node.tag is Comment:
            elem_str = node.tag(" comment ")
        else:
            elem_str = "<%s>" % node.tag
        return elem_str

    # node.tag is lxml.etree.PI (is lxml.etree.ProcessingInstruction).
    if node.tag is PI:
        # Processing instruction node - node.target -- node.tag(): <? ?>
        return "%s value: '%s'" % (node.tag(node.target), node.text)

    # node.tag is lxml.etree.Comment.
    if node.tag is Comment:
        # Comment node - node.tag(): <!-- -->
        return node.tag(node.text)

    # node.tag: string.
    if node.text:
        if node.text.isspace():
            elem_str = "<%s> contains whitespace" % node.tag
        elif not isinstance(node.text, str):
            # Python 2 Unicode naar Bytestring.
            elem_str = "<%s> contains '%s'" % (node.tag, node.text.encode("utf-8"))
        else:
            # node.text is a Python string.
            elem_str = "<%s> contains '%s'" % (node.tag, node.text)
        return elem_str
    return "<%s> is empty" % node.tag


def print_elem(node, pretty=False, xpath_exp=None):
    """Print element (UTF-8 Unicode).

    node -- lxml.etree._Element instance.
            element, comment or processing instruction node; see element_repr()
    pretty -- True: use prettyprint() to print an element.
              False: use element_repr().
    xpath_exp -- optional XPath expression
    """
    if pretty:
        if xpath_exp:
            print("XPath %s (line %d):" % (xpath_exp, node.sourceline))
        else:
            print("line %d:" % node.sourceline)
        prettyprint(node, xml_declaration=False)
    else:
        if xpath_exp:
            print("XPath %s (line %d):" % (xpath_exp, node.sourceline))
            print("   %s" % element_repr(node))
        else:
            print("line %4d:   %s" % (node.sourceline, element_repr(node)))


def smart_with_parent(smart_string):
    """Return lxml 'smart' string representation (UTF-8) with parent relation.

    lxml 'smart' string is a text node (atomic value) or an attribute node:
     * text node (tail, entity): contains text; never empty
     * attribute node: contains the value of the attribute
    """
    smart_repr = None
    parent_rel = None

    # ATTRIBUTE node -- @ -- .is_attribute
    if smart_string.is_attribute:
        parent_rel = "of"
        smart_repr = "@%s = '%s'" % (smart_string.attrname, smart_string)
    # TEXT node -- text() -- .is_text
    elif smart_string.is_text:
        parent_rel = "in"
        # Python str.isspace()
        if smart_string.isspace():
            smart_repr = "whitespace"
        else:
            smart_repr = "'%s'" % smart_string
    # TAIL node -- text() -- .is_tail
    elif smart_string.is_tail:
        parent_rel = "after"
        if smart_string.isspace():
            smart_repr = "tail whitespace"
        else:
            smart_repr = "tail '%s'" % smart_string

    return (smart_repr, parent_rel)


def print_smart_string(smart_string, xml_dom, args):
    """Print lxml 'smart' string with parent element tag.

    smart_string -- XPath string result that provides a getparent() method:
     * string: lxml.etree._ElementStringResult
     * Unicode: lxml.etree._ElementUnicodeResult
    xml_dom -- XML DOM (ElementTree)
    args -- Command-line arguments
    """
    # Parent element.
    par_el = smart_string.getparent()
    # string() and concat() results do not have an origin.
    if par_el is None:
        print("XPath string: '%s'" % smart_string)
        return
    # Parent is an lxml.etree._Element instance.
    par_el_str = element_repr(par_el, content=False)

    # Print 'smart' string.
    smart_repr, parent_rel = smart_with_parent(smart_string)
    if smart_repr:
        if args.result_xpath:
            # Print the absolute XPath expression of the parent element.
            print("line %d, parent XPath %s" % (
                par_el.sourceline, xml_dom.getpath(par_el)))
            print("   %s %s %s" % (smart_repr, parent_rel, par_el_str))
        else:
            print("line %4d:   %s %s %s" % (
                par_el.sourceline, smart_repr, parent_rel, par_el_str))
    else:
        print("**smart string DEBUG fallback**")
        print_elem(par_el, pretty=args.pretty_element)


def print_result_list(result_list, xml_dom, args):
    """Print all nodes from the list of XPath results.

    result_list -- XPath result list
    xml_dom -- XML DOM (ElementTree)
    args -- Command-line arguments
    """
    if args.pretty_element:
        print()
    # All nodes -- //node()
    for node in result_list:
        if iselement(node):
            if args.result_xpath:
                print_elem(
                    node,
                    pretty=args.pretty_element,
                    xpath_exp=xml_dom.getpath(node))
            else:
                print_elem(node, pretty=args.pretty_element)

        # Smart string -- .getparent() | attribute, entity, text (atomic value).
        elif hasattr(node, "getparent"):
            print_smart_string(node, xml_dom, args)

        # Namespaces -- namespace::
        elif isinstance(node, tuple):
            # No line number.
            print("prefix: %-8s URI: %s" % node)

        # ?
        else:
            print("**DEBUG fallback**")
            print(type(node))
            print(node)


def print_result_header(xp_result):
    """Print header for XPath result(s)."""
    if isinstance(xp_result, list):
        list_result = xp_result
    else:
        list_result = [xp_result]
    xp_r_len = len(list_result)
    if xp_r_len == 0:
        print("no results.")
    elif xp_r_len == 1:
        if isinstance(list_result[0], tuple):
            print("1 XML namespace result")
        else:
            print("1 result.")
    else:
        if isinstance(list_result[0], tuple):
            print("%d XML namespace results." % xp_r_len)
        else:
            print("%d results." % xp_r_len)


def print_xp_result(xp_result, xml_dom, ns_map, args):
    """Print XPath results.

    xp_result -- XPath result
    xml_dom -- XML DOM (ElementTree)
    ns_map -- XML namespaces (xmlns) 'prefix: URI' dict
    args -- Command-line arguments

    Prints:
     * result header
     * XML namespaces (if there are any)
     * XPath result(s)

    XPath return values:
        https://lxml.de/xpathxslt.html#xpath-return-values
    """
    print_result_header(xp_result)
    print_xmlns(ns_map, xml_dom.getroot())

    # STRING - string (basestring) - smart string | Namespace URI.
    try:
        basestring
    except NameError:
        # Python 3.
        basestring = (str, bytes)
    # 'lxml.etree._ElementStringResult'
    if isinstance(xp_result, basestring):
        print_smart_string(xp_result, xml_dom, args)

    # LIST - list - node-set.
    elif isinstance(xp_result, list):
        try:
            print_result_list(xp_result, xml_dom, args)
        except IOError as e:
            # Catch 'IOError: [Errno 32] Broken pipe'.
            if e.errno != 32:
                sys.stderr.write("IOError: %s [%s]\n" % (e.strerror, e.errno))

    # FLOAT - float | nan == NaN == not a number.
    elif hasattr(xp_result, "is_integer"):
        # Python float.is_integer()
        if xp_result.is_integer():
            print("XPath number: %i" % xp_result)
        else:
            print("XPath number: %s" % xp_result)

    # BOOLEAN - bool - boolean.
    elif isinstance(xp_result, bool):
        print("XPath test: %s" % xp_result)
    else:
        print("Unknown XPath result: %s" % xp_result)


def xpath_on_xml(xml_source, parser, dom_xpath, args):
    """Apply XPath expression to XML source.

    xml_source -- XML file, file-like object or URL
    parser -- XML parser (lxml.etree.XMLParser)
    dom_xpath -- ElementTree.xpath method or XPath class
    args -- Command-line arguments
    """
    # XML DOM Node Tree (ElementTree).
    xml_dom = build_etree(
        xml_source,
        parser=parser,
        lenient=False)
    if xml_dom is None:
        return False

    # XML namespaces.
    ns_map = dom_namespaces(xml_dom, args.exslt, args.default_ns_prefix)
    # Use XPath expression on XML DOM.
    xp_result = dom_xpath(xml_dom, args.xpath_expr, ns_map)
    if xp_result is None:
        return False

    if xml_source == '-' or xml_source is sys.stdin:
        print("<stdin>, XPath: %s," % args.xpath_expr, end=" ")
    else:
        print("Source: %s, XPath: %s," % (xml_source, args.xpath_expr), end=" ")
    return print_xp_result(xp_result, xml_dom, ns_map, args)


def main():
    """xp command line script entry point."""
    # Logging to the console.
    setup_logger_console()

    # Command line.
    args = parse_cl()

    # XPath expressie.
    if isinstance(args.xpath_expr, bytes):
        # Python 2 Bytestring to Unicode.
        args.xpath_expr = args.xpath_expr.decode("utf-8")
    if not build_xpath(args.xpath_expr):
        sys.exit(60)

    # DOM XPath function and XML parser.
    (dom_xpath, xml_parser) = xp_prepare(args)

    # Use XPath on XML sources.
    first = True
    for xml_s in args.xml_sources:
        if first:
            first = False
        else:
            print()
        xpath_on_xml(xml_s, xml_parser, dom_xpath, args)

    if not args.xml_sources:
        # Read from a pipe when no XML source is specified.
        if not sys.stdin.isatty():
            xpath_on_xml(sys.stdin, xml_parser, dom_xpath, args)
        else:
            sys.stderr.write("Error: no XML source specified\n")
