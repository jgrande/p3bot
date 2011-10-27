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

import scripts.helloworld
import p3bot
import unittest

class TestHelloWorldScript(unittest.TestCase):

  def setUp(self):
    self._script = scripts.helloworld.init('bot')

  def test_basic(self):
    self.assertEqual('hola person', self._script.handle(p3bot.IrcCommand(':person PRIVMSG #test :hola bot')))
    self.assertEqual('hello person', self._script.handle(p3bot.IrcCommand(':person PRIVMSG #test :hello bot')))
    self.assertEqual('hola person', self._script.handle(p3bot.IrcCommand(':person PRIVMSG #test :Hola bot')))
    self.assertEqual('hello person', self._script.handle(p3bot.IrcCommand(':person PRIVMSG #test :Hello bot')))
    self.assertEqual('hola person', self._script.handle(p3bot.IrcCommand(':person PRIVMSG #test :HOLA bot')))
    self.assertEqual('hello person', self._script.handle(p3bot.IrcCommand(':person PRIVMSG #test :HELLO bot')))

if __name__ == '__main__':
    unittest.main()

