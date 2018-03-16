import inspect
import re


BINDS = {
    'hear': [],
    'reply': [],
}


def func_to_description(func):
    return '.'.join((
        inspect.getmodule(func).__name__,
        func.__name__,
    ))


def bind(bind_type, pattern):
    def inner(func):
        BINDS[bind_type].append((func_to_description(func), pattern, re.compile(pattern, re.I), func))
    return inner
