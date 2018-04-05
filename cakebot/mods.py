import cakebot.logging
from cakebot import KILL_SWITCH
from cakebot.bind import bind


ZERO_WIDTH_SPACE = '\u200b'


class DeathException(Exception):
    pass


@bind('hear', '^{kill}$'.format(kill=KILL_SWITCH))
def die(self, conn, event, message, match):
    warning = '[{nickname}] Aaaargh -- {reply} -- my only weakness!'.format(
        nickname=conn.get_nickname(),
        reply=match.group(0),
    )
    cakebot.logging.warning(warning)
    raise DeathException(warning)


@bind('reply', '^echo (.*)')
def echo(self, conn, event, message, match):
    reply = match.group(1)
    self.send(conn, event, reply)


def pingless_nick(nick):
    return nick[0] + ZERO_WIDTH_SPACE + nick[1:]


def forward(self, conn, event, message, match):
    if event.target in self.listens:
        prefix = '.'.join((
            event.target,
            pingless_nick(event.source.nick),
        ))
        message = '{prefix}: `{message}`'.format(prefix=prefix, message=message)
        for channel in self.forwards:
            event.target = channel
            self.send(conn, event, message)
