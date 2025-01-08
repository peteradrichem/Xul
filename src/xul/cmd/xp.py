"""Select nodes in an XML source with an XPath expression."""

import sys
from argparse import ArgumentParser

# pylint: disable=no-name-in-module
from lxml.etree import PI, Comment, XMLParser, XPathEvalError, iselement

# Import my own modules.
from .. import __version__
from ..etree import build_etree
from ..log import setup_logger_console
from ..ppxml import prettyprint
from ..xpath import build_xpath, etree_xpath, namespaces


def parse_cl():
    """Parse the command line for options, XPath expression and XML sources."""
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("-V", "--version", action="version", version="%(prog)s " + __version__)
    parser.add_argument("xpath_expr", help="XPath expression")
    parser.add_argument(
        "xml_sources",
        nargs="*",
        metavar="xml_source",
        help="XML source (file, <stdin>, http://...)",
    )
    parser.add_argument(
        "-e",
        "--exslt",
        action="store_true",
        default=False,
        dest="exslt",
        help="add EXSLT XML namespace prefixes",
    )
    parser.add_argument(
        "-d",
        "--default-prefix",
        action="store",
        default="d",
        dest="default_ns_prefix",
        help="set the prefix for the default namespace in XPath [default: '%(default)s']",
    )
    parser.add_argument(
        "-r",
        "--result-xpath",
        action="store_true",
        default=False,
        dest="result_xpath",
        help="print the XPath expression of the result element (or its parent)",
    )
    parser.add_argument(
        "-p",
        "--pretty-element",
        action="store_true",
        default=False,
        dest="pretty_element",
        help="pretty print the result element",
    )
    parser.add_argument(
        "-m",
        "--method",
        action="store_true",
        default=False,
        dest="lxml_method",
        help="use ElementTree.xpath method instead of XPath class",
    )
    file_group = parser.add_mutually_exclusive_group(required=False)
    file_group.add_argument(
        "-f",
        "-l",
        "--files-with-hits",
        action="store_true",
        default=False,
        dest="files_with_hits",
        help="only the names of files with a non-false and non-NaN result "
        + "are written to standard output",
    )
    file_group.add_argument(
        "-F",
        "-L",
        "--files-without-hits",
        action="store_true",
        default=False,
        dest="files_without_hits",
        help="only the names of files with a false or NaN result, "
        + "or without any results are written to standard output",
    )
    parser.add_argument(
        "-q",
        "--quiet",
        action="store_false",
        default=True,
        dest="verbose",
        help="don't print the XML namespace list",
    )

    return parser.parse_args()


def xpath_class(el_tree, xpath_exp, ns_map):
    """XPath with lxml.etree.XPath class."""
    if xpath_obj := build_xpath(xpath_exp, ns_map):
        return etree_xpath(el_tree, xpath_obj)
    return None


def eltree_xpath(el_tree, xpath_exp, ns_map):
    """XPath with lxml.etree.ElementTree.xpath method."""
    try:
        return el_tree.xpath(xpath_exp, namespaces=ns_map)
    except XPathEvalError as e:
        sys.stderr.write(f"{e}: {xpath_exp}\n")
        return None
    # EXSLT function call errors (re:test positional arguments).
    except TypeError as e:
        sys.stderr.write(f"Type error {e}: {xpath_exp}\n")
        return None


def xp_prepare(args):
    """Return XPath function and XML parser.

    args -- Command-line arguments
    """
    # ElementTree.xpath method or XPath class (default).
    if args.lxml_method:
        xpath_fn = eltree_xpath
    else:
        xpath_fn = xpath_class

    # Initialise XML parser.
    if args.pretty_element:
        # Pretty print preparation (removes white space text nodes!).
        xml_parser = XMLParser(remove_blank_text=True)
    else:
        xml_parser = XMLParser()

    return xpath_fn, xml_parser


