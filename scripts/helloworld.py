# -*- coding: utf-8 -*-

import re
from p3bot import *

def init(nick):
  print 'Initializing script helloworld.py'
  return HelloWorldScript(nick)

class HelloWorldScript:
  def __init__(self, nick):
    self._greeting_pat = re.compile('^(HELLO|HOLA) %s$' % nick.upper())

  def handle(self, cmd):
    if cmd.get_cmd_name() == 'PRIVMSG':
      m = self._greeting_pat.match(cmd.get_param(1).upper())
      if m != None:
        return '%s %s' % ( m.group(1).lower(), cmd.get_user().get_nick() )

    return None

if __name__ == '__main__':
  init('bot')
  print 'Running tests...'
  script = HelloWorldScript('bot')
  assert script.handle(IrcCommand(':person PRIVMSG #test :hola bot')) == 'hola person'
  assert script.handle(IrcCommand(':person PRIVMSG #test :hello bot')) == 'hello person'
  assert script.handle(IrcCommand(':person PRIVMSG #test :Hola bot')) == 'hola person'
  assert script.handle(IrcCommand(':person PRIVMSG #test :Hello bot')) == 'hello person'
  assert script.handle(IrcCommand(':person PRIVMSG #test :HOLA bot')) == 'hola person'
  assert script.handle(IrcCommand(':person PRIVMSG #test :HELLO bot')) == 'hello person'
  print 'Tests OK'

