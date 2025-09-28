"""Select nodes in an XML source with an XPath expression."""

import argparse
import sys
from typing import Any, Callable, Optional, TextIO, Union

from lxml import etree

from .. import __version__
from ..etree import build_etree
from ..ppxml import prettyprint
from ..utils import config_logger, get_source_name
from ..xpath import build_xpath, etree_xpath, namespaces


def parse_cl() -> argparse.Namespace:
    """Parse the command line for options, XPath expression and XML sources."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-V", "--version", action="version", version="%(prog)s " + __version__)
    parser.add_argument("xpath_expr", help="XPath expression")
    parser.add_argument(
        "xml_sources",
        nargs="*",
        metavar="xml_source",
        help="XML source (file, <stdin>, http://...)",
    )
    file_group = parser.add_argument_group(
        title="file hit options", description="output filenames to standard output"
    )
    file_hit_group = file_group.add_mutually_exclusive_group(required=False)
    file_hit_group.add_argument(
        "-l",
        "-f",
        "--files-with-hits",
        action="store_true",
        default=False,
        dest="files_with_hits",
        help=(
            "only names of files with a result that is not false and not NaN"
            " are written to standard output"
        ),
    )
    file_hit_group.add_argument(
        "-L",
        "-F",
        "--files-without-hits",
        action="store_true",
        default=False,
        dest="files_without_hits",
        help=(
            "only names of files with a false or NaN result,"
            " or without a result, are written to standard output"
        ),
    )
    namespace_group = parser.add_argument_group(title="namespace options")
    namespace_group.add_argument(
        "-d",
        "--default-prefix",
        action="store",
        default="d",
        dest="default_ns_prefix",
        help="set the prefix for the default namespace in XPath [default: '%(default)s']",
    )
    namespace_group.add_argument(
        "-e",
        "--exslt",
        action="store_true",
        default=False,
        dest="exslt",
        help="add EXSLT XML namespaces",
    )
    namespace_group.add_argument(
        "-q",
        "--quiet",
        action="store_false",
        default=True,
        dest="verbose",
        help="don't print XML source namespaces",
    )
    output_group = parser.add_argument_group(title="element output options")
    output_type_group = output_group.add_mutually_exclusive_group(required=False)
    output_type_group.add_argument(
        "-c",
        "--count",
        action="store_true",
        default=False,
        dest="count",
        help="only print the number of selected nodes",
    )
    output_type_group.add_argument(
        "-p",
        "--pretty-element",
        action="store_true",
        default=False,
        dest="pretty_element",
        help="pretty print the result element",
    )
    output_group.add_argument(
        "-r",
        "--result-xpath",
        action="store_true",
        default=False,
        dest="result_xpath",
        help="print the XPath expression of the result element (or its parent)",
    )
    parser.add_argument(
        "-m",
        "--method",
        action="store_true",
        default=False,
        dest="lxml_method",
        help="use ElementTree.xpath method instead of XPath class",
    )

    return parser.parse_args()


def xpath_class(el_tree: etree._ElementTree, xpath_exp: str, ns_map: dict[str, str]):
    """XPath with lxml.etree.XPath class.

    :param el_tree: lxml ElementTree
    :param xpath_exp: XPath expression
    :param ns_map: XML namespace (prefix: URI) dictionary
    :return: XPath result
    """
    if xpath_obj := build_xpath(xpath_exp, ns_map):
        return etree_xpath(el_tree, xpath_obj)
    return None


def eltree_xpath(el_tree: etree._ElementTree, xpath_exp: str, ns_map: dict[str, str]):
    """XPath with lxml.etree.ElementTree.xpath method.

    :param el_tree: lxml ElementTree
    :param xpath_exp: XPath expression
    :param ns_map: XML namespace (prefix: URI) dictionary
    :return: XPath result
    """
    try:
        return el_tree.xpath(xpath_exp, namespaces=ns_map)
    except etree.XPathEvalError as e:
        sys.stderr.write(f"{e}: {xpath_exp}\n")
        return None
    # Incorrect EXSLT function call (e.g. number of positional arguments for re:test).
    except TypeError as e:
        sys.stderr.write(f"{xpath_exp} is invalid: {e}\n")
        return None


def xp_prepare(
    args: argparse.Namespace,
) -> tuple[Callable[[etree._ElementTree, str, dict[str, str]], Any], etree.XMLParser]:
    """Return XPath function and XML parser.

    :param args: command-line arguments
    """
    # ElementTree.xpath method or XPath class (default).
    if args.lxml_method:
        xpath_fn = eltree_xpath
    else:
        xpath_fn = xpath_class

    # Initialise XML parser.
    if args.pretty_element:
        # Pretty print preparation (removes white space text nodes!).
        xml_parser = etree.XMLParser(remove_blank_text=True)
    else:
        xml_parser = etree.XMLParser()

    return xpath_fn, xml_parser


def print_xmlns(ns_map: dict[str, str], root: etree._Element) -> None:
    """Print XML source namespaces (prefix: namespace URI).

    :param ns_map: XML namespace (prefix: URI) dictionary
    :param root: root (document) element
    """
    if ns_map:
        print("XML namespaces (prefix: URI):")
        for key in ns_map:
            if None in root.nsmap and ns_map[key] == root.nsmap[None]:
                print(f"{key:>9}: {ns_map[key]} (default namespace)")
            else:
                print(f"{key:>9}: {ns_map[key]}")
    elif None in root.nsmap:
        print(f"Default XML namespace URI: {root.nsmap[None]}")


def element_repr(node) -> str:
    """Return element representation with its content.

    :param node: element, comment or processing instruction node

    Node types:
    - element (lxml.etree._Element) : /path/el, //*
    - comment (lxml.etree._Comment) : comment()
    - processing instruction (lxml.etree._ProcessingInstruction) : processing-instruction()

    Use node.tag to return representation with content.
    """
    # lxml.etree.PI (lxml.etree.ProcessingInstruction).
    if node.tag is etree.PI:
        # Processing instruction node - node.target -- node.tag(): <? ?>
        return f"{node.tag(node.target)} value: '{node.text}'"

    # lxml.etree.Comment.
    if node.tag is etree.Comment:
        # Comment node - node.tag(): <!-- -->
        return node.tag(node.text)

    # string (str).
    if node.text:
        if node.text.isspace():
            return f"<{node.tag}> contains whitespace"
        return f"<{node.tag}> contains '{node.text}'"

    return f"<{node.tag}> is empty"


def parent_repr(parent) -> str:
    """Return parent element representation (without content).

    :param node: element, comment or processing instruction node; see element_repr()
    """
    if parent.tag is etree.PI:
        return parent.tag(parent.target)
    if parent.tag is etree.Comment:
        return parent.tag(" comment ")
    return f"<{parent.tag}>"


def print_elem(node, pretty: bool = False, xpath_exp: Optional[str] = None) -> None:
    """Print element (UTF-8 Unicode).

    :param node: element, comment or processing instruction node; see element_repr()
    :param pretty: pretty print node
    :param xpath_exp: also print node XPath expression
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


