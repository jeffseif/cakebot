import inspect
import irc.bot
import irc.connection
import re
import ssl

import cakebot.bind
import cakebot.config
import cakebot.mods
from cakebot import __version__


class Bot(irc.bot.SingleServerIRCBot):

    FORWARDS = set()
    LISTENS = set()

    @classmethod
    def from_config_path(cls, config_path):
        config = cakebot.config.Config.from_json_path(config_path)
        kwargs = {
            'server_list': [config.server],
            'nickname': config.nick,
            'realname': config.realname,
        }
        if config.ssl:
            kwargs['connect_factory'] = irc.connection.Factory(wrapper=ssl.wrap_socket)
        instance = cls(**kwargs)
        instance.config = config
        return instance

    def get_version(self):
        return 'AIRC CakeBot Version {version}'.format(version=__version__)

    def on_nicknameinuse(self, conn, event):
        old = conn.get_nickname()
        new = old + '_'
        print('Nick {old} already in use; trying {new}'.format(old=old,new=new))
        conn.nick(new)

    def on_welcome(self, conn, event):
        print('Successfully connected to AIRC!')

        for channel in self.config.forwards:
            print('Forwarding to channel {channel}'.format(channel=channel))
            conn.join(channel)
            self.FORWARDS.add(channel)

        for channel in self.config.listens:
            print('Listening to channel {channel}'.format(channel=channel))
            conn.join(channel)
            self.LISTENS.add(channel)

        for pattern in self.config.patterns:
            cakebot.bind.bind('hear', pattern)(cakebot.mods.forward)

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

    def send(self, conn, event, message):
        if event.target.lower() == conn.get_nickname().lower():
            event.target = event.source.nick
        conn.privmsg(event.target, message)
        print('> ({target}): {message}'.format(target=event.target, message=message))

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
            self.try_reply_or_hear(conn, event, message, 'reply')

        self.try_reply_or_hear(conn, event, message, 'hear')

    def try_reply_or_hear(self, conn, event, message, bind_type):
        for name, pattern, match, func in cakebot.bind.BINDS[bind_type]:
            match = match.match(message)
            if match:
                print('{bind_type}: {name} (`{pattern}`)'.format(bind_type=bind_type.upper(), name=name, pattern=pattern))
                func(self, conn, event, message, match)