def print_xmlns(ns_map, root):
    """Print XML namespaces."""
    if None in root.nsmap:
        print(f"Default XML namespace URI: {root.nsmap[None]}")
    if ns_map:
        # Print all XML namespaces -- prefix: namespace URI.
        print("XML namespaces:")
        for key in ns_map:
            print(f"{key:>9}: {ns_map[key]}")


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
            elem_str = f"<{node.tag}>"
        return elem_str

    # node.tag is lxml.etree.PI (is lxml.etree.ProcessingInstruction).
    if node.tag is PI:
        # Processing instruction node - node.target -- node.tag(): <? ?>
        return f"{node.tag(node.target)} value: '{node.text}'"

    # node.tag is lxml.etree.Comment.
    if node.tag is Comment:
        # Comment node - node.tag(): <!-- -->
        return node.tag(node.text)

    # node.tag: string.
    if node.text:
        if node.text.isspace():
            return f"<{node.tag}> contains whitespace"
        if not isinstance(node.text, str):
            # Python 2 Unicode naar Bytestring.
            return f"<{node.tag}> contains {node.text.encode('utf-8')}"
        # node.text is a Python string.
        return f"<{node.tag}> contains whitespace"
    return f"<{node.tag}> is empty"


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
            print(f"XPath {xpath_exp} (line {node.sourceline}):")
        else:
            print(f"line {node.sourceline}:")
        prettyprint(node, xml_declaration=False)
    else:
        if xpath_exp:
            print(f"XPath {xpath_exp} (line {node.sourceline}):\n   {element_repr(node)}")
        else:
            print(f"line {node.sourceline:<4d}: {element_repr(node)}")


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
        smart_repr = f"@{smart_string.attrname} = '{smart_string}'"
    # TEXT node -- text() -- .is_text
    elif smart_string.is_text:
        parent_rel = "in"
        # Python str.isspace()
        if smart_string.isspace():
            smart_repr = "whitespace"
        else:
            smart_repr = f"'{smart_string}'"
    # TAIL node -- text() -- .is_tail
    elif smart_string.is_tail:
        parent_rel = "after"
        if smart_string.isspace():
            smart_repr = "tail whitespace"
        else:
            smart_repr = f"tail '{smart_string}'"

    return (smart_repr, parent_rel)


def print_smart_string(smart_string, el_tree, args):
    """Print lxml 'smart' string with parent element tag.

    smart_string -- XPath string result that provides a getparent() method:
     * string: lxml.etree._ElementStringResult
     * Unicode: lxml.etree._ElementUnicodeResult
    el_tree -- ElementTree (lxml.etree._ElementTree)
    args -- Command-line arguments
    """
    # Parent element.
    par_el = smart_string.getparent()
    # string() and concat() results do not have an origin.
    if par_el is None:
        print(f"XPath string: '{smart_string}'")
        return
    # Parent is an lxml.etree._Element instance.
    par_el_str = element_repr(par_el, content=False)

    # Print 'smart' string.
    smart_repr, parent_rel = smart_with_parent(smart_string)
    if smart_repr:
        if args.result_xpath:
            # Print the absolute XPath expression of the parent element.
            print(
                f"line {par_el.sourceline}, parent XPath {el_tree.getpath(par_el)}\n"
                f"   {smart_repr} {parent_rel} {par_el_str}"
            )
        else:
            print(f"line {par_el.sourceline:<4d}: {smart_repr} {parent_rel} {par_el_str}")
    else:
        sys.stderr.write("Unable to print smart string\n")
        print_elem(par_el, pretty=args.pretty_element)


def print_result_list(result_list, el_tree, args):
    """Print all nodes from the list of XPath results.

    result_list -- XPath result list
    el_tree -- ElementTree (lxml.etree._ElementTree)
    args -- Command-line arguments
    """
    # All nodes -- //node()
    for node in result_list:
        if iselement(node):
            if args.result_xpath:
                print_elem(node, pretty=args.pretty_element, xpath_exp=el_tree.getpath(node))
            else:
                print_elem(node, pretty=args.pretty_element)

        # Smart string -- .getparent() | attribute, entity, text (atomic value).
        elif hasattr(node, "getparent"):
            print_smart_string(node, el_tree, args)

        # Namespaces -- namespace::
        elif isinstance(node, tuple):
            prefix, uri = node
            # No line number.
            print(f"prefix: {str(prefix):<8} URI: {uri}")

        # ?
        else:
            print("**DEBUG fallback**")
            print(type(node))
            print(node)


def print_result_header(source_name, xp_result):
    """Print header with XPath result summary."""
    # Result count.
    if isinstance(xp_result, list):
        list_result = xp_result
        xp_r_len = len(list_result)
    else:
        # String, number, boolean.
        list_result = [xp_result]
        xp_r_len = 1

    # XPath result summary.
    print(f"{source_name}:", end=" ")
    if xp_r_len == 0:
        print("no results.")
    elif xp_r_len == 1:
        if isinstance(list_result[0], tuple):
            print("1 XML namespace result.")
        else:
            print("1 result.")
    else:
        if isinstance(list_result[0], tuple):
            print(f"{xp_r_len} XML namespace results.")
        else:
            print(f"{xp_r_len} results.")


