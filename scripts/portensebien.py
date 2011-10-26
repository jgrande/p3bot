# -*- coding: utf-8 -*-

import re
from p3bot import *

def init(nick):
  print 'Initializing script portensebien.py'
  return PortenseBienScript(nick)

class PortenseBienScript:
  def __init__(self, nick):
    self._greeting_pat = re.compile('^%s[, ] *DECILES QUE SE PORTEN BIEN$' % nick.upper())

  def handle(self, cmd):
    if cmd.get_cmd_name() == 'PRIVMSG':
      m = self._greeting_pat.match(cmd.get_param(1).upper())
      if m != None:
        return 'chicos, portense bien'
    return None

if __name__ == '__main__':
  init('bot')
  print 'Running tests...'
  script = PortenseBienScript('bot')
  assert script.handle(IrcCommand(':person PRIVMSG #test :bot, deciles que se porten bien')) == 'chicos, portense bien'
  assert script.handle(IrcCommand(':person PRIVMSG #test :bot,deciles que se porten bien')) == 'chicos, portense bien'
  print 'Tests OK'

