import config
from twitch_client import TwitchClient

from commands.snap import SnapCommand
from commands.thanos import ThanosCommand

import traceback


client = TwitchClient(config.HOST, config.PORT, config.NICK, config.PASS, config.CHANNEL)

client.connect()

#def on_message(user, msg):
#  client.send_message(msg)


#client.on("message", on_message)

client.register_command(SnapCommand())
client.register_command(ThanosCommand())

while(True):
  try:
    client.run()
  except KeyboardInterrupt:
    raise
  except:
    print(traceback.format_exc())
    client = TwitchClient(config.HOST, config.PORT, config.NICK, config.PASS, config.CHANNEL)
    client.connect()
    client.register_command(SnapCommand())
    client.register_command(ThanosCommand())
    client.run()