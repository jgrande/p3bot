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

import unittest
import p3bot

class MockSocket:
  def connect(self, args):
    pass

  def close(self):
    pass

  def sendall(self, data):
    pass

  def recv(self, size):
    return None

class MockShelf(dict):

  def __init__(self, test):
    dict.__init__(self)
    self._expects = None
    self._test = test

  def close(self):
    if self._expects != None:
      self._test.assertEqual(0, len(self._expects), msg='%s more operations expected' % len(self._expects))

  def expect_set(self, key, val):
    if self._expects == None:
      self._expects = []

    self._expects.append(('set', key, val))

  def expect_get(self, key):
    if self._expects == None:
      self._expects = []

    self._expects.append(('get', key))

  def expect_del(self, key):
    if self._expects == None:
      self._expects = []

    self._expects.append(('del', key))

  def __getitem__(self, key):
    if self._expects != None:
      self._test.assertTrue(len(self._expects)>0, msg='Unexpected operation')
      next = self._expects.pop(0)
      self._test.assertEqual('get', next[0])
      self._test.assertEqual(key, next[1])
    return dict.__getitem__(self, key)

  def __setitem__(self, key, val):
    if self._expects != None:
      self._test.assertTrue(len(self._expects)>0, msg='Unexpected operation')
      next = self._expects.pop(0)
      self._test.assertEqual('set', next[0])
      self._test.assertEqual(key, next[1])
      self._test.assertEqual(val, next[2])
    dict.__setitem__(self, key, val)

  def __delitem__(self, key):
    if self._expects != None:
      self._test.assertTrue(len(self._expects)>0, msg='Unexpected operation')
      next = self._expects.pop(0)
      self._test.assertEqual('del', next[0])
      self._test.assertEqual(key, next[1])
    dict.__delitem__(self, key)

class MockP3Bot(p3bot.P3Bot):

  def __init__(self, test):
    p3bot.P3Bot.__init__(self, 'Test Bot', 'bot', 'user', sock=MockSocket(), shelf=MockShelf(test))

  def expect_set_data(self, script, key, val):
    key = '%s/%s' % (script,key)
    if val == None:
      self._shelf.expect_del(key)
    else:
      self._shelf.expect_set(key, val)

  def expect_get_data(self, script, key):
    key = '%s/%s' % (script, key)
    self._shelf.expect_get(key)

class P3BotTestCase(unittest.TestCase):
  
  def setUp(self):
    self.bot = MockP3Bot(self)

  def tearDown(self):
    if self.bot != None:
      self.bot.close()

