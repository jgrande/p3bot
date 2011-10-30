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

import scripts.autoresponse
import p3bot
import p3bot_testcase

class TestAutoResponseScript(p3bot_testcase.P3BotTestCase):

  def setUp(self):
    p3bot_testcase.P3BotTestCase.setUp(self)
    self._script = scripts.autoresponse.init(self.bot)

  def test_set_and_get(self):
    self.bot.expect_set_data(self._script.get_name(), 'hola', 'chau')
    self.bot.expect_get_data(self._script.get_name(), 'hola')
    self.assertEqual('person, ok', self._script.execute('person', 'bot, cuando te digan "hola" responde "chau"'))
    self.assertEqual('chau', self._script.execute('person', 'bot, hola'))

  def test_del(self):
    self.bot.expect_set_data(self._script.get_name(), 'hola', 'chau')
    self.bot.expect_get_data(self._script.get_name(), 'hola')
    self.bot.expect_set_data(self._script.get_name(), 'hola', None)
    self.bot.expect_get_data(self._script.get_name(), 'hola')
    self.assertEqual('person, ok', self._script.execute('person', 'bot, cuando te digan "hola" responde "chau"'))
    self.assertEqual('person, ok', self._script.execute('person', 'bot, cuando te digan "hola" no respondas'))
    self.assertEqual(None, self._script.execute('person', 'bot, hola'))

  def test_del_without_adding(self):
    self.bot.expect_get_data(self._script.get_name(), 'hola')
    self.bot.expect_set_data(self._script.get_name(), 'hola', None)
    self.assertEqual('person, ok, igual no iba a responder', self._script.execute('person', 'bot, cuando te digan "hola" no respondas'))

