# -*- coding: utf-8 -*-

"""XML Document Object Model / ElementTree XML API.

W3C Document Object Model:
    https://www.w3.org/DOM/

The ElementTree XML API:
    https://docs.python.org/library/xml.etree.elementtree.html

ElementTree Overview:
    https://effbot.org/zone/element-index.htm
"""


# Standard Python.
from logging import getLogger
# pylint: disable=no-member
# lxml ElementTree <https://lxml.de/>
from lxml import etree


# Module logging initialisation.
logger = getLogger(__name__)


def build_etree(xml_source, parser=None, lenient=True):
    """Parse XML source into an XML Document Object Model (ElementTree).

    xml_source -- XML file, file-like object or URL
    parser -- (optional) XML parser (lxml.etree.XMLParser)
    lenient -- log XMLSyntaxError as warnings instead of errors

    Return XML Document Object Model on success.
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
        xml_dom = etree.parse(xml_source, parser)
    # Catch XML syntax errors.
    #   https://lxml.de/api.html#error-handling-on-exceptions
    # error log copy attached to the exception: global error log of all errors
    # that occurred at the application level.
    except etree.XMLSyntaxError:
        if lenient:
            xmllogger = logger.warning
        else:
            xmllogger = logger.error
        if hasattr(xml_source, "name"):
            name = xml_source.name
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
        return xml_dom


def build_xsl_transform(xslt_source):
    """Parse an XSLT source into an XSL Transformer.

    xslt_source -- XSLT file, file-like object or URL

    Lines with XSLT parse errors are logged as warnings.

    Return XSL Transformer (lxml.etree.XSLT) on success.
    Return None on error.

    The Extensible Stylesheet Language Family (XSL):
        https://www.w3.org/Style/XSL/
    XSL Transformations (XSLT):
        https://www.w3.org/TR/xslt

    The lxml.etree.XSLT class:
        https://lxml.de/api/lxml.etree.XSLT-class.html
        https://lxml.de/xpathxslt.html#xslt
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


def etree_transformer(xml_dom, transformer, **params):
    """Transform an XML DOM (ElementTree) with an XSL Transformer.

    xml_dom -- XML Document Object Model
    transformer -- XSL Transformer (lxml.etree.XSLT)
    params -- (optional) XSL style sheet parameters:
        https://lxml.de/xpathxslt.html#stylesheet-parameters

    XSLT lines with apply errors are logged as warnings.

    Return XML Document Object Model on success.
    Return None on error.
    """
    try:
        if params:
            xml_result = transformer(xml_dom, **params)
        else:
            xml_result = transformer(xml_dom)
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
        return xml_result


def xml_transformer(xml_source, transformer, parser=None):
    """Transform an XML source with an XSL Transformer.

    xml_source -- XML file, file-like object or URL
    transformer -- XSL Transformer (lxml.etree.XSLT)
    parser -- (optional) XML parser (lxml.etree.XMLParser)

    Return XML Document Object Model on success.
    Return None on error.
    """
    xml_dom = build_etree(xml_source, parser=parser, lenient=False)
    if not xml_dom:
        return None

    xml_result = etree_transformer(xml_dom, transformer)
    if xml_result:
        return xml_result

    if hasattr(xml_source, "name"):
        name = xml_source.name
    else:
        name = xml_source
    logger.error("XSL transformation on '%s' failed", name)
    return None


def build_xml_schema(xsd_file):
    """Parse an XSD file into an XMLSchema Validator.

    xsd_file -- XSD file (XML file)

    Lines with XSD parse errors are logged as warnings.

    Return XMLSchema Validator (lxml.etree.XMLSchema) on success.
    Return None on error.

    XML Schema Definition (XSD):
        https://www.w3.org/XML/Schema

    The lxml.etree.XMLSchema class:
        https://lxml.de/validation.html#xmlschema
        https://lxml.de/api/lxml.etree.XMLSchema-class.html
    """
    xsd_etree = build_etree(xsd_file, lenient=False)
    if not xsd_etree:
        return None

    try:
        validator = etree.XMLSchema(xsd_etree)
    # Catch XSD parse errors.
    except etree.XMLSchemaParseError as inst:
        if inst.error_log.last_error.line != 0:
            logger.error("XML file '%s' is not a valid XSD file", xsd_file)
        for e in inst.error_log:
            # E.g. e.level_name: "ERROR", e.domain_name: "SCHEMASP",
            # e.type_name: "SCHEMAP_NOT_SCHEMA"
            if e.line == 0:
                # The XML document '%s' is not a schema document.
                logger.error(e.message)
            else:
                logger.warning("line %i, column %i: %s", e.line, e.column, e.message)
        return None
    else:
        return validator


def build_dtd(dtd_file):
    """Parse an DTD file into an DTD Validator.

    dtd_file -- DTD file

    Lines with DTD parse errors are logged as warnings.

    Return DTD Validator (lxml.etree.DTD) on success.
    Return None on error.

    Document Type Definition (DTD):
        https://en.wikipedia.org/wiki/Document_type_definition

    The lxml.etree.DTD class:
        https://lxml.de/validation.html#id1
        https://lxml.de/api/lxml.etree.DTD-class.html
    """
    try:
        validator = etree.DTD(file=dtd_file)
    # Catch DTD parse errors
    except etree.DTDParseError as inst:
        # "failed to load external entity" when file does not exist
        logger.error("'%s' is not a DTD file:", dtd_file)
        for e in inst.error_log:
            # E.g. e.level_name: "FATAL", e.domain_name: "PARSER",
            # e.type_name: "ERR_EXT_SUBSET_NOT_FINISHED"
            if e.line == 0:
                logger.error(e.message)
            else:
                logger.warning("line %i, column %i: %s", e.line, e.column, e.message)
        return None
    else:
        return validator


def xml_validator(xml_source, validator):
    """Validate an XML source against an XSD or DTD validator.

    xml_source -- XML file, file-like object or URL
    validator -- XMLSchema or DTD Validator

    Log XML validation errors as warnings.

    Return a tuple with the validation result (True/False) and the status string.
    """
    xml_dom = build_etree(xml_source)
    if not xml_dom:
        return (False, "Not an XML source")

    if validator.validate(xml_dom):
        logger.info("XML source '%s' validates", xml_source)
        return (True, "XML source validates")

    logger.warning("XML source '%s' does not validate:", xml_source)
    for e in validator.error_log:
        # E.g. DTD e.level_name: "ERROR", e.domain_name: "VALID",
        # e.type_name: "DTD_UNKNOWN_ELEM"
        # E.g. XSD e.level_name: "ERROR", e.domain_name: "SCHEMASV",
        # e.type_name: "SCHEMAV_CVC_ELT_1"
        logger.warning("line %i, column %i: %s", e.line, e.column, e.message)
    # Return the first line with a validation error (status string)
    e = validator.error_log[0]
    return (False, "line %i, column %i: %s" % (e.line, e.column, e.message))
