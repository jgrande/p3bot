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

