# -*- coding: utf-8 -*-

"""XML Validation.

XML Schema Definition (XSD):
    https://www.w3.org/XML/Schema

Document Type Definition (DTD):
    https://en.wikipedia.org/wiki/Document_type_definition

RELAX NG:
    https://relaxng.org/

Validation with lxml:
    https://lxml.de/validation.html
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


def build_xml_schema(xsd_file):
    """Parse an XSD file into an XMLSchema validator.

    xsd_file -- XSD file (XML schema file)

    Return XMLSchema validator (lxml.etree.XMLSchema) on success.
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
        if inst.error_log.last_error.line == 0:
            # The XML document '%s' is not a schema document.
            logger.error(inst)
            return None
        logger.error("XML file '%s' is not a valid XSD file", xsd_file)
        # Lines with XSD parse errors are logged as warnings.
        for e in inst.error_log:
            # E.g. e.level_name: "ERROR", e.domain_name: "SCHEMASP",
            # e.type_name: "SCHEMAP_S4S_ATTR_INVALID_VALUE".
            logger.warning("line %i, column %i: %s", e.line, e.column, e.message)
        return None
    else:
        return validator


def build_dtd(dtd_file):
    """Parse a DTD file into a DTD validator.

    dtd_file -- DTD file

    Return DTD validator (lxml.etree.DTD) on success.
    Return None on error.

    The lxml.etree.DTD class:
        https://lxml.de/validation.html#id1
        https://lxml.de/api/lxml.etree.DTD-class.html
    """
    try:
        validator = etree.DTD(file=dtd_file)
    # Catch DTD parse errors.
    except etree.DTDParseError as inst:
        if inst.error_log.last_error.line == 0:
            # error parsing DTD
            logger.error(inst)
            # "failed to load external entity" when file does not exist.
            logger.error(inst.error_log.last_error.message)
            return None
        logger.error("'%s' is not a valid DTD file", dtd_file)
        # Lines with DTD parse errors are logged as warnings.
        for e in inst.error_log:
            # E.g. e.level_name: "FATAL", e.domain_name: "PARSER",
            # e.type_name: "ERR_EXT_SUBSET_NOT_FINISHED"
            logger.warning("line %i, column %i: %s", e.line, e.column, e.message)
        return None
    else:
        return validator


def xml_validator(xml_source, validator, lenient=True):
    """Validate an XML source against an XSD, DTD or RELAX NG validator.

    xml_source -- XML file, file-like object or URL
    validator -- XMLSchema, DTD validator or RELAX NG validator
    lenient -- log XML (validation) errors as warnings

    Return a tuple with the validation result (True/False) and the status string.
    """
    el_tree = build_etree(xml_source, lenient=lenient)
    if not el_tree:
        return (False, "Not an XML source")

    if xml_source in ('-', sys.stdin):
        # <stdin>.
        source_name = sys.stdin.name
    else:
        source_name = xml_source
    if validator.validate(el_tree):
        logger.info("XML source '%s' validates", source_name)
        return (True, "XML source validates")

    if lenient:
        val_logger = logger.warning
    else:
        val_logger = logger.error
    val_logger("XML source '%s' does not validate", source_name)
    # Lines with XML validation errors.
    for e in validator.error_log:
        # E.g. DTD e.level_name: "ERROR", e.domain_name: "VALID",
        # e.type_name: "DTD_UNKNOWN_ELEM".
        # E.g. XSD e.level_name: "ERROR", e.domain_name: "SCHEMASV",
        # e.type_name: "SCHEMAV_CVC_ELT_1".
        val_logger("line %i, column %i: %s", e.line, e.column, e.message)
    # Return the status string: first validation error.
    e = validator.error_log[0]
    return (False, "line %i, column %i: %s" % (e.line, e.column, e.message))


def build_relaxng(relaxng_file):
    """Parse a RELAX NG file into a RELAX NG validator.

    relaxng_file -- RELAX NG file

    Return RelaxNG validator (lxml.etree.RelaxNG) on success.
    Return None on error.

    The lxml.etree.RelaxNG class:
        https://lxml.de/validation.html#relaxng
        https://lxml.de/api/lxml.etree.RelaxNG-class.html
    """
    relaxng_etree = build_etree(relaxng_file, lenient=False)
    if not relaxng_etree:
        return None

    try:
        validator = etree.RelaxNG(relaxng_etree)
    # Catch RELAX NG parse errors.
    except etree.RelaxNGParseError as inst:
        logger.error("XML file '%s' is not a valid RELAX NG file", relaxng_file)
        if inst.error_log.last_error.line == -1:
            # xmlRelaxNGParse: schemas is empty.
            logger.error(inst)
            return None
        # Lines with RELAX NG parse errors are logged as warnings.
        for e in inst.error_log:
            # E.g. e.level_name: "ERROR", e.domain_name: "RELAXNGP",
            # e.type_name: "RNGP_UNKNOWN_CONSTRUCT".
            logger.warning("line %i, column %i: %s", e.line, e.column, e.message)
        return None
    else:
        return validator


def validate_xml(xml_source, validator, lenient=True, silent=False):
    """Validate an XML source against an XSD, DTD or RELAX NG validator.

    xml_source -- XML file, file-like object or URL
    validator -- XMLSchema, DTD validator or RELAX NG validator
    lenient -- log XML (validation) errors as warnings
    silent -- no logging

    Return the validation result (True/False).
    """
    el_tree = build_etree(xml_source, lenient=lenient, silent=silent)
    if not el_tree:
        return False

    if xml_source in ('-', sys.stdin):
        # <stdin>.
        source_name = sys.stdin.name
    else:
        source_name = xml_source

    if validator.validate(el_tree):
        if not silent:
            logger.info("XML source '%s' validates", source_name)
        return True
    if silent:
        return False

    # Log validation errors.
    if lenient:
        val_logger = logger.warning
    else:
        val_logger = logger.error
    val_logger("XML source '%s' does not validate", source_name)
    # Lines with XML validation errors.
    for e in validator.error_log:
        # E.g. DTD e.level_name: "ERROR", e.domain_name: "VALID",
        # e.type_name: "DTD_UNKNOWN_ELEM".
        # E.g. XSD e.level_name: "ERROR", e.domain_name: "SCHEMASV",
        # e.type_name: "SCHEMAV_CVC_ELT_1".
        val_logger("line %i, column %i: %s", e.line, e.column, e.message)
    return False
