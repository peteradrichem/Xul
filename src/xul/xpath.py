"""XPath.

XPath with lxml
    https://lxml.de/xpathxslt.html#xpath

The XPath result depends on the XPath expression used.
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

# pylint: disable=no-name-in-module
from lxml.etree import LIBXSLT_COMPILED_VERSION, XPath, XPathEvalError, XPathSyntaxError

# Import my own modules.
from .etree import build_etree

# Module logging initialisation.
logger = getLogger(__name__)


def build_xpath(xpath_exp, ns_map=None):
    """Build an lxml.etree.XPath instance from an XPath expression.

    xpath_exp -- XPath expression
    ns_map -- XML namespace (prefix: URI) dictionary

    Uses the lxml XPath class:
        https://lxml.de/xpathxslt.html#the-xpath-class
        https://lxml.de/apidoc/lxml.etree.html#lxml.etree.XPath
    """
    if not ns_map:
        ns_map = {}
    try:
        return XPath(xpath_exp, namespaces=ns_map)
    # Handle (parsing) errors in XPath expression.
    #   https://lxml.de/xpathxslt.html#error-handling
    except XPathSyntaxError as e:
        logger.error("%s: %s", e, xpath_exp)
        return None


def etree_xpath(el_tree, xpath_obj):
    """Apply XPath instance to an ElementTree.

    el_tree -- ElementTree (lxml.etree._ElementTree)
    xpath_obj -- lxml.etree.XPath instance; see build_xpath()
    """
    try:
        return xpath_obj(el_tree)
    # Handle errors in evaluating an XPath expression.
    #   https://lxml.de/xpathxslt.html#error-handling
    except XPathEvalError as e:
        logger.error("%s: %s", e, xpath_obj)
        return None
    # Incorrect EXSLT function call (e.g. number of arguments for re:match).
    except TypeError as e:
        logger.error("Type error %s: %s", e, xpath_obj)
        return None


def call_xpath(xml_source, xpath_obj):
    """Apply lxml.etree.XPath on an XML source.

    xml_source -- XML file, file-like object or URL
    xpath_obj -- lxml.etree.XPath instance; see build_xpath()
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


def xml_xpath(xml_source, xpath_exp):
    """Apply XPath expression to an XML source.

    xml_source -- XML file, file-like object or URL
    xpath_exp -- XPath expression

    Uses call_xpath()
    """
    xpath_obj = build_xpath(xpath_exp)
    if not xpath_obj:
        return None

    return call_xpath(xml_source, xpath_obj)


def update_ns_map(ns_map, elm, none_prefix="default"):
    """Update XPath namespace prefix mapping with element namespaces.

    ns_map -- an XML namespace prefix mapping
    elm -- element with namespaces
    none_prefix -- prefix for the default namespace in XPath

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
        if not key:
            # XPath prefix for element default namespace.
            if none_prefix not in ns_map:
                ns_map[none_prefix] = elm.nsmap[key]
        elif key not in ns_map:
            # Protect the XPath default namespace prefix.
            if not key == none_prefix:
                ns_map[key] = elm.nsmap[key]


def namespaces(el_tree, exslt=False, none_prefix="default"):
    """Collect all XML namespaces (xmlns) in ElementTree.

    el_tree -- ElementTree (lxml.etree._ElementTree)
    exslt -- add EXSLT XML namespace prefixes (libxslt 1.1.25 and newer)
    none_prefix -- prefix for the default namespace in XPath

    Return XML namespaces (xmlns) 'prefix: URI' dict.

    Namespaces.
        https://lxml.de/tutorial.html#namespaces
    """
    if exslt:
        if LIBXSLT_COMPILED_VERSION < (1, 1, 25):
            logger.warning(
                "EXSLT requires libxslt 1.1.25 or higher. " + "lxml is compiled against libxslt %s",
                ".".join(str(n) for n in LIBXSLT_COMPILED_VERSION),
            )
        # EXSLT <http://exslt.org/>
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
