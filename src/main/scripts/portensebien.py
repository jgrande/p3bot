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

