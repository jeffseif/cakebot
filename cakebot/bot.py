import inspect
import irc.bot
import irc.connection
import re
import ssl

import cakebot.bind
import cakebot.config
import cakebot.logging
import cakebot.mods
from cakebot import __version__
from cakebot import KILL_SWITCH


class Bot(irc.bot.SingleServerIRCBot):

    nick_to_kill = None

    def reset_attrs(self):
        self.forwards = set()
        self.listens = set()
        self.patterns = list()

    @classmethod
    def from_dict(cls, the_dict):
        config = {
            attr: the_dict.pop(attr)
            for attr in ('forwards', 'listens', 'patterns')
        }
        instance = cls(**the_dict)
        instance.config = config
        instance.reset_attrs()
        return instance

    def get_version(self):
        return 'AIRC CakeBot Version {version}'.format(version=__version__)

    def on_nicknameinuse(self, conn, event):
        self.nick_to_kill = conn.get_nickname()
        new = '_'.join((
            self.nick_to_kill,
            'killah',
        ))
        cakebot.logging.warning('[{new}] {old} already in use; trying to kill it with {kill} as {new} ...'.format(old=self.nick_to_kill,new=new,kill=KILL_SWITCH))
        conn.nick(new)

    def on_welcome(self, conn, event):
        if self.nick_to_kill:
            event.target = self.nick_to_kill
            self.send(conn, event, KILL_SWITCH, override_target=True)
            self.die()

        nickname = conn.get_nickname()

        cakebot.logging.info('[{nickname}] successfully connected to AIRC'.format(nickname=nickname))

        for channel in self.config['forwards']:
            cakebot.logging.info('[{nickname}] forwarding to channel {channel}'.format(nickname=nickname, channel=channel))
            conn.join(channel)
            self.forwards.add(channel)

        for channel in self.config['listens']:
            cakebot.logging.info('[{nickname}] listening to channel {channel}'.format(nickname=nickname, channel=channel))
            conn.join(channel)
            self.listens.add(channel)

        for pattern in self.config['patterns']:
            self.patterns.append(cakebot.bind.bind_inner('hear', pattern, cakebot.mods.forward))

    @staticmethod
    def get_is_to_me(nickname, message):
        return message.lower().startswith(nickname.lower())

    @staticmethod
    def strip_nick_from_message(nickname, message):
        index = len(nickname)
        if message[index] in (':', ','):
            index += 1
        return message[index:].strip()

    def action(self, conn, event, message):
        self.send(conn, event, '\001ACTION {message}\001'.format(message=message))

    def send(self, conn, event, message, override_target=False):
        if (not override_target) and (event.target.lower() == conn.get_nickname().lower()):
            event.target = event.source.nick
        conn.privmsg(event.target, message)
        cakebot.logging.info('> ({target}): {message}'.format(target=event.target, message=message))

    def on_privmsg(self, conn, event):
        self.respond(conn, event, is_private=True)

    def on_pubmsg(self, conn, event):
        self.respond(conn, event)

    def respond(self, conn, event, is_private=False):
        nickname = conn.get_nickname()
        message = event.arguments[0].strip()

        if is_private or self.get_is_to_me(nickname, message):
            if not is_private:
                message = self.strip_nick_from_message(nickname, message)
            self.try_reply_or_hear(conn, event, message, cakebot.bind.BINDS['reply'])

        self.try_reply_or_hear(conn, event, message, cakebot.bind.BINDS['hear'])
        self.try_reply_or_hear(conn, event, message, self.patterns)

    def try_reply_or_hear(self, conn, event, message, binds):
        for bind_type, name, pattern, match, func in binds:
            match = match.match(message)
            if match:
                cakebot.logging.info('[{nickname}] {bind_type}: {name} (`{pattern}`)'.format(
                    nickname=conn.get_nickname(),
                    bind_type=bind_type.upper(),
                    name=name,
                    pattern=pattern,
                ))
                func(self, conn, event, message, match)
