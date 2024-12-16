# -*- coding: utf-8 -*-

"""XSL Transformations.

The Extensible Stylesheet Language Family (XSL):
    https://www.w3.org/Style/XSL/

XSL Transformations (XSLT):
    https://www.w3.org/TR/xslt

XSLT with lxml
    https://lxml.de/xpathxslt.html#xslt
"""


from logging import getLogger
import sys

# pylint: disable=no-member
# lxml ElementTree <https://lxml.de/>
from lxml import etree

# Import my own modules.
from .etree import build_etree


# Module logging initialisation.
logger = getLogger(__name__)


def build_xsl_transform(xslt_source):
    """Parse an XSLT source into an XSL Transformer.

    xslt_source -- XSLT file, file-like object or URL

    Lines with XSLT parse errors are logged as warnings.

    Return XSL Transformer (lxml.etree.XSLT) on success.
    Return None on error.

    The lxml.etree.XSLT class:
        https://lxml.de/api/lxml.etree.XSLT-class.html
    I/O access control in XSLT:
        https://lxml.de/resolvers.html#i-o-access-control-in-xslt
    """
    xslt_etree = build_etree(xslt_source, lenient=False)
    if not xslt_etree:
        return None

    try:
        xsl_transform = etree.XSLT(xslt_etree)
    # Catch XSLT parse errors.
    except etree.XSLTParseError as inst:
        logger.error("XML source '%s' is not a valid XSLT source", xslt_source)
        if not inst.error_log:
            logger.error("XSLTParseError: %s", inst)
        for e in inst.error_log:
            # E.g. e.level_name: "ERROR", e.domain_name: "XSLT", e.type_name: "ERR_OK"
            if e.line == 0:
                logger.error(e.message)
            else:
                logger.warning("line %i, column %i: %s", e.line, e.column, e.message)
        return None
    else:
        return xsl_transform


def etree_transformer(el_tree, transformer, **params):
    """Transform an ElementTree with an XSL Transformer.

    el_tree -- ElementTree (lxml.etree._ElementTree)
    transformer -- XSL Transformer (lxml.etree.XSLT)
    params -- (optional) XSL style sheet parameters:
        https://lxml.de/xpathxslt.html#stylesheet-parameters

    XSLT lines with apply errors are logged as warnings.

    Return lxml.etree._XSLTResultTree object on success.
    Return None on error.
    """
    try:
        if params:
            xslt_result = transformer(el_tree, **params)
        else:
            xslt_result = transformer(el_tree)
    # Catch XSL Transformation errors.
    except etree.XSLTApplyError as inst:
        if not inst.error_log:
            logger.error("XSLTApplyError: %s", inst)
        else:
            logger.error("XSLTApplyError on ElementTree")
        for e in inst.error_log:
            # E.g. e.level_name: "ERROR", e.domain_name: "XSLT", e.type_name: "ERR_OK"
            if e.line == 0:
                logger.error(e.message)
            else:
                logger.warning("line %i, column %i: %s", e.line, e.column, e.message)
        return None
    else:
        return xslt_result


def xml_transformer(xml_source, transformer, parser=None):
    """Transform an XML source with an XSL Transformer.

    xml_source -- XML file, file-like object or URL
    transformer -- XSL Transformer (lxml.etree.XSLT)
    parser -- (optional) XML parser (lxml.etree.XMLParser)

    Return lxml.etree._XSLTResultTree object on success.
    Return None on error.
    """
    el_tree = build_etree(xml_source, parser=parser, lenient=False)
    if not el_tree:
        return None

    xslt_result = etree_transformer(el_tree, transformer)
    if xslt_result:
        return xslt_result

    if xml_source in ('-', sys.stdin):
        name = sys.stdin.name
    else:
        name = xml_source
    logger.error("XSL transformation on '%s' failed", name)
    return None
