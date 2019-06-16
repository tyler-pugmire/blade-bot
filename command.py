from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from enum import Enum

class Permissions(Enum):
  broadcaster = 0
  moderators = 1
  vips = 2
  viewers = 3


class Command(ABC):
  def __init__(self, name, cooldown, permission):
    super().__init__()
    self._name = name
    self._cooldown = cooldown
    self._last_use = 0
    self._permission = permission
    
  def try_run(self, client, user, msg):
    if not self.__on_cooldown and self.__has_permission(client, user):
      self._last_command_usage = datetime.now()
      return self.run(client, user, msg)
    else:
      return None

  @abstractmethod
  def run(self, client, user, msg): pass

  @property
  def __on_cooldown(self): 
    return datetime.now() - self._last_use <= self._cooldown

  def __has_permission(self, client, user):
    if(user == "tylerex"):
      return True

    all_veiwers = client.get_names()["chatters"]
    if self._permission == Permissions.broadcaster:
      return user in all_veiwers["broadcaster"]
    elif self._permission == Permissions.moderators:
      return user in all_veiwers["broadcaster"] or user in all_veiwers["moderators"]
    elif self._permission == Permissions.vips:
      return user in all_veiwers["broadcaster"] or user in all_veiwers["moderators"] or user in all_veiwers["vips"]
    elif self._permission == Permissions.viewers:
      return True
    else:
      return False
  
