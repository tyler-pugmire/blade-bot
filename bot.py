import config
from twitch_client import TwitchClient

from commands.snap import SnapCommand


client = TwitchClient(config.HOST, config.PORT, config.NICK, config.PASS, config.CHANNEL)

client.connect()

#def on_message(user, msg):
#  client.send_message(msg)


#client.on("message", on_message)

client.register_command(SnapCommand())

client.run()