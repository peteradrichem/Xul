# -*- coding: utf-8 -*-

"""Logging.

Python logging URLs:
    https://docs.python.org/library/logging.html
    https://docs.python.org/library/logging.handlers.html
    https://docs.python.org/library/logging.config.html
    https://docs.python.org/howto/logging.html
    https://docs.python.org/howto/logging-cookbook.html
"""


# Standard Python.
import logging


# Module logging initialisation.
logger = logging.getLogger(__name__)

# Logging level names.
log_levels = {
    'debug':    logging.DEBUG,
    'info':     logging.INFO,
    'warning':  logging.WARNING,
    'error':    logging.ERROR,
    'critical': logging.CRITICAL}


def lvl_name2num(name):
    """Return the numeric value of the `name` logging level.

       Log an error for nonexistent `name` and return `logging.NOTSET`.
            https://docs.python.org/library/logging.html#levels
    """
    try:
        levelno = log_levels[name]
    except KeyError:
        logger.error("Log level not set: '%s' is not a valid level", name)
        logger.error("Fix the log level configuration")
        return logging.NOTSET
    else:
        return levelno


def setup_logger(log_level='debug', propagate=True):
    """Configureer threshold log level van de root logger.

       log_level -- threshold log level
       propagate -- messages doorgeven naar boven [default: ja]

       Log records worden door message handlers verwerkt.
       Met setup_logger_console() wordt de console handler gekoppeld.
    """
    # logger '' staat voor de root logger
    logging.getLogger('').setLevel(lvl_name2num(log_level))
    if not propagate:
        # Er hoeft niet dubbel gelogd te worden
        logging.getLogger('').propagate = False


def customize_handler(handler, level, fmt=None, datefmt=None):
    """Configureer level en formatering van een log message handler.

       handler -- log message handler (StreamHandler, FileHandler ...)
       level -- log level voor de handler
       fmt -- formatering voor LogRecord
            https://docs.python.org/library/logging.html#logrecord-attributes
       datefmt -- datum en tijd formatering

       Geef log message handler terug.
    """
    # Configureer log level
    handler.setLevel(lvl_name2num(level))
    # Formatering aanpassen, indien gewenst.
    if fmt or datefmt:
        handler.setFormatter(logging.Formatter(fmt=fmt, datefmt=datefmt))

    return handler


def setup_logger_console(log_level='info'):
    """Setup de root logger en koppel de console handler.

       log_level -- console log level [default 'info']

       Logging op het console (sys.stderr) voor de command line.

       Geef console handler (StreamHandler) terug.
            https://docs.python.org/library/logging.handlers.html#streamhandler
    """
    # Configureer threshold log level DEBUG voor de root logger (i.p.v. WARNING).
    setup_logger()

    # Configureer de console handler.
    console_handler = customize_handler(logging.StreamHandler(), log_level)
    # Koppel console handler aan de root logger.
    logging.getLogger('').addHandler(console_handler)

    return console_handler
