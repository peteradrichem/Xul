# coding=utf-8

"""XML Document Object Model.

Document Object Model / ElementTree

W3C Document Object Model
    http://www.w3.org/DOM/

The ElementTree XML API
    https://docs.python.org/library/xml.etree.elementtree.html

ElementTree Overview
    http://effbot.org/zone/element-index.htm
"""


# Standard Python
from logging import getLogger
#
# pylint: disable=no-member
# lxml ElementTree <http://lxml.de/>
from lxml import etree


# Module logging
logger = getLogger(__name__)


def build_etree(file_obj, parser=None, lenient=True):
    """Parse XML Document Object Model from a file object.
       - file_obj: file object
       - parser: lxml.etree.XMLParser object (optional)
       - lenient: log XMLSyntaxError as warnings instead of errors

       Return XML Document Object Model on success.
       Return None on error.

       Extensible Markup Language (XML)
           http://www.w3.org/XML/

       Gebruikt lxml.etree.parse en lxml.etree.XMLParser
           http://lxml.de/parsing.html
           http://effbot.org/elementtree/elementtree-xmlparser.htm
           http://effbot.org/zone/element.htm#reading-and-writing-xml-files
    """
    # XML parser object preparation.
    #   http://lxml.de/parsing.html#parser-options
    if not parser:
        parser = etree.XMLParser(ns_clean=True)

    # Parse file object into an XML Document Object Model (ElementTree).
    try:
        xml_dom = etree.parse(file_obj, parser)
    # Catch XML exceptions.
    #   http://lxml.de/api.html#error-handling-on-exceptions
    except etree.XMLSyntaxError as inst:
        if lenient:
            xmllogger = logger.warning
        else:
            xmllogger = logger.error
        xmllogger("%s is not an XML object:", file_obj)
        # http://lxml.de/parsing.html#error-log
        # [http://lxml.de/api/lxml.etree._LogEntry-class.html]
        for e in inst.error_log:
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


def build_xsl_transform(xslt_file):
    """ Bouw een XSL transformer object op uit een XSLT bestand
        - xslt_file: XSLT bestand

        Geeft lxml.etree.XSLT object terug.
        Bij problemen:
            - XSLT fouten worden gelogd als warnings
            - als resultaat wordt None teruggegeven

        Extensible Stylesheet Language Transformatie (XSLT)
            http://www.w3.org/Style/XSL/
    """
    # XSLT bestand dient valide XML te zijn
    xslt_tree = build_etree(xslt_file, lenient=False)
    if not xslt_tree:
        return None

    # Probeer een XSL Transformatie object op te bouwen (XSL transformer)
    #   http://lxml.de/xpathxslt.html#xslt
    # I/O access control in XSLT
    #   http://lxml.de/resolvers.html
    try:
        xsl_transform = etree.XSLT(xslt_tree)
    # Vang XSLT fouten af
    except etree.XSLTParseError as inst:
        logger.error("XML file '%s' is not a valid XSLT file", xslt_file)
        if not inst.error_log:
            logger.error("XSLTParseError: %s", inst)
        for e in inst.error_log:
            # Bijv. e.level_name: "ERROR", e.domain_name: "XSLT", e.type_name: "ERR_OK"
            if e.line == 0:
                logger.error(e.message)
            else:
                logger.warning("line %i, column %i: %s", e.line, e.column, e.message)
        return None
    else:
        return xsl_transform


def etree_transformer(xml_dom, transformer, **params):
    """ Transformeer een ElementTree via een XSL transformer
        - xml_dom: XML Document Object Model
        - transformer: XSL Transformer (lxml.etree.XSLT)
        - params: XSL parameters (optioneel)
            http://lxml.de/xpathxslt.html#stylesheet-parameters

        Het resultaat is een XML Document Object Model bij succes
        en None bij problemen

        Transformatie fouten worden gelogd als warnings
    """
    try:
        if params:
            xml_result = transformer(xml_dom, **params)
        else:
            xml_result = transformer(xml_dom)
    # Vang XSL Transformation fouten af
    except etree.XSLTApplyError as inst:
        if not inst.error_log:
            logger.error("XSLTApplyError: %s", inst)
        else:
            logger.error("XSLTApplyError on ElementTree")
        for e in inst.error_log:
            # Bijv. e.level_name: "ERROR", e.domain_name: "XSLT", e.type_name: "ERR_OK"
            if e.line == 0:
                logger.error(e.message)
            else:
                logger.warning("line %i, column %i: %s", e.line, e.column, e.message)
        return None
    else:
        return xml_result


