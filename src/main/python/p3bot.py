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

import socket
import re
import os
import imp
import scripts

HOST = 'irc.freenode.net'
PORT = 8001
NICK = 'p3bot_dev'
USERNAME = 'p3bot_dev'
REALNAME = 'Plugtree Bot Dev'
CHANNEL = '#plugtree'
SCRIPTSDIR = 'scripts'

class IrcUser:

  def __init__(self, nick='', user='', host=''):
    self._nick = nick
    self._user = user
    self._host = host

  def __str__(self):
    return 'IrcUser(nick=%s, user=%s, host=%s)' % ( self._nick, self._user, self._host )

  def get_nick(self):
    return self._nick

  def get_user(self):
    return self._user

  def get_host(self):
    return self._host

class IrcCommand:

  _cmd_pat = re.compile(r'^(:[^ ]+ +)?([a-zA-Z]+|\d\d\d)(.*)$')

  _params_pat = re.compile(r'^(( +[^: ][^ ]*)*)( +:(.*))?$')
  
  _user_pat = re.compile(r'^:([^! ]+)(!([^@ ]+)(@([^ ]+))?)? *$')

  def __init__(self, cmd_str):
    self._user = None
    self._cmd_name = None
    self._params = []
    self._parse_cmd_str(cmd_str)

  def __str__(self):
    return 'IrcCommand(user=%s,cmd_name=%s,params=%s)' % ( self._user, self._cmd_name, self._params  )

  def get_param(self, idx):
    return self._params[idx]

  def get_cmd_name(self):
    return self._cmd_name

  def get_user(self):
    return self._user

  def _parse_cmd_str(self, cmd_str):
    m = IrcCommand._cmd_pat.match(cmd_str)
    if m == None:
      return None
      
    self._parse_user(m.group(1))
    self._cmd_name = m.group(2)
    self._parse_params(m.group(3))

  def _parse_params(self, params_str):
    if params_str != None:
      m = IrcCommand._params_pat.match(params_str)
      if m != None:
        # TOFIX maybe this is splitting not only on spaces, but on tabs and so
        if m.group(1) != None:
          self._params = m.group(1).split()
        if m.group(4) != None:
          self._params.append(m.group(4))
    
  def _parse_user(self, user_str):
    if user_str != None:
      m = IrcCommand._user_pat.match(user_str)
      if m != None:
        self._user = IrcUser(nick=m.group(1), user=m.group(3), host=m.group(5))

class IrcCommandSource:
  def next(self):
    return IrcCommand()

class FileIrcCommandSource(IrcCommandSource):

  def __init__(self, filename):
    f = open(filename, 'r')
    self._lines = f.readlines()
    f.close()

  def next(self):
    if len(self._lines)>0:
      return IrcCommand(self._lines.pop(0))
    else:
      return None

class SocketIrcCommandSource(IrcCommandSource):

  def __init__(self, socket):
    self._socket = socket
    self._data = ''
    self._lines = []

  def next(self):
    while len(self._lines)==0:
      self._data = self._data + self._socket.recv(1024)
      lines = self._data.split('\n')
      self._data = lines.pop()
      self._lines.extend(lines)

    return IrcCommand(self._lines.pop(0).rstrip())

class ScriptsLoader:

  def __init__(self, pkg):
    self.scripts = []
    self.pkg = pkg

  def load_scripts(self):
    # TODO all scripts should be called <anything>_script.py
    filenames = [ fn for fn in os.listdir(self.pkg.__path__[0]) if not fn.startswith('__') and fn.endswith('.py') ]
    for fn in filenames:
      t = imp.find_module(fn[:-3], self.pkg.__path__)
      try:
        module = imp.load_module(fn[:-3], t[0], t[1], t[2])
        script = module.init(NICK)
        self.scripts.append(script)
        print 'Script %s loaded' % fn
      except ImportError as err:
        print 'Error loading script %s: %s' % (fn, err)
      finally:
        t[0].close()

  def clear_scripts(self):
    for m in self.scripts:
      del m
    self.scripts = []

  def __iter__(self):
    return self.scripts.__iter__()
  
class P3Bot:

  def run(self):
    loader = ScriptsLoader(scripts)
    loader.load_scripts()
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    print 'Connected, registering connection...'
    
    s.sendall('NICK %s\r\n' % NICK)
    s.sendall('USER %s a b :%s\r\n' % (USERNAME, REALNAME))
    print 'Connection successfully registered'
    
    s.sendall('JOIN %s\r\n' % CHANNEL)
    print 'Channel %s successfully joined' % CHANNEL
    
    try:
      src = SocketIrcCommandSource(s)
      while True:
        cmd = src.next()
        
        if cmd.get_cmd_name() == 'PING':
          print 'Ping received!'
          s.sendall('PONG %s\r\n' % cmd.get_param(0))
        else:
          for script in loader:
            resp = script.handle(cmd)
            if resp != None:
              s.sendall('PRIVMSG %s :%s\r\n' % (CHANNEL, resp))
          
    finally:
      print 'Closing connection'
      s.close()
  