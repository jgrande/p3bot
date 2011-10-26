# -*- coding: utf-8 -*-

import re

_nick = ''
_greeting_pat = None

def init(nick):
  global _nick, _greeting_pat
  print 'Initializing script helloworld.py'
  _nick = nick
  _greeting_pat = re.compile('^[Hh]ello %s$' % nick)
  
def handle(cmd):
  if cmd[1] == 'PRIVMSG':
    m = _greeting_pat.match(cmd[2][1])
    if m != None:
      return 'Hello %s' % cmd[0][0]

  return None
  
