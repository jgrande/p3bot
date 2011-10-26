# -*- coding: utf-8 -*-

import re
import dateutil.tz
import dateutil.parser
import datetime

_nick = ''
_pat = None
_tzs = { 'PDT': dateutil.tz.gettz('US/Pacific'),
         'EDT': dateutil.tz.gettz('US/Eastern'),
         'MDT': dateutil.tz.gettz('US/Mountain'),
         'CDT': dateutil.tz.gettz('US/Central'),
         'LOCAL': dateutil.tz.gettz('America/Argentina/Buenos Aires'),
       }

def init(nick):
  global _nick, _pat
  print 'Initializing script timezone.py'
  _nick = nick
  _pat = re.compile('^%s[, ]? *CONVERTIME +(\\d?\\d:\\d?\\d( ?[AP]M)? ([^ ]+)) +A +([^ ]+)$' % nick.upper())
  
def handle(cmd):
  global _tzs
  
  if cmd[1] == 'PRIVMSG':
    m = _pat.match(cmd[2][1].upper())
    if m != None:
      time_str = m.group(1)
      origtz = m.group(3)
      desttz = m.group(4)
      
      if origtz not in _tzs:
        return '%s, no conozco el huso horario %s' % (cmd[0][0], origtz)
        
      if desttz not in _tzs:
        return '%s, no conozco el huso horario %s' % (cmd[0][0], desttz)
      
      try:
        time = dateutil.parser.parse(time_str, tzinfos=_tzs)
      except ValueError as e:
        return '%s, no entiendo la hora, %s' % (cmd[0][0], e)
      
      if time == None:
        return 'No entiendo la hora %s' % time_str
      
      desttime = time.astimezone(_tzs[desttz])
      return '%s, %s' % (cmd[0][0], desttime.strftime('%I:%M %p %Z'))

  return None

if __name__ == '__main__':
  init('bot')
  print 'Running tests...'
  assert handle([ ['person'], 'PRIVMSG', ['#test', 'bot,convertime 3:30am pdt a abc'] ]) == 'person, no conozco el huso horario ABC'
  assert handle([ ['person'], 'PRIVMSG', ['#test', 'bot,convertime 3:30am abc a local'] ]) == 'person, no conozco el huso horario ABC'
  assert handle([ ['person'], 'PRIVMSG', ['#test', 'bot,convertime 93:30am pdt a local'] ]) == 'person, no entiendo la hora, hour must be in 0..23'
  assert handle([ ['person'], 'PRIVMSG', ['#test', 'bot,convertime 2:30am pdt a local'] ]) == 'person, 06:30 AM ART'
  assert handle([ ['person'], 'PRIVMSG', ['#test', 'bot,convertime 2:30 am pdt a local'] ]) == 'person, 06:30 AM ART'
  assert handle([ ['person'], 'PRIVMSG', ['#test', 'bot, convertime 2:30 am pdt a local'] ]) == 'person, 06:30 AM ART'
  assert handle([ ['person'], 'PRIVMSG', ['#test', 'bot convertime 2:30 am pdt a local'] ]) == 'person, 06:30 AM ART'
  assert handle([ ['person'], 'PRIVMSG', ['#test', 'bot convertime 2:30 am PDT a local'] ]) == 'person, 06:30 AM ART'
  assert handle([ ['person'], 'PRIVMSG', ['#test', 'bot convertime 2:30 AM PDT a local'] ]) == 'person, 06:30 AM ART'
  assert handle([ ['person'], 'PRIVMSG', ['#test', 'bot convertime 2:30 PM PDT a local'] ]) == 'person, 06:30 PM ART'
  assert handle([ ['person'], 'PRIVMSG', ['#test', 'bot convertime 14:30 PDT a local'] ]) == 'person, 06:30 PM ART'
  assert handle([ ['person'], 'PRIVMSG', ['#test', 'bot convertime 14:30 EDT a local'] ]) == 'person, 03:30 PM ART'
  assert handle([ ['person'], 'PRIVMSG', ['#test', 'bot convertime 14:30 local a PDT'] ]) == 'person, 10:30 AM PDT'
  print 'Tests OK'
  
