# coding=utf-8

"""Logging.

Python logging URLs:
    https://docs.python.org/library/logging.html
    https://docs.python.org/library/logging.handlers.html
    https://docs.python.org/library/logging.config.html
    https://docs.python.org/howto/logging.html
    https://docs.python.org/howto/logging-cookbook.html
"""


# Standard Python
import logging


# Module logger initialisatie
logger = logging.getLogger(__name__)

# Logging level names
LOG_LEVELS = {
    'debug':    logging.DEBUG,
    'info':     logging.INFO,
    'warning':  logging.WARNING,
    'error':    logging.ERROR,
    'critical': logging.CRITICAL}


def lvl_name2num(name):
    """Return the numeric value of the LOG_LEVELS `name` logging level.

    Log an error for nonexistent `name` and return `logging.NOTSET`.

    https://docs.python.org/library/logging.html#levels
    """
    try:
        levelno = LOG_LEVELS[name]
    except KeyError:
        logger.error("Log level not set: '%s' is not a valid level", name)
        logger.error("Fix the log level configuration")
        return logging.NOTSET
    else:
        return levelno


def setup_logger(log_level='debug', name='', propagate=True):
    """ Configureer het threshold log level van de root/name logger
        - log_level: threshold log level van de logger
        - name: naam van de logger [default: root logger]
        - propagate: messages doorgeven naar boven [default: ja]

        De `propagate' optie is alleen nuttig bij name loggers.
        Merk op dat propagate=False ook gevolgen heeft voor de
        console handler (die aan de root logger hangt)

        Log records worden door handlers verwerkt:
        - file logging via add_logfile()
        - console logging zie setup_logger_console()
    """
    logging.getLogger(name).setLevel(lvl_name2num(log_level))
    if not propagate:
        # Er hoeft niet dubbel gelogd te worden
        logging.getLogger(name).propagate = False


def customize_handler(handler, level, form='%(name)-12s: %(levelname)-8s - %(message)s'):
    """ Configureer level en formattering van een log message handler
        - handler: de log message handler (StreamHandler, FileHandler ...)
        - level: log level voor de handler
        - form: log formattering voor de handler (default t.b.v. console/cron)
            https://docs.python.org/library/logging.html#logrecord-attributes

        Geeft de handler terug
    """
    # Configureer log level
    handler.setLevel(lvl_name2num(level))
    # Log formattering aanpassen, indien gewenst
    if form:
        handler.setFormatter(logging.Formatter(form))

    return handler


def setup_logger_console(log_level='info', log_format='%(message)s'):
    """ Configureer threshold log level DEBUG voor de root logger.
        Koppel console handler aan de root logger
        - log_level: console log level [default 'info']
        - log_format: log formattering voor de console handler (default t.b.v. cli)

        Logging op het console (sys.stderr) voor fout meldingen

        Geeft console handler (StreamHandler) terug
            https://docs.python.org/library/logging.handlers.html#streamhandler
    """
    # Configureer threshold log level DEBUG voor de root logger (i.p.v. WARNING)
    setup_logger('debug')

    # Configureer de console handler
    console_handler = customize_handler(
        logging.StreamHandler(), log_level, log_format)

    # Koppel console handler aan de root logger
    logging.getLogger('').addHandler(console_handler)

    # Geef de console handler terug
    return console_handler


def add_logfile(log_file, log_level, name=''):
    """ Koppel een log file (FileHandler) aan de root/name logger
        - log_file: log file voor de FileHandler
        - log_level: log level voor de FileHandler
        - name: naam van de logger [default: root logger]

        Controleer of er in de log file geschreven kan worden.
        Als dat lukt geef dan de FileHandler terug; anders None
            https://docs.python.org/library/logging.handlers.html#filehandler
    """
    # Log file
    try:
        file_obj = open(log_file, 'a')
    # Vang (IO|OS)Error exceptions af
    except EnvironmentError as e:
        logger.error("OS error %s writing to log file %s:", e.errno, log_file)
        logger.error(e.strerror)
        return None
    # geen finally, want alleen als try open() lukt is .close() nodig
    else:
        file_obj.close()

    # Configureer FileHandler (log message handler)
    file_hndlr = customize_handler(
        logging.FileHandler(log_file), log_level,
        '%(asctime)s %(levelname)s - %(message)s')

    # Koppel de FileHandler aan de root/name logger
    logging.getLogger(name).addHandler(file_hndlr)

    # Geef de file_hndlr terug
    return file_hndlr


def remove_logfile(file_hndlr, name=''):
    """ Verwijder een FileHandler van de root/name logger
        - file_hndlr: logging.FileHandler object
        - name: naam van de logger [default: root logger]
    """
    file_hndlr.close()
    logging.getLogger(name).removeHandler(file_hndlr)
    return True
