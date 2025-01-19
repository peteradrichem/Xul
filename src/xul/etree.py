"""ElementTree XML API.

The ElementTree XML API
    https://docs.python.org/3/library/xml.etree.elementtree.html

lxml ElementTree
    https://lxml.de/apidoc/lxml.etree.html#lxml.etree._ElementTree
    https://lxml.de/compatibility.html

The lxml.etree Tutorial
    https://lxml.de/tutorial.html
"""

from logging import getLogger
from typing import Optional, TextIO, Union

from lxml import etree

from .utils import get_source_name

logger = getLogger(__name__)


def build_etree(
    xml_source: Union[TextIO, str],
    parser: Optional[etree.XMLParser] = None,
    lenient: bool = True,
    silent: bool = False,
) -> Optional[etree._ElementTree]:
    """Parse XML source into an ElementTree.

    :param xml_source: XML file, file-like object or URL
    :param parser: (optional) XML parser
    :param lenient: log XMLSyntaxError as warnings instead of errors
    :param silent: disable logging

    Return ElementTree (lxml.etree._ElementTree) on success.
    Return None on error.

    The lxml.etree.parse function:
        https://lxml.de/parsing.html
    Parser options (lxml.etree.XMLParser class):
        https://lxml.de/parsing.html#parser-options
    """
    # XML parser preparation.
    if not parser:
        parser = etree.XMLParser(ns_clean=True)

    file_name = get_source_name(xml_source)
    try:
        etree.clear_error_log()
        return etree.parse(xml_source, parser)

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
        xmllogger("%s is not a valid XML source:", file_name)

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

    # Catch UnicodeDecodeError exceptions, for example:
    #   "'utf-8' codec can't decode byte 0xff in position 0: invalid start byte"
    except UnicodeDecodeError as e:
        logger.error("%s: %s", file_name, e)
        return None

    # Catch OSError exceptions, for example:
    #   Error reading file '404.xml': failed to load external entity "404.xml"
    except OSError as e:
        logger.error(e)
        return None
