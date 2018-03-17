import irc.bot
import irc.connection
import ssl

import cakebot.bot
import cakebot.config
import cakebot.logging


class Swarm:

    bots = []

    def __init__(self, config_path):
        self.config = cakebot.config.Swarm.from_json_path(config_path)
        server_kwargs = {
            'server_list': [self.config.server],
        }
        if self.config.ssl:
            server_kwargs['connect_factory'] = irc.connection.Factory(wrapper=ssl.wrap_socket)

        for bot_config in self.config.bots:
            kwargs = bot_config.to_dict()
            kwargs.update(server_kwargs)
            self.bots.append(cakebot.bot.Bot.from_dict(kwargs))
        return

    def start(self):
        for bot in self.bots:
            print(bot)
            bot.start()
