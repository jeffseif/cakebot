import inspect
import irc.bot
import irc.connection
import re
import ssl

import cakebot.mods
from cakebot import __version__
from cakebot.bind import BINDS
from cakebot.config import Config


class Bot(irc.bot.SingleServerIRCBot):

    @classmethod
    def from_config_path(cls, config_path):
        config = Config.from_json_path(config_path)
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

    def on_nicknameinuse(self, conn, entry):
        old = conn.get_nickname()
        new = old + '_'
        print('Nick {old} already in use; trying {new}'.format(old=old,new=new))
        conn.nick(new)

    def on_welcome(self, conn, entry):
        print('Successfully connected to AIRC!')
        for auto_channel in self.config.autojoin:
            print('Autojoining channel {channel}'.format(channel=auto_channel))
            conn.join(auto_channel)

    @staticmethod
    def get_is_to_me(nickname, message):
        return message.lower().startswith(nickname.lower())

    @staticmethod
    def strip_nick_from_message(nickname, message):
        index = len(nickname)
        if message[index] in (':', ','):
            index += 1
        return message[index:].strip()

    def action(self, conn, entry, message):
        self.send(conn, entry, '\001ACTION {message}\001'.format(message=message))

    def send(self, conn, entry, message):
        if entry.target.lower() == conn.get_nickname().lower():
            entry.target = entry.source.nick
        conn.privmsg(entry.target, message)
        print('> ({target}): {message}'.format(target=entry.target, message=message))

    def on_privmsg(self, conn, entry):
        self.respond(conn, entry, is_private=True)

    def on_pubmsg(self, conn, entry):
        self.respond(conn, entry)

    def respond(self, conn, entry, is_private=False):
        nickname = conn.get_nickname()
        message = entry.arguments[0].strip()

        if is_private or self.get_is_to_me(nickname, message):
            if not is_private:
                message = self.strip_nick_from_message(nickname, message)
            self.try_reply_or_hear(conn, entry, message, 'reply')

        self.try_reply_or_hear(conn, entry, message, 'hear')

    def try_reply_or_hear(self, conn, entry, message, bind_type):
        for name, pattern, func in BINDS[bind_type]:
            match = pattern.match(message)
            if match:
                print('{bind_type}: {name}'.format(bind_type=bind_type.upper(), name=name))
                func(self, conn, entry, message, match)
