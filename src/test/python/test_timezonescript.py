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

import scripts.timezone
import p3bot
import unittest

class TestTimeZoneScript(unittest.TestCase):

  def setUp(self):
    self._script = scripts.timezone.init('bot')

  def test_basic(self):
     self.assertEqual('person, no conozco el huso horario ABC', self._script.handle(p3bot.IrcCommand(':person PRIVMSG #test :bot,convertime 3:30am pdt a abc')))
     self.assertEqual('person, no conozco el huso horario ABC', self._script.handle(p3bot.IrcCommand(':person PRIVMSG #test :bot,convertime 3:30am abc a local')))
     self.assertEqual('person, no entiendo la hora, hour must be in 0..23', self._script.handle(p3bot.IrcCommand(':person PRIVMSG #test :bot,convertime 93:30am pdt a local')))
     self.assertEqual('person, 06:30 AM ART', self._script.handle(p3bot.IrcCommand(':person PRIVMSG #test :bot,convertime 2:30am pdt a local')))
     self.assertEqual('person, 06:30 AM ART', self._script.handle(p3bot.IrcCommand(':person PRIVMSG #test :bot,convertime 2:30 am pdt a local')))
     self.assertEqual('person, 06:30 AM ART', self._script.handle(p3bot.IrcCommand(':person PRIVMSG #test :bot, convertime 2:30 am pdt a local')))
     self.assertEqual('person, 06:30 AM ART', self._script.handle(p3bot.IrcCommand(':person PRIVMSG #test :bot convertime 2:30 am pdt a local')))
     self.assertEqual('person, 06:30 AM ART', self._script.handle(p3bot.IrcCommand(':person PRIVMSG #test :bot convertime 2:30 am PDT a local')))
     self.assertEqual('person, 06:30 AM ART', self._script.handle(p3bot.IrcCommand(':person PRIVMSG #test :bot convertime 2:30 AM PDT a local')))
     self.assertEqual('person, 06:30 PM ART', self._script.handle(p3bot.IrcCommand(':person PRIVMSG #test :bot convertime 2:30 PM PDT a local')))
     self.assertEqual('person, 06:30 PM ART', self._script.handle(p3bot.IrcCommand(':person PRIVMSG #test :bot convertime 14:30 PDT a local')))
     self.assertEqual('person, 03:30 PM ART', self._script.handle(p3bot.IrcCommand(':person PRIVMSG #test :bot convertime 14:30 EDT a local')))
     self.assertEqual('person, 10:30 AM PDT', self._script.handle(p3bot.IrcCommand(':person PRIVMSG #test :bot convertime 14:30 local a PDT')))

