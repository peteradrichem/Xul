# coding=utf-8

"""XPath.

XML Path Language
    http://www.w3.org/TR/xpath/

XPath and XSLT with lxml
    http://lxml.de/xpathxslt.html

The XPath result depends on the XPath expression used.
    http://lxml.de/xpathxslt.html#xpath-return-values
- attributes:               "location/@attribute"
- text nodes:               "location/text()"
- element nodes:            "location"
- comment nodes:            "location/comment()"
- processing instructions:  "location/processing-instruction()"
- boolean:                  "location/text() = 'string'"
- string:                   "namespace-uri(location)"
- float:                    "count(location)"
"""


# Standard Python
from logging import getLogger
# lxml ElementTree <http://lxml.de/>
from lxml import etree

# Import my own modules
from .dom import build_etree


# Module logging
logger = getLogger(__name__)


def build_xpath(xpath_exp, ns_map=None):
    """Build an lxml.etree.XPath instance from an XPath expression.

    xpath_exp -- XPath expression
    ns_map -- XML namespace (prefix: URI) dictionary

    Uses the lxml XPath class:
        http://lxml.de/xpathxslt.html#the-xpath-class
        http://lxml.de/api/lxml.etree.XPath-class.html
    """
    if not ns_map:
        ns_map = {}
    try:
        xpath_obj = etree.XPath(xpath_exp, namespaces=ns_map)
    # Handle (parsing) errors in XPath expression
    #   http://lxml.de/xpathxslt.html#error-handling
    except etree.XPathSyntaxError as e:
        logger.error("Invalid XPath '%s'", xpath_exp)
        logger.error("XPathSyntaxError: %s", e)
        return None
    else:
        return xpath_obj


def etree_xpath(xml_dom, xpath_obj):
    """Apply XPath instance to an XML DOM.

    xml_dom -- XML Document Object Model
    xpath_obj -- lxml.etree.XPath instance; see build_xpath()
    """
    try:
        xpath_result = xpath_obj(xml_dom)
    # Handle errors in evaluating an XPath expression
    #   http://lxml.de/xpathxslt.html#error-handling
    except etree.XPathEvalError as e:
        logger.error("Invalid XPath '%s'", xpath_obj)
        logger.error("XPathEvalError: %s", e)
        return None
    # Incorrect EXSLT function call (e.g. number of arguments for re:match)
    except TypeError as e:
        logger.error("Invalid XPath '%s'", xpath_obj)
        logger.error("TypeError: %s", e)
        return None
    else:
        return xpath_result


def call_xpath(xml_file, xpath_obj):
    """Apply XPath instance to an XML file.

    xml_file -- XML file
    xpath_obj -- lxml.etree.XPath instance; see build_xpath()
    """
    # Parse an XML file into an XML Document Object Model
    xml_dom = build_etree(xml_file, lenient=False)
    if not xml_dom:
        # No XML file
        return None

    xpath_result = etree_xpath(xml_dom, xpath_obj)
    if xpath_result is None:
        logger.error("XPath failed on %s", xml_file)
    return xpath_result


def xml_xpath(xml_file, xpath_exp):
    """Apply XPath expression to an XML file.

    xml_file -- XML file
    xpath_exp -- XPath expression

    Uses call_xpath()
    """
    xpath_obj = build_xpath(xpath_exp)
    if not xpath_obj:
        return None

    return call_xpath(xml_file, xpath_obj)
