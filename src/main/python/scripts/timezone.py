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

_TZS = { 'PST': dateutil.tz.gettz('US/Pacific'),
         'EST': dateutil.tz.gettz('US/Eastern'),
         'MST': dateutil.tz.gettz('US/Mountain'),
         'CST': dateutil.tz.gettz('US/Central'),
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
  
