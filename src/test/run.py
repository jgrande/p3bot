import unittest

import test_p3bot
import test_helloworldscript
import test_portensebienscript
import test_timezonescript

if __name__=='__main__':
  suite = unittest.TestSuite()
  loader = unittest.TestLoader()

  suite.addTests(loader.loadTestsFromTestCase(test_p3bot.TestP3Bot))
  suite.addTests(loader.loadTestsFromTestCase(test_timezonescript.TestTimeZoneScript))
  suite.addTests(loader.loadTestsFromTestCase(test_portensebienscript.TestPortenseBienScript))
  suite.addTests(loader.loadTestsFromTestCase(test_helloworldscript.TestHelloWorldScript))

  unittest.TextTestRunner(verbosity=2).run(suite)

