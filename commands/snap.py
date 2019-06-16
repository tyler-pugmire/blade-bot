import command
import random
import math
import time

class SnapCommand(command.Command):
  def __init__(self):
    super().__init__("snap", 0, command.Permissions.broadcaster)

  def run(self, client, user, msg):
    all_names = client.get_names()
    viewers = all_names["chatters"]["viewers"]
    half = math.ceil(len(viewers) / 2)
    snapped = []
    while len(snapped) < half:
      userToMove = random.choice(viewers)
      if userToMove in snapped:
        print("User " + userToMove + " is already to be timed out.")
      else:
        snapped.append(userToMove)
    
    for user in snapped:
      client.timeout(user, 1)
      time.sleep(1 / 30)

