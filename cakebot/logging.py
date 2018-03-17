import datetime
import logging

from cakebot import __program__


def setup(verbose):
    FORMAT = '%(asctime)s:%(levelname)s:{program}:%(process)d	%(message)s'.format(program=__program__)
    if verbose == 0:
        logging.basicConfig(format=FORMAT, level=logging.WARNING)
    elif verbose == 1:
        logging.basicConfig(format=FORMAT, level=logging.INFO)
    elif verbose > 1:
        logging.basicConfig(format=FORMAT, level=logging.DEBUG)


def warning(message):
    logging.getLogger(__name__).warning(message)


def info(message):
    logging.getLogger(__name__).info(message)


def debug(message):
    logging.getLogger(__name__).debug(message)