def smart_with_parent(smart_string: etree._ElementUnicodeResult) -> tuple[str, str]:
    """Return lxml 'smart' string representation (UTF-8) with parent relation.

    :param smart_string: XPath string result with parent element

    lxml 'smart' string is a text node (atomic value) or an attribute node:
    - text node (tail, entity): contains text; never empty
    - attribute node: contains the value of the attribute
    """
    # ATTRIBUTE node -- @ -- .is_attribute
    if smart_string.is_attribute:
        return f"@{smart_string.attrname!r} = '{smart_string}'", "of"
    # TEXT node -- text() -- .is_text
    if smart_string.is_text:
        smart_repr = "whitespace" if smart_string.isspace() else f"'{smart_string}'"
        return smart_repr, "in"
    # TAIL node -- text() -- .is_tail
    if smart_string.is_tail:
        if smart_string.isspace():
            smart_repr = "tail whitespace"
        else:
            smart_repr = f"tail '{smart_string}'"
        return smart_repr, "after"

    return "", ""


def print_smart_string(
    smart_string: etree._ElementUnicodeResult, el_tree: etree._ElementTree, args: argparse.Namespace
) -> None:
    """Print lxml 'smart' string with parent element tag.

    :param smart_string: XPath string result with parent element
    :param el_tree: lxml ElementTree to retrieve XPath path expressions
    :param args: command-line arguments
    """
    # Parent element.
    par_el = smart_string.getparent()
    # string() and concat() results do not have an origin.
    if par_el is None:
        print(f"XPath string: '{smart_string}'")
        return
    # Parent is an lxml.etree._Element instance.
    par_el_str = parent_repr(par_el)

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


def print_result_list(result_list, el_tree: etree._ElementTree, args: argparse.Namespace) -> None:
    """Print all nodes from the list of XPath results.

    :param result_list: XPath result list
    :param el_tree: lxml ElementTree to retrieve XPath path expressions
    :param args: command-line arguments
    """
    # All nodes -- //node()
    for node in result_list:
        if etree.iselement(node):
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
            if prefix is None:
                print(f"prefix: {args.default_ns_prefix:<8} URI: {uri}")
            else:
                print(f"prefix: {prefix:<8} URI: {uri}")


