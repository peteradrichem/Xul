"""XPath.

XPath:
    https://lxml.de/xpathxslt.html#xpath

The XPath class:
    https://lxml.de/xpathxslt.html#the-xpath-class
    https://lxml.de/apidoc/lxml.etree.html#lxml.etree.XPath

The return value types of XPath evaluations vary, depending on the XPath expression used:
    https://lxml.de/xpathxslt.html#xpath-return-values
- attributes:               "location/@attribute"
- text nodes:               "location/text()"
- element nodes:            "location"
- comment nodes:            "location/comment()"
- processing instructions:  "location/processing-instruction()"
- boolean:                  "location/text() = 'string'"
- string:                   "namespace-uri(location)"
- float:                    "count(location)"
"""

from logging import getLogger
from typing import Optional, TextIO, Union

from lxml import etree

from .etree import build_etree

logger = getLogger(__name__)


def build_xpath(xpath_exp: str, ns_map: Optional[dict[str, str]] = None) -> Optional[etree.XPath]:
    """Build an lxml.etree.XPath instance from an XPath expression.

    :param xpath_exp: XPath expression
    :param ns_map: XML namespace (prefix: URI) dictionary
    """
    if not ns_map:
        ns_map = {}
    try:
        return etree.XPath(xpath_exp, namespaces=ns_map)
    # Handle (parsing) errors in XPath expression.
    #   https://lxml.de/xpathxslt.html#error-handling
    except etree.XPathSyntaxError as e:
        logger.error("%s: %s", e, xpath_exp)
        return None


def etree_xpath(el_tree: etree._ElementTree, xpath_obj: etree.XPath):
    """Apply XPath instance to an ElementTree.

    :param el_tree: lxml ElementTree
    :param xpath_obj: lxml.etree.XPath instance; see build_xpath()
    :return: XPath result
    """
    try:
        return xpath_obj(el_tree)
    # Handle errors in evaluating an XPath expression.
    #   https://lxml.de/xpathxslt.html#error-handling
    except etree.XPathEvalError as e:
        logger.error("%s: %s", e, xpath_obj)
        return None
    # Incorrect EXSLT function call (e.g. number of positional arguments for re:match).
    except TypeError as e:
        logger.error("%s is invalid: %s", xpath_obj, e)
        return None


def call_xpath(xml_source: Union[TextIO, str], xpath_obj: etree.XPath):
    """Apply lxml.etree.XPath to an XML source.

    :param xml_source: XML file, file-like object or URL
    :param xpath_obj: lxml.etree.XPath instance; see build_xpath()
    :return: XPath result
    """
    # Parse an XML source into an XML Document Object Model.
    el_tree = build_etree(xml_source, lenient=False)
    if not el_tree:
        # No XML source.
        return None

    xpath_result = etree_xpath(el_tree, xpath_obj)
    if xpath_result is None:
        logger.error("XPath failed on %s", xml_source)
    return xpath_result


def xml_xpath(xml_source: Union[TextIO, str], xpath_exp: str):
    """Apply XPath expression to an XML source with call_xpath().

    :param xml_source: XML file, file-like object or URL
    :param xpath_exp: XPath expression
    :return: XPath result
    """
    if xpath_obj := build_xpath(xpath_exp):
        return call_xpath(xml_source, xpath_obj)

    return None


def update_ns_map(
    ns_map: dict[str, str], elm: etree._Element, none_prefix: str = "default"
) -> None:
    """Update XPath namespace prefix mapping with element namespaces.

    :param ns_map: XML namespace (prefix: URI) dictionary
    :param elm: element with namespaces
    :param none_prefix: prefix for the default namespace in XPath

    Element namespaces:
    - xmlns, default namespace (None prefix) URI: elm.nsmap[None]
    - xmlns:prefix, namespace URI: elm.nsmap[elm.prefix]

    Remarks:
     * XPath does not have a notion of a default namespace.
       The empty namespace prefix is not supported in XPath (TypeError).
     * No protection against namespace prefix collisions.
       First occurrence (ns_map) wins.

    Namespaces and prefixes:
        https://lxml.de/xpathxslt.html#namespaces-and-prefixes
    """
    for key in elm.nsmap:
        if key is None:
            # XPath prefix for element default namespace.
            if none_prefix not in ns_map:
                ns_map[none_prefix] = elm.nsmap[key]
        # Protect the XPath default namespace prefix.
        elif not (key in ns_map or key == none_prefix):
            ns_map[key] = elm.nsmap[key]


def namespaces(
    el_tree: etree._ElementTree, exslt: bool = False, none_prefix: str = "default"
) -> dict[str, str]:
    """Collect all XML namespaces (xmlns) in ElementTree.

    :param el_tree: lxml ElementTree
    :param exslt: add EXSLT XML namespace prefixes (libxslt 1.1.25 and newer)
    :param none_prefix: prefix for the default namespace in XPath

    Return XML namespaces (xmlns) 'prefix: URI' mapping.

    Namespaces.
        https://lxml.de/tutorial.html#namespaces
    """
    if exslt:
        if etree.LIBXSLT_COMPILED_VERSION < (1, 1, 25):
            logger.warning(
                "EXSLT requires libxslt 1.1.25 or higher. lxml is compiled against libxslt %s",
                ".".join(str(n) for n in etree.LIBXSLT_COMPILED_VERSION),
            )
        # EXSLT <https://exslt.github.io/>
        ns_map = {
            "date": "http://exslt.org/dates-and-times",
            "dyn": "http://exslt.org/dynamic",
            "exsl": "http://exslt.org/common",
            "func": "http://exslt.org/functions",
            "math": "http://exslt.org/math",
            "random": "http://exslt.org/random",
            "re": "http://exslt.org/regular-expressions",
            "set": "http://exslt.org/sets",
            "str": "http://exslt.org/strings",
        }
    else:
        ns_map = {}

    # Collect XML namespaces (xmlns) in all elements.
    for elm in el_tree.iter("*"):
        if elm.nsmap:
            update_ns_map(ns_map, elm, none_prefix=none_prefix)

    return ns_map
