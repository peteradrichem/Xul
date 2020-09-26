# -*- coding: utf-8 -*-

"""XML Validation.

XML Schema Definition (XSD):
    https://www.w3.org/XML/Schema

Document Type Definition (DTD):
    https://en.wikipedia.org/wiki/Document_type_definition

Validation with lxml:
    https://lxml.de/validation.html
"""


# Standard Python.
from logging import getLogger
# pylint: disable=no-member
# lxml ElementTree <https://lxml.de/>
from lxml import etree

# Import my own modules.
from .etree import build_etree


# Module logging initialisation.
logger = getLogger(__name__)


def build_xml_schema(xsd_file):
    """Parse an XSD file into an XMLSchema Validator.

    xsd_file -- XSD file (XML schema file)

    Lines with XSD parse errors are logged as warnings.

    Return XMLSchema Validator (lxml.etree.XMLSchema) on success.
    Return None on error.

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
    el_tree = build_etree(xml_source)
    if not el_tree:
        return (False, "Not an XML source")

    if validator.validate(el_tree):
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
