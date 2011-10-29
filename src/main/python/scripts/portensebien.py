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
  print 'Initializing script portensebien.py'
  return PortenseBienScript(bot)

class PortenseBienScript:
  def __init__(self, bot):
    self._pat = re.compile('^%s[, ] *deciles que se porten bien$' % bot.get_nick().lower())

  def execute(self, src, msg):
    m = self._pat.match(msg.lower())
    if m != None:
      return 'chicos, portense bien'

    return None