def build_result_list(xp_result: Any) -> list[Any]:
    """Return a list with XPath results.

    :param xp_result: XPath result
    """
    if isinstance(xp_result, list):
        # List is empty if there are no results.
        return xp_result
    # String, number, boolean.
    return [xp_result]


def print_result_header(source_name: str, xp_result: Any) -> None:
    """Print header with XPath result summary.

    :param source_name: name of the XML source
    :param xp_result: XPath result
    """
    result_list = build_result_list(xp_result)
    xp_r_len = len(result_list)

    # XPath result summary.
    print(f"{source_name}:", end=" ")
    if xp_r_len == 0:
        print("no results.")
    elif xp_r_len == 1:
        if isinstance(xp_result, tuple):
            print("1 XML namespace result.")
        else:
            print("1 result.")
    else:
        if isinstance(result_list[0], tuple):
            print(f"{xp_r_len} XML namespace results.")
        else:
            print(f"{xp_r_len} results.")


def print_xp_result(xp_result: Any, el_tree: etree._ElementTree, args: argparse.Namespace) -> None:
    """Print XPath results.

    :param xp_result: XPath result
    :param el_tree: lxml ElementTree
    :param args: command-line arguments

    Prints:
    - XML namespaces (if there are any)
    - XPath result(s)

    XPath return values:
        https://lxml.de/xpathxslt.html#xpath-return-values
    """
    # STRING - string - smart string | Namespace URI.
    if isinstance(xp_result, etree._ElementUnicodeResult):
        print_smart_string(xp_result, el_tree, args)

    # LIST - list - node-set.
    elif isinstance(xp_result, list):
        try:
            # List can be empty.
            print_result_list(xp_result, el_tree, args)
        except BrokenPipeError:
            sys.stderr.close()

    # BOOLEAN - bool - boolean.
    elif isinstance(xp_result, bool):
        print(f"XPath test: {xp_result}")

    # FLOAT - float.
    elif isinstance(xp_result, float):
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

    else:
        sys.stderr.write(f"Unknown XPath result: {xp_result}\n")


def xpath_on_xml(
    xml_source: Union[TextIO, str],
    parser: etree.XMLParser,
    xpath_fn: Callable[[etree._ElementTree, str, dict[str, str]], Any],
    args: argparse.Namespace,
) -> bool:
    """Apply XPath expression to XML source.

    :param xml_source: XML file, file-like object or URL
    :param parser: XML parser
    :param xpath_fn: ElementTree.xpath method or XPath class
    :param args: command-line arguments
    """
    # ElementTree (lxml.etree._ElementTree).
    el_tree = build_etree(xml_source, parser=parser, lenient=False)
    if el_tree is None:
        return False

    # Determine XML namespaces.
    ns_map = namespaces(el_tree, args.exslt, args.default_ns_prefix)
    # XPath expression on ElementTree.
    xp_result = xpath_fn(el_tree, args.xpath_expr, ns_map)
    if xp_result is None:
        return False

    # Printable name for sys.stdin.
    source_name = get_source_name(xml_source)

    # XML sources names (--files-with-hits/--files-without-hits).
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

    # Result count (--count).
    if args.count:
        xp_result_count = len(build_result_list(xp_result))
        if len(args.xml_sources) > 1:
            print(f"{source_name}:{xp_result_count}")
        else:
            print(xp_result_count)
        return True

    # XML namespaces (verbose).
    if args.verbose:
        print_xmlns(ns_map, el_tree.getroot())
    # XPath result(s) header.
    print_result_header(source_name, xp_result)
    # XPath result(s).
    print_xp_result(xp_result, el_tree, args)
    return True


def main() -> None:
    """Entry point for command line script xp."""
    # Logging to the console.
    config_logger()

    # Command line.
    args = parse_cl()

    # Valid XPath expression?
    if not build_xpath(args.xpath_expr):
        sys.exit(60)

    # XPath function and XML parser.
    (xpath_fn, xml_parser) = xp_prepare(args)

    # Use XPath on XML sources.
    extra_new_line = False
    for xml_s in args.xml_sources:
        if extra_new_line:
            print()
        elif not (args.files_with_hits or args.files_without_hits or args.count):
            extra_new_line = True
        xpath_on_xml(xml_s, xml_parser, xpath_fn, args)

    if not args.xml_sources:
        # Read from a pipe when no XML source is specified.
        if not sys.stdin.isatty():
            xpath_on_xml(sys.stdin, xml_parser, xpath_fn, args)
        else:
            sys.stderr.write("Error: no XML source specified\n")
            sys.exit(70)
