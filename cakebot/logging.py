import datetime
import logging

from cakebot import __program__


def set_verbosity(verbose):
    if verbose == 0:
        logging.basicConfig(level=logging.WARNING)
    elif verbose == 1:
        logging.basicConfig(level=logging.INFO)
    elif verbose > 1:
        logging.basicConfig(level=logging.DEBUG)


def prepend_timestamp(func):
    def inner(message):
        timestamp = str(datetime.datetime.now())
        return func(' '.join((
            timestamp,
            message
        )))
    return inner


@prepend_timestamp
def warning(message):
    logging.getLogger(__name__).warning(message)


@prepend_timestamp
def info(message):
    logging.getLogger(__name__).info(message)


@prepend_timestamp
def debug(message):
    logging.getLogger(__name__).debug(message)
