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

def init(bot):
  print 'Initializing script timezone.py'
  return TimeZoneScript(bot)

class TimeZoneScript:
  def __init__(self, bot):
    self._pat = re.compile('^%s[, ]? *CONVERTIME +(\\d?\\d(:\\d?\\d)?( ?[AP]M)? ([^ ]+)) +A +([^ ]+)$' % bot.get_nick().upper())

  def execute(self, src, msg):
    m = self._pat.match(msg.upper())
    if m != None:
      time_str = m.group(1)
      origtz = m.group(4)
      desttz = m.group(5)
      
      if origtz not in _TZS:
        return '%s, no conozco el huso horario %s' % (src, origtz)
        
      if desttz not in _TZS:
        return '%s, no conozco el huso horario %s' % (src, desttz)
      
      try:
        time = dateutil.parser.parse(time_str, tzinfos=_TZS)
      except ValueError as e:
        return '%s, no pude leer la hora, %s' % (src, e)
      
      desttime = time.astimezone(_TZS[desttz])
      return '%s, %s' % (src, desttime.strftime('%I:%M %p %Z'))

    return None
  
