# -*- coding: utf-8 -*-

"""ElementTree XML API.

The ElementTree XML API:
    https://docs.python.org/library/xml.etree.elementtree.html

ElementTree Overview:
    https://effbot.org/zone/element-index.htm

The lxml.etree Tutorial
    https://lxml.de/tutorial.html
"""


from logging import getLogger
import sys

# pylint: disable=no-member
# lxml ElementTree <https://lxml.de/>
from lxml import etree


# Module logging initialisation.
logger = getLogger(__name__)


def build_etree(xml_source, parser=None, lenient=True, silent=False):
    """Parse XML source into an ElementTree.

    xml_source -- XML file, file-like object or URL
    parser -- (optional) XML parser (lxml.etree.XMLParser)
    lenient -- log XMLSyntaxError as warnings instead of errors
    silent -- no logging

    Return ElementTree (lxml.etree._ElementTree) on success.
    Return None on error.

    Extensible Markup Language (XML):
        https://www.w3.org/XML/

    The lxml.etree.parse function:
        https://lxml.de/parsing.html
        https://effbot.org/zone/element.htm#reading-and-writing-xml-files
    Parser options (lxml.etree.XMLParser class):
        https://lxml.de/parsing.html#parser-options
        https://effbot.org/elementtree/elementtree-xmlparser.htm
    """
    # XML parser preparation.
    if not parser:
        parser = etree.XMLParser(ns_clean=True)

    try:
        el_tree = etree.parse(xml_source, parser)
    # Catch XML syntax errors.
    #   https://lxml.de/api.html#error-handling-on-exceptions
    # error log copy attached to the exception: global error log of all errors
    # that occurred at the application level.
    except etree.XMLSyntaxError:
        if silent:
            return None
        if lenient:
            xmllogger = logger.warning
        else:
            xmllogger = logger.error
        if xml_source in ('-', sys.stdin):
            name = sys.stdin.name
            xml_type = "object"
        else:
            name = xml_source
            xml_type = "file"
        xmllogger("%s is not a valid XML %s:", name, xml_type)

        # Parsers have an error_log property that lists the errors and warnings
        # of the last parser run.
        #   https://lxml.de/parsing.html#error-log
        for e in parser.error_log:
            # For example: e.level_name: "FATAL", e.domain_name: "PARSER",
            # e.type_name: "ERR_DOCUMENT_EMPTY"
            if e.line == 0:
                logger.error(e.message)
            else:
                xmllogger("line %i, column %i: %s", e.line, e.column, e.message)
        return None
    # Catch EnvironmentError (IOError) exceptions, for example:
    #   "failed to load external entity" (lxml.etree._raiseParseError)
    except EnvironmentError as e:
        logger.error(e)
        return None
    else:
        return el_tree