def print_xp_result(xp_result, el_tree, ns_map, args):
    """Print XPath results.

    xp_result -- XPath result
    el_tree -- ElementTree (lxml.etree._ElementTree)
    ns_map -- XML namespaces (xmlns) 'prefix: URI' dict
    args -- Command-line arguments

    Prints:
     * XML namespaces (if there are any)
     * XPath result(s)

    XPath return values:
        https://lxml.de/xpathxslt.html#xpath-return-values
    """
    if args.verbose:
        print_xmlns(ns_map, el_tree.getroot())

    # STRING - string (basestring) - smart string | Namespace URI.
    try:
        basestring
    except NameError:
        # Python 3 -- pylint: disable=redefined-builtin
        basestring = (str, bytes)
    # 'lxml.etree._ElementStringResult'
    if isinstance(xp_result, basestring):
        print_smart_string(xp_result, el_tree, args)

    # LIST - list - node-set.
    elif isinstance(xp_result, list):
        try:
            # List can be empty.
            print_result_list(xp_result, el_tree, args)
        except BrokenPipeError:
            sys.stderr.close()

    # FLOAT - float.
    elif hasattr(xp_result, "is_integer"):
        # pylint: disable=comparison-with-itself ## NaN elif.
        if xp_result.is_integer():
            # count() => integer
            print(f"XPath number: {int(xp_result)}")
        # float('nan') != float('nan') -- IEEE 754.
        elif xp_result != xp_result:
            print("XPath result: NaN (not a number)")
        # float.
        else:
            print(f"XPath number: {xp_result}")

    # BOOLEAN - bool - boolean.
    elif isinstance(xp_result, bool):
        print(f"XPath test: {xp_result}")

    else:
        print(f"Unknown XPath result: {xp_result}")


def xpath_on_xml(xml_source, parser, xpath_fn, args):
    """Apply XPath expression to XML source.

    xml_source -- XML file, file-like object or URL
    parser -- XML parser (lxml.etree.XMLParser)
    xpath_fn -- ElementTree.xpath method or XPath class
    args -- Command-line arguments
    """
    # ElementTree (lxml.etree._ElementTree).
    el_tree = build_etree(xml_source, parser=parser, lenient=False)
    if el_tree is None:
        return False

    # XML namespaces.
    ns_map = namespaces(el_tree, args.exslt, args.default_ns_prefix)
    # XPath expression on ElementTree.
    xp_result = xpath_fn(el_tree, args.xpath_expr, ns_map)
    if xp_result is None:
        return False

    # Printable name for sys.stdin.
    if xml_source in ("-", sys.stdin):
        source_name = sys.stdin.name
    else:
        source_name = xml_source

    # XML sources names (--files-with-results/--files-without-results).
    if args.files_with_hits or args.files_without_hits:
        # pylint: disable=comparison-with-itself
        # NaN check: float('nan') != float('nan').
        if xp_result != xp_result:
            if args.files_without_hits:
                print(source_name)
        elif args.files_with_hits and xp_result:
            print(source_name)
        # False is a possible value for xp_result (XPath test).
        elif args.files_without_hits and not xp_result:
            print(source_name)
        return True

    # Result header.
    print_result_header(source_name, xp_result)
    # XPath results.
    print_xp_result(xp_result, el_tree, ns_map, args)
    return True


def main():
    """Entry point for command line script xp."""
    # Logging to the console.
    setup_logger_console()

    # Command line.
    args = parse_cl()

    # XPath expression.
    if isinstance(args.xpath_expr, bytes):
        # Python 2 Bytestring to Unicode.
        args.xpath_expr = args.xpath_expr.decode("utf-8")
    if not build_xpath(args.xpath_expr):
        sys.exit(60)

    # XPath function and XML parser.
    (xpath_fn, xml_parser) = xp_prepare(args)

    # Use XPath on XML sources.
    extra_new_line = False
    for xml_s in args.xml_sources:
        if extra_new_line:
            print()
        elif not (args.files_with_hits or args.files_without_hits):
            extra_new_line = True
        xpath_on_xml(xml_s, xml_parser, xpath_fn, args)

    if not args.xml_sources:
        # Read from a pipe when no XML source is specified.
        if not sys.stdin.isatty():
            xpath_on_xml(sys.stdin, xml_parser, xpath_fn, args)
        else:
            sys.stderr.write("Error: no XML source specified\n")
            sys.exit(70)
