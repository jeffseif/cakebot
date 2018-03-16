from cakebot.bind import bind


@bind('reply', '^echo (.*)')
def echo(self, conn, event, message, match):
    reply = match.group(1)
    self.send(conn, event, reply)


# @bind('hear', '(.*)')
# def log(self, conn, event, message, match):
#     reply = match.group(1)
#     print('I heard this: ' + reply)


def forward(self, conn, event, message, match):
    if event.target in self.LISTENS:
        prefix = '.'.join((
            event.target,
            event.source.nick,
        ))
        message = '{prefix}: {message}'.format(prefix=prefix, message=message)
        for channel in self.FORWARDS:
            event.target = channel
            self.send(conn, event, message)
