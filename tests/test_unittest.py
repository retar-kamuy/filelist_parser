import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../verilog_filelist_parser'))

from verilog_filelist_parser.yacc import main
import unittest

class Test_TestIncrementDecrement(unittest.TestCase):
    def test_increment(self):
        main()
        # self.assertEqual(inc_dec.increment(3), 4)

if __name__ == '__main__':
    unittest.main()