def xml_transformer(xml_file, transformer):
    """ Transformeer een XML bestand via een XSL transformer
        - xml_file: XML bestand
        - transformer: XSL Transformer (lxml.etree.XSLT)

        Het resultaat is een XML Document Object Model bij succes
        en None bij problemen
    """
    # Maak XML Document Object Model van het XML bestand
    xml_dom = build_etree(xml_file, lenient=False)
    if not xml_dom:
        return None

    # Probeer de XML DOM (ElementTree) te transformeren
    xml_result = etree_transformer(xml_dom, transformer)
    if xml_result:
        return xml_result
    else:
        logger.error("XSL transformation on '%s' failed", xml_file)
        return None


def build_xml_schema(xsd_file):
    """ Bouw een XMLSchema validator object op uit een XSD bestand
        - xsd_file: XSD bestand

        Geeft lxml.etree.XMLSchema object terug.
        Bij problemen:
            - XSD fouten worden gelogd als warnings
            - als resultaat wordt None teruggegeven

        XML Schema Definition (XSD)
            http://www.w3.org/XML/Schema

        Gebruikt lxml.etree.XMLSchema
            http://lxml.de/validation.html#xmlschema
            http://lxml.de/api/lxml.etree.XMLSchema-class.html
    """
    # XSD bestand dient valide XML bestand te zijn
    xsd_tree = build_etree(xsd_file, lenient=False)
    if not xsd_tree:
        return None

    # Probeer een XMLSchema validator object op te bouwen
    #   http://lxml.de/validation.html#xmlschema
    try:
        validator = etree.XMLSchema(xsd_tree)
    # Vang XSD fouten af
    except etree.XMLSchemaParseError as inst:
        if inst.error_log.last_error.line != 0:
            logger.error("XML file '%s' is not a valid XSD file", xsd_file)
        for e in inst.error_log:
            # Bijv. e.level_name: "ERROR", e.domain_name: "SCHEMASP",
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
    """ Bouw een DTD validator object op uit een DTD bestand
        - dtd_file: DTD bestand

        Geeft lxml.etree.DTD object terug.
        Bij problemen:
            - DTD fouten worden gelogd als warnings
            - als resultaat wordt None teruggegeven

        Document Type Definition (DTD)
            http://en.wikipedia.org/wiki/Document_Type_Definition

        Gebruikt lxml.etree.DTD
            http://lxml.de/validation.html#id1
    """
    # Probeer de DTD file te parsen
    #   http://lxml.de/validation.html#id1
    try:
        validator = etree.DTD(file=dtd_file)
    # Vang DTD fouten af
    #   "failed to load external entity" bij niet bestaand bestand
    except etree.DTDParseError as inst:
        logger.error("'%s' is not a DTD file:", dtd_file)
        for e in inst.error_log:
            # Bijv. e.level_name: "FATAL", e.domain_name: "PARSER",
            # e.type_name: "ERR_EXT_SUBSET_NOT_FINISHED"
            if e.line == 0:
                logger.error(e.message)
            else:
                logger.warning("line %i, column %i: %s", e.line, e.column, e.message)
        return None
    else:
        return validator


def xml_validator(xml_file, validator):
    """ Valideer een XML bestand tegen een XSD/DTD validator
        - xml_file: XML bestand
        - validator: XMLSchema (lxml.etree.XMLSchema) of DTD validator (lxml.etree.DTD)

        Validatie fouten worden gelogd als warnings

        Geeft een tuple terug met het resultaat van de validatie (True/False)
        en string met status tekst
    """
    # Maak XML Document Object Model van het XML bestand
    xml_dom = build_etree(xml_file)
    if not xml_dom:
        return (False, "Not an XML file")

    # Probeer de XML DOM (ElementTree) te valideren
    if validator.validate(xml_dom):
        logger.info("XML file '%s' validates", xml_file)
        return (True, "XML file validates")
    else:
        # Error is onnodig luid bij ongeldige leverancier XML
        logger.warning("XML file '%s' does not validate:", xml_file)
        for e in validator.error_log:
            # Bijv. DTD e.level_name: "ERROR", e.domain_name: "VALID",
            # e.type_name: "DTD_UNKNOWN_ELEM"
            # Bijv. XSD e.level_name: "ERROR", e.domain_name: "SCHEMASV",
            # e.type_name: "SCHEMAV_CVC_ELT_1"
            logger.warning("line %i, column %i: %s", e.line, e.column, e.message)
        # Geef alleen de eerste validatie fout terug
        e = validator.error_log[0]
        return (False, "line %i, column %i: %s" % (e.line, e.column, e.message))
