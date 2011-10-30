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
from p3bot import *

def init(bot):
  print 'Initializing script autoresponse.py'
  return AutoResponseScript(bot)

class AutoResponseScript:
  def __init__(self, bot):
    self._store_pat = re.compile('^%s[ ,] *cuando te digan "(.*)" responde "(.*)"$' % bot.get_nick().lower())
    self._search_pat = re.compile('^%s[ ,] *(.*)$' % bot.get_nick().lower())
    self._del_pat = re.compile('^%s[ ,] *cuando te digan "(.*)" no respondas$' % bot.get_nick().lower())
    self._bot = bot

  def get_name(self):
    return 'AutoResponseScript'

  def execute(self, src, msg):
    msg = msg.lower()

    m = self._store_pat.match(msg)
    if m != None:
      self._bot.set_data(self.get_name(), m.group(1).strip(), m.group(2).strip())
      return '%s, ok' % src

    m = self._del_pat.match(msg)
    if m != None:
      has_key = self._bot.get_data(self.get_name(), m.group(1).strip()) != None
      response = '%s, ok' % src if has_key else '%s, ok, igual no iba a responder' % src
      self._bot.set_data(self.get_name(), m.group(1).strip(), None)
      return response

    m = self._search_pat.match(msg)
    if m != None:
      response = self._bot.get_data(self.get_name(), m.group(1).strip())
      return response

    return None

