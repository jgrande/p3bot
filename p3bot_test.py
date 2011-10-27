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

from p3bot import *
import sys

def assert_equals(arg1, arg2):
  if arg1 != arg2:
    print 'Test error: expected <%s> but found <%s>' % ( arg1, arg2 ) 
    sys.exit(1)

def test_IrcCommand():
  cmd = IrcCommand(':test_nick!test_user@test_host TESTCMD #test_channel test_param :this is a test message')
  assert_equals('TESTCMD', cmd.get_cmd_name())
  assert_equals('#test_channel', cmd.get_param(0))
  assert_equals('test_param', cmd.get_param(1))
  assert_equals('this is a test message', cmd.get_param(2))
  assert_equals('test_nick', cmd.get_user().get_nick())
  assert_equals('test_user', cmd.get_user().get_user())
  assert_equals('test_host', cmd.get_user().get_host())

def test_FileIrcCommandSource():
  src = FileIrcCommandSource('test_cmds.txt')
  cmd = src.next()
  assert_equals('TESTCMD', cmd.get_cmd_name())
  assert_equals('#test_channel', cmd.get_param(0))
  assert_equals('test_param', cmd.get_param(1))
  assert_equals('this is a test message', cmd.get_param(2))
  assert_equals('test_nick', cmd.get_user().get_nick())
  assert_equals('test_user', cmd.get_user().get_user())
  assert_equals('test_host', cmd.get_user().get_host())
  cmd = src.next()
  assert_equals(None, cmd)

def test_notice():
  cmd = IrcCommand(':card.freenode.net NOTICE * :*** Looking up your hostname...')
  assert_equals('NOTICE', cmd.get_cmd_name())
  assert_equals('*', cmd.get_param(0))
  assert_equals('*** Looking up your hostname...', cmd.get_param(1))
  assert_equals('card.freenode.net', cmd.get_user().get_nick())
  assert_equals(None, cmd.get_user().get_user())
  assert_equals(None, cmd.get_user().get_host())

if __name__=='__main__':
  test_IrcCommand()
  test_FileIrcCommandSource()
  test_notice()

