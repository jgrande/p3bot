#!/usr/bin/python
# -*- coding: utf-8 -*-

import socket
import re
import os
import imp

HOST = 'irc.freenode.net'
PORT = 8001
NICK = 'p3bot'
USERNAME = 'jgrande'
REALNAME = 'Plugtree Bot'
CHANNEL = '#plugtree'
SCRIPTSDIR = 'scripts'

cmd_pat = re.compile(r'^(:[^ ]+ +)?([a-zA-Z]+|\d\d\d)(.*)$')
params_pat = re.compile(r'^(( +[^: ][^ ]*)*)( +:(.*))?$')
user_pat = re.compile(r'^:([^!]+)(!([^@]+)(@([^ ]+))?)? *$')
scripts = []

def parse_cmd(cmd_str):
  m = cmd_pat.match(cmd_str)
  if m == None:
    return None
    
  return ( parse_user(m.group(1)), m.group(2), parse_params(m.group(3)) )

def parse_params(params_str):
  ret = []
  if params_str != None:
    m = params_pat.match(params_str)
    if m != None:
      # TODO ver qué pasa con split y tabs, etc
      if m.group(1) != None:
        ret = m.group(1).split()
      if m.group(4) != None:
        ret.append(m.group(4))
  return ret
  
def parse_user(user_str):
  if user_str != None:
    m = user_pat.match(user_str)
    if m != None:
      return [m.group(1), m.group(3), m.group(5)]
  return None
  
def load_scripts():
  filenames = [ fn for fn in os.listdir(SCRIPTSDIR) if fn[-3:]=='.py' ]
  for fn in filenames:
    module = imp.load_source(fn[:-3], '%s/%s'%(SCRIPTSDIR,fn))
    module.init(NICK)
    scripts.append(module)
    print 'Script %s initialized' % fn
  
if __name__ == '__main__':
  load_scripts()
  
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.connect((HOST, PORT))
  print 'Connected, registering connection...'
  
  s.sendall('NICK %s\r\n' % NICK)
  s.sendall('USER %s a b :%s\r\n' % (USERNAME, REALNAME))
  print 'Connection successfully registered'
  
  s.sendall('JOIN %s\r\n' % CHANNEL)
  print 'Channel %s successfully joined' % CHANNEL
  
  try:
    data = ''
    while True:
      data = data + s.recv(1024)
      lines = data.split('\n')
      data = lines.pop()
      for line in lines:
        line = line.rstrip()
        cmd = parse_cmd(line)
        
        if cmd[1] == 'PING':
          print 'Ping received!'
          s.sendall('PONG %s\r\n' % cmd[2][0])
        else:
          # print cmd
          for script in scripts:
            resp = script.handle(cmd)
            if resp != None:
              s.sendall('PRIVMSG %s :%s\r\n' % (CHANNEL, resp))
        
  finally:
    print 'Closing connection'
    s.close()
  
