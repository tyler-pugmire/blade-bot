import socket
import string
import re
import requests

def remove_prefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix):]
    return text  # or whatever

class TwitchClient:
  def __init__(self, HOST, PORT, NICK, PASS, CHANNEL):
    self._host = HOST
    self._port = PORT
    self._nick = NICK
    self._pass = PASS
    self._channel = CHANNEL
    self.events = {}
    self.commands = {}

    self.s = socket.socket()

  def connect(self):
    self.s.connect((self._host, self._port))
    self.s.send("PASS {}\r\n".format(self._pass).encode("utf-8"))
    self.s.send("NICK {}\r\n".format(self._nick).encode("utf-8"))
    self.s.send("JOIN #{}\r\n".format(self._channel).encode("utf-8"))

    readBuffer = ""
    loading = True
    while loading:
      readBuffer = readBuffer + self.s.recv(1024).decode("utf-8")
      temp = readBuffer.split("\n")
      readBuffer = temp.pop()

      for line in temp:
        print(line)
        loading = not self.connection_complete(line)
    
    #self.send_message("Connected to chat")

  def connection_complete(self, line):
    if("End of /NAMES list" in line):
      return True
    else:
      return False

  def send_message(self, msg):
    realMsg = "PRIVMSG #" + self._channel + " :" + msg
    self.s.send("{}\r\n".format(realMsg).encode("utf-8"))

  def on(self, event, pred):
    self.events[event] = pred

  def run(self):
    running = True
    readBuffer = ""
    CHAT_MSG = re.compile(r"^:\w+!\w+@\w+.tmi.twitch.tv PRIVMSG #\w+ :")

    while running:
      readBuffer = readBuffer + self.s.recv(1024).decode("utf-8")
      temp = readBuffer.split("\r\n")
      readBuffer = temp.pop()
      
      for line in temp:
        if "PING" in line:
          self.s.send(line.replace("PING", "PONG").encode("utf-8"))
          break
        elif "!QUIT!" in line:
          self.send_message("BYE!")
          running = False
          break
        else:
          username = re.search(r"\w+", line).group(0) # return the entire match
          message = CHAT_MSG.sub("", line)
          print(message)
          if message.startswith("!"):
            message = remove_prefix(message, "!")
            split = message.split(" ")
            self.commands[split[0]].try_run(self, username, split.pop())
  
  def register_command(self, cmd):
    self.commands[cmd._name] = cmd

  def get_names(self):
    URL = "http://tmi.twitch.tv/group/user/{}/chatters".format(self._channel)
    r = requests.get(URL)
    data = r.json()
    return data
  
  def timeout(self, user, duration):
    self.send_message("/timeout {} {}".format(user, duration))

  #def do_command(self, user, cmd, args)
  #  self.commands[cmd].run(user, args)
        