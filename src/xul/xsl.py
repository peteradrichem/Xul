"""XSL Transformations.

XSLT with lxml
    https://lxml.de/xpathxslt.html#xslt
"""

import sys
from logging import getLogger
from typing import Optional, TextIO, Union

# pylint: disable=no-member
from lxml import etree

from .etree import build_etree

logger = getLogger(__name__)


def build_xsl_transform(xslt_source: Union[TextIO, str]) -> Optional[etree.XSLT]:
    """Parse an XSLT source into an XSL Transformer.

    :param xslt_source: XSLT file, file-like object or URL

    Lines with XSLT parse errors are logged as warnings.

    Return XSL Transformer (lxml.etree.XSLT) on success.
    Return None on error.

    The lxml.etree.XSLT class:
        https://lxml.de/apidoc/lxml.etree.html#lxml.etree.XSLT
    I/O access control in XSLT:
        https://lxml.de/resolvers.html#i-o-access-control-in-xslt
    """
    xslt_etree = build_etree(xslt_source, lenient=False)
    if not xslt_etree:
        return None

    try:
        return etree.XSLT(xslt_etree)
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


def etree_transformer(
    el_tree: etree._ElementTree, transformer: etree.XSLT, **params
) -> Optional[etree._XSLTResultTree]:
    """Transform an ElementTree with an XSL Transformer.

    :param el_tree: lxml ElementTree
    :param transformer: XSL Transformer
    :param params: (optional) XSL style sheet parameters:
        https://lxml.de/xpathxslt.html#stylesheet-parameters

    XSLT lines with apply errors are logged as warnings.

    Return lxml.etree._XSLTResultTree object on success.
    Return None on error.
    """
    try:
        if params:
            return transformer(el_tree, **params)
        return transformer(el_tree)
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


def xml_transformer(
    xml_source: Union[TextIO, str],
    transformer: etree.XSLT,
    parser: Optional[etree.XMLParser] = None,
) -> Optional[etree._XSLTResultTree]:
    """Transform an XML source with an XSL Transformer.

    :param xml_source: XML file, file-like object or URL
    :param transformer: XSL Transformer
    :param parser: (optional) XML parser

    Return lxml.etree._XSLTResultTree object on success.
    Return None on error.
    """
    el_tree = build_etree(xml_source, parser=parser, lenient=False)
    if not el_tree:
        return None

    if xslt_result := etree_transformer(el_tree, transformer):
        return xslt_result

    name = sys.stdin.name if xml_source in ("-", sys.stdin) else xml_source
    logger.error("XSL transformation on '%s' failed", name)
    return None
