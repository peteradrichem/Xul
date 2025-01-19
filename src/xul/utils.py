"""Xul utilities."""

import io
import logging
from typing import TextIO, Union


def config_logger(log_level: int = logging.INFO) -> None:
    """Configure the root logger and add console handler.

    log_level -- console log level [default 'info']

    Console logging (sys.stderr) for the command line scripts.
    """
    # Configure threshold log level for the root logger.
    logging.getLogger("").setLevel(logging.DEBUG)

    # Configure console handler (StreamHandler).
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)

    # Attach the console handler to the root logger.
    logging.getLogger("").addHandler(console_handler)


def get_source_name(xml_source: Union[TextIO, str]) -> str:
    """Return the name of XML source."""
    if isinstance(xml_source, str):
        return xml_source
    if isinstance(xml_source, io.TextIOWrapper):
        # e.g. sys.stdin
        return xml_source.name
    if isinstance(xml_source, io.StringIO):
        return "StringIO"
    # ?
    return str(xml_source)
