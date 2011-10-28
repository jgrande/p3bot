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
import os

if __name__=='__main__':
  sys.path.append(os.path.abspath('src/main/python'))
  sys.path.append(os.path.abspath('src/test/python'))
  os.chdir('src/test/python')

  import sys
  import unittest
  import test_p3bot
  import test_helloworldscript
  import test_portensebienscript
  import test_timezonescript

  suite = unittest.TestSuite()
  loader = unittest.TestLoader()

  suite.addTests(loader.loadTestsFromTestCase(test_p3bot.TestP3Bot))
  suite.addTests(loader.loadTestsFromTestCase(test_timezonescript.TestTimeZoneScript))
  suite.addTests(loader.loadTestsFromTestCase(test_portensebienscript.TestPortenseBienScript))
  suite.addTests(loader.loadTestsFromTestCase(test_helloworldscript.TestHelloWorldScript))

  unittest.TextTestRunner(verbosity=2).run(suite)
  
