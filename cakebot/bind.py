import inspect
import re


BINDS = {
    'hear': [],
    'reply': [],
}


def bind_inner(bind_type, pattern, func):
    return (
        bind_type,
        '.'.join((
            inspect.getmodule(func).__name__,
            func.__name__,
        )),
        pattern,
        re.compile(pattern, re.I),
        func,
    )


def bind(bind_type, pattern):
    def inner(func):
        BINDS[bind_type].append(bind_inner(bind_type, pattern, func))
    return inner
