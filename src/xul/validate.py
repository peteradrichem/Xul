"""XML Validation.

Validation with lxml:
    https://lxml.de/validation.html
"""

import sys
from logging import getLogger
from typing import Optional, TextIO, Union

from lxml import etree

# pylint: disable=no-member
from .etree import build_etree

logger = getLogger(__name__)


def build_xml_schema(xsd_file: Union[TextIO, str]) -> Optional[etree.XMLSchema]:
    """Parse an XSD file into an XMLSchema validator.

    :param xsd_file: XSD (XML schema) file, file-like object or URL

    Return XMLSchema validator (lxml.etree.XMLSchema) on success.
    Return None on error.

    The lxml.etree.XMLSchema class:
        https://lxml.de/validation.html#xmlschema
        https://lxml.de/apidoc/lxml.etree.html#lxml.etree.XMLSchema
    """
    xsd_etree = build_etree(xsd_file, lenient=False)
    if not xsd_etree:
        return None

    try:
        return etree.XMLSchema(xsd_etree)

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


def build_dtd(dtd_file: Union[TextIO, str]) -> Optional[etree.DTD]:
    """Parse a DTD file into a DTD validator.

    :param dtd_file: DTD file, file-like object or URL

    Return DTD validator (lxml.etree.DTD) on success.
    Return None on error.

    The lxml.etree.DTD class:
        https://lxml.de/validation.html#dtd-1
        https://lxml.de/apidoc/lxml.etree.html#lxml.etree.DTD
    """
    try:
        return etree.DTD(file=dtd_file)

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


def build_relaxng(relaxng_file: Union[TextIO, str]) -> Optional[etree.RelaxNG]:
    """Parse a RELAX NG file into a RELAX NG validator.

    :param relaxng_file: RELAX NG file, file-like object or URL

    Return RelaxNG validator (lxml.etree.RelaxNG) on success.
    Return None on error.

    The lxml.etree.RelaxNG class:
        https://lxml.de/validation.html#relaxng
        https://lxml.de/apidoc/lxml.etree.html#lxml.etree.RelaxNG
    """
    relaxng_etree = build_etree(relaxng_file, lenient=False)
    if not relaxng_etree:
        return None

    try:
        return etree.RelaxNG(relaxng_etree)

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


def xml_validator(
    xml_source: Union[TextIO, str],
    validator: Union[etree.XMLSchema, etree.DTD, etree.RelaxNG],
    lenient: bool = True,
) -> tuple[bool, str]:
    """Validate an XML source against an XSD, DTD or RELAX NG validator.

    :param xml_source: XML file, file-like object or URL
    :param validator: XMLSchema, DTD or RELAX NG validator
    :param lenient: log XML (validation) errors as warnings instead of errors

    Return a tuple with the validation result (True/False) and the status string.
    """
    el_tree = build_etree(xml_source, lenient=lenient)
    if not el_tree:
        return (False, "Not an XML source")

    if xml_source in ("-", sys.stdin):
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
    for e in validator.error_log:  # type: ignore[union-attr]
        # E.g. DTD e.level_name: "ERROR", e.domain_name: "VALID",
        # e.type_name: "DTD_UNKNOWN_ELEM".
        # E.g. XSD e.level_name: "ERROR", e.domain_name: "SCHEMASV",
        # e.type_name: "SCHEMAV_CVC_ELT_1".
        val_logger("line %i, column %i: %s", e.line, e.column, e.message)
    # Return the status string: first validation error.
    e = validator.error_log[0]  # type: ignore[index]
    return (False, f"line {e.line}, column {e.column}: {e.message}")


def validate_xml(
    xml_source: Union[TextIO, str],
    validator: Union[etree.XMLSchema, etree.DTD, etree.RelaxNG],
    lenient: bool = True,
    silent: bool = False,
):
    """Validate an XML source against an XSD, DTD or RELAX NG validator.

    :param xml_source: XML file, file-like object or URL
    :param validator: XMLSchema, DTD or RELAX NG validator
    :param lenient: log XML (validation) errors as warnings instead of errors
    :param silent: disable logging

    Return True when `xml_source' validates.
    """
    el_tree = build_etree(xml_source, lenient=lenient, silent=silent)
    if not el_tree:
        return False

    if xml_source in ("-", sys.stdin):
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
    # Lines with XML validation errors (lxml.etree._ListErrorLog).
    for e in validator.error_log:  # type: ignore[union-attr]
        # E.g. DTD e.level_name: "ERROR", e.domain_name: "VALID",
        # e.type_name: "DTD_UNKNOWN_ELEM".
        # E.g. XSD e.level_name: "ERROR", e.domain_name: "SCHEMASV",
        # e.type_name: "SCHEMAV_CVC_ELT_1".
        val_logger("line %i, column %i: %s", e.line, e.column, e.message)
    return False
