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

from p3bot import *
import unittest
import shutil
import os
import test_scripts

class TestP3Bot(unittest.TestCase):

  def test_IrcCommand(self):
    cmd = IrcCommand(':test_nick!test_user@test_host TESTCMD #test_channel test_param :this is a test message')
    self.assertEqual('TESTCMD', cmd.get_cmd_name())
    self.assertEqual('#test_channel', cmd.get_param(0))
    self.assertEqual('test_param', cmd.get_param(1))
    self.assertEqual('this is a test message', cmd.get_param(2))
    self.assertEqual('test_nick', cmd.get_user().get_nick())
    self.assertEqual('test_user', cmd.get_user().get_user())
    self.assertEqual('test_host', cmd.get_user().get_host())

  def test_FileIrcCommandSource(self):
    src = FileIrcCommandSource('test_cmds.txt')
    cmd = src.next()
    self.assertEqual('TESTCMD', cmd.get_cmd_name())
    self.assertEqual('#test_channel', cmd.get_param(0))
    self.assertEqual('test_param', cmd.get_param(1))
    self.assertEqual('this is a test message', cmd.get_param(2))
    self.assertEqual('test_nick', cmd.get_user().get_nick())
    self.assertEqual('test_user', cmd.get_user().get_user())
    self.assertEqual('test_host', cmd.get_user().get_host())
    cmd = src.next()
    self.assertEqual(None, cmd)

  def test_notice(self):
    cmd = IrcCommand(':card.freenode.net NOTICE * :*** Looking up your hostname...')
    self.assertEqual('NOTICE', cmd.get_cmd_name())
    self.assertEqual('*', cmd.get_param(0))
    self.assertEqual('*** Looking up your hostname...', cmd.get_param(1))
    self.assertEqual('card.freenode.net', cmd.get_user().get_nick())
    self.assertEqual(None, cmd.get_user().get_user())
    self.assertEqual(None, cmd.get_user().get_host())

  def test_load_scripts(self):
    loader = ScriptsLoader(test_scripts)
    self.assertEqual(0, len(loader.scripts))
    loader.load_scripts('')
    self.assertEqual(2, len(loader.scripts))
    self.assertEqual('script1', loader.scripts[0].handle(None))
    self.assertEqual('script2', loader.scripts[1].handle(None))

  def test_reload_scripts(self):
    try:
      loader = ScriptsLoader(test_scripts)
      self.assertEqual(0, len(loader.scripts))
      loader.load_scripts('')
      self.assertEqual(2, len(loader.scripts))
      
      shutil.copyfile('test_scripts/script3.py.a', 'test_scripts/script3.py')
      loader.clear_scripts()
      loader.load_scripts('')
      self.assertEqual(3, len(loader.scripts))
      self.assertTrue('script3.a' in [s.handle(None) for s in loader.scripts])
      self.assertTrue('script3.b' not in [s.handle(None) for s in loader.scripts])

      shutil.copyfile('test_scripts/script3.py.b', 'test_scripts/script3.py')
      os.remove('test_scripts/script3.pyc')
      loader.clear_scripts()
      loader.load_scripts('')
      self.assertEqual(3, len(loader.scripts))
      self.assertTrue('script3.a' not in [s.handle(None) for s in loader.scripts])
      self.assertTrue('script3.b' in [s.handle(None) for s in loader.scripts])
    finally:
      if os.path.exists('test_scripts/script3.py'):
        os.remove('test_scripts/script3.py')

