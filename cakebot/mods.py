import cakebot.logging
from cakebot import KILL_SWITCH
from cakebot.bind import bind


class DeathException(Exception):
    pass


@bind('hear', '^{kill}$'.format(kill=KILL_SWITCH))
def die(self, conn, event, message, match):
    warning = 'Aaaargh -- {reply} -- my only weakness!'.format(reply=match.group(0))
    cakebot.logging.warning(warning)
    raise DeathException(warning)


@bind('reply', '^echo (.*)')
def echo(self, conn, event, message, match):
    reply = match.group(1)
    self.send(conn, event, reply)


def forward(self, conn, event, message, match):
    if event.target in self.listens:
        prefix = '.'.join((
            event.target,
            event.source.nick,
        ))
        message = '{prefix}: `{message}`'.format(prefix=prefix, message=message)
        for channel in self.forwards:
            event.target = channel
            self.send(conn, event, message)
