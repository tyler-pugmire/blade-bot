import command
import random
import math
import time

timeouts = [ 1, 10, 50, 100, 200, 500, 750, 1000, 1500, 2000 ]

class ThanosCommand(command.Command):
  def __init__(self,):
    super().__init__("thanos", 10.0, command.Permissions.viewers)
    self.users = {}

  def run(self, client, user, msg):
    coin = random.randint(0, 1)
    if not user in self.users:
      self.users[user] = 0

    if(coin == 0):
      client.send_message("{} You have been PURGED! CRUMBLE TO ASHES!".format(user))
      client.timeout(user, timeouts[self.users[user]])
      self.users[user] = 0
    else:
      client.send_message("{} You have been deemed worthy and are spared.".format(user))
      self.users[user] = min(self.users[user] + 1, len(timeouts) - 1)


