#!/usr/bin/python
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

import sys

NICKNAME = 'p3bot_dev'
USERNAME = 'p3bot_dev'
REALNAME = 'Plugtree Bot Dev'

if __name__ == '__main__':
  sys.path.append('src/main/python')
  from p3bot import P3Bot
  P3Bot(REALNAME, NICKNAME, USERNAME).run()
  
