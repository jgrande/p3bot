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
import p3bot_testcase

class TestTimeZoneScript(p3bot_testcase.P3BotTestCase):

  def setUp(self):
    p3bot_testcase.P3BotTestCase.setUp(self)
    self._script = scripts.timezone.init(self.bot)

  def test_basic(self):
     self.assertEqual('person, no conozco el huso horario ABC', self._script.execute('person', 'bot,convertime 3:30am pst a abc'))
     self.assertEqual('person, no conozco el huso horario ABC', self._script.execute('person', 'bot,convertime 3:30am abc a local'))
     self.assertEqual('person, no pude leer la hora, hour must be in 0..23', self._script.execute('person', 'bot,convertime 93:30am pst a local'))
     self.assertEqual('person, 06:30 AM ART', self._script.execute('person', 'bot,convertime 2:30am pst a local'))
     self.assertEqual('person, 06:30 AM ART', self._script.execute('person', 'bot,convertime 2:30 am pst a local'))
     self.assertEqual('person, 06:30 AM ART', self._script.execute('person', 'bot, convertime 2:30 am pst a local'))
     self.assertEqual('person, 06:30 AM ART', self._script.execute('person', 'bot convertime 2:30 am pst a local'))
     self.assertEqual('person, 06:30 AM ART', self._script.execute('person', 'bot convertime 2:30 am PST a local'))
     self.assertEqual('person, 06:30 AM ART', self._script.execute('person', 'bot convertime 2:30 AM PST a local'))
     self.assertEqual('person, 06:30 PM ART', self._script.execute('person', 'bot convertime 2:30 PM PST a local'))
     self.assertEqual('person, 06:30 PM ART', self._script.execute('person', 'bot convertime 14:30 PST a local'))
     self.assertEqual('person, 03:30 PM ART', self._script.execute('person', 'bot convertime 14:30 EST a local'))
     self.assertEqual('person, 10:30 AM PDT', self._script.execute('person', 'bot convertime 14:30 local a PST'))

  def test_no_minutes(self):
     self.assertEqual('person, 09:00 AM ART', self._script.execute('person', 'bot convertime 9 am local a local'))

