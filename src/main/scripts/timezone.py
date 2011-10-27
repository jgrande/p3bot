# -*- coding: utf-8 -*-

#   Copyright 2011 Juan Grande
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import re
import dateutil.tz
import dateutil.parser
import datetime
from p3bot import *

_TZS = { 'PDT': dateutil.tz.gettz('US/Pacific'),
         'EDT': dateutil.tz.gettz('US/Eastern'),
         'MDT': dateutil.tz.gettz('US/Mountain'),
         'CDT': dateutil.tz.gettz('US/Central'),
         'LOCAL': dateutil.tz.gettz('America/Argentina/Buenos Aires'),
       }

def init(nick):
  print 'Initializing script timezone.py'
  return TimeZoneScript(nick)

class TimeZoneScript:
  def __init__(self, nick):
    self._pat = re.compile('^%s[, ]? *CONVERTIME +(\\d?\\d:\\d?\\d( ?[AP]M)? ([^ ]+)) +A +([^ ]+)$' % nick.upper())

  def handle(self, cmd):
    if cmd.get_cmd_name() == 'PRIVMSG':
      m = self._pat.match(cmd.get_param(1).upper())
      if m != None:
        time_str = m.group(1)
        origtz = m.group(3)
        desttz = m.group(4)
        
        if origtz not in _TZS:
          return '%s, no conozco el huso horario %s' % (cmd.get_user().get_nick(), origtz)
          
        if desttz not in _TZS:
          return '%s, no conozco el huso horario %s' % (cmd.get_user().get_nick(), desttz)
        
        try:
          time = dateutil.parser.parse(time_str, tzinfos=_TZS)
        except ValueError as e:
          return '%s, no entiendo la hora, %s' % (cmd.get_user().get_nick(), e)
        
        if time == None:
          return 'No entiendo la hora %s' % time_str
        
        desttime = time.astimezone(_TZS[desttz])
        return '%s, %s' % (cmd.get_user().get_nick(), desttime.strftime('%I:%M %p %Z'))

    return None

if __name__ == '__main__':
  init('bot')
  print 'Running tests...'
  script = TimeZoneScript('bot')
  assert script.handle(IrcCommand(':person PRIVMSG #test :bot,convertime 3:30am pdt a abc')) == 'person, no conozco el huso horario ABC'
  assert script.handle(IrcCommand(':person PRIVMSG #test :bot,convertime 3:30am abc a local')) == 'person, no conozco el huso horario ABC'
  assert script.handle(IrcCommand(':person PRIVMSG #test :bot,convertime 93:30am pdt a local')) == 'person, no entiendo la hora, hour must be in 0..23'
  assert script.handle(IrcCommand(':person PRIVMSG #test :bot,convertime 2:30am pdt a local')) == 'person, 06:30 AM ART'
  assert script.handle(IrcCommand(':person PRIVMSG #test :bot,convertime 2:30 am pdt a local')) == 'person, 06:30 AM ART'
  assert script.handle(IrcCommand(':person PRIVMSG #test :bot, convertime 2:30 am pdt a local')) == 'person, 06:30 AM ART'
  assert script.handle(IrcCommand(':person PRIVMSG #test :bot convertime 2:30 am pdt a local')) == 'person, 06:30 AM ART'
  assert script.handle(IrcCommand(':person PRIVMSG #test :bot convertime 2:30 am PDT a local')) == 'person, 06:30 AM ART'
  assert script.handle(IrcCommand(':person PRIVMSG #test :bot convertime 2:30 AM PDT a local')) == 'person, 06:30 AM ART'
  assert script.handle(IrcCommand(':person PRIVMSG #test :bot convertime 2:30 PM PDT a local')) == 'person, 06:30 PM ART'
  assert script.handle(IrcCommand(':person PRIVMSG #test :bot convertime 14:30 PDT a local')) == 'person, 06:30 PM ART'
  assert script.handle(IrcCommand(':person PRIVMSG #test :bot convertime 14:30 EDT a local')) == 'person, 03:30 PM ART'
  assert script.handle(IrcCommand(':person PRIVMSG #test :bot convertime 14:30 local a PDT')) == 'person, 10:30 AM PDT'
  print 'Tests OK'
  
