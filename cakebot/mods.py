from cakebot.bind import bind


@bind('reply', '^echo (.*)')
def echo(self, conn, entry, message, match):
    reply = match.group(1)
    self.send(conn, entry, reply)


@bind('hear', '(.*)')
def log(self, conn, entry, message, match):
    reply = match.group(1)
    print('I heard this: ' + reply)
