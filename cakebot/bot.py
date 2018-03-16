from cakebot.config import Config

import irc.bot
import irc.connection
import ssl


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

    def on_nicknameinuse(self, c, s):
        old = c.get_nickname()
        new = old + '_'
        print('Nick {old} already in use; trying {new}'.format(old=old,new=new))
        c.nick(new)

    def on_welcome(self, c, e):
        for channel in self.config.autojoin:
            print('Autojoining {channel}'.format(channel=channel))
            c.join(channel)

    def on_pubmsg(self, c, e):
        at_me = False
        print(e)
        msg = e.arguments[0].strip()

        if msg.lower().startswith(c.get_nickname().lower()):
            at_me = True
            msg = msg.rstrip(':,')

        if at_me:
            print(msg)
