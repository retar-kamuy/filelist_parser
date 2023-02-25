import os
import sys
import io as StringIO
import ply.lex as lex
sys.path.append(os.path.join(os.path.dirname(__file__), '../verilog_filelist_parser'))

from verilog_filelist_parser import lex_filelist
import unittest

def check_expected(result, expected, contains=False):
    if sys.version_info[0] >= 3:
        if isinstance(result,str):
            result = result.encode('ascii')
        if isinstance(expected,str):
            expected = expected.encode('ascii')
    resultlines = result.splitlines()
    expectedlines = expected.splitlines()

    if len(resultlines) != len(expectedlines):
        return False

    for rline,eline in zip(resultlines,expectedlines):
        if contains:
            if eline not in rline:
                return False
        else:
            if not rline.endswith(eline):
                return False
    return True

class Test_Lex(unittest.TestCase):
    def setUp(self):
        sys.stderr = StringIO.StringIO()
        sys.stdout = StringIO.StringIO()

    def tearDown(self):
        sys.stderr = sys.__stderr__
        sys.stdout = sys.__stdout__

    def test_variable(self):
        lex.lex(module=lex_filelist)
        data = '$OS path1/$OS $OS/path2 ${OS} path3/${OS}/path4 $(OS)'
        result = lex.runmain(data=data)
        result = sys.stdout.getvalue()
        self.assertTrue(check_expected(result,
            "(VARIABLE,'$OS',1,0)\n"
            "(IDENTIFIER,'path1/',1,4)\n"
            "(VARIABLE,'$OS',1,10)\n"
            "(VARIABLE,'$OS',1,14)\n"
            "(IDENTIFIER,'/path2',1,17)\n"
            "(VARIABLE,'${OS}',1,24)\n"
            "(IDENTIFIER,'path3/',1,30)\n"
            "(VARIABLE,'${OS}',1,36)\n"
            "(IDENTIFIER,'/path4',1,41)\n"
            "(VARIABLE,'$(OS)',1,48)"
        ))

    def test_positional(self):
        lex.lex(module=lex_filelist)
        data = 'multiple_-y_no_optional multiple_p2 multiple_path3'

        #data = '''
#src/test+test.sv +define+macro1+macro2 -y src/test+test-Itest +incdir+tb1 +incdir+tb2 -Iinc -Ddef
#'''
        result = lex.runmain(data=data)
        result = sys.stdout.getvalue()
        expects = data.split(' ')
        self.assertTrue(check_expected(result,
            f"(IDENTIFIER,'{expects[0]}',1,0)\n"
            f"(IDENTIFIER,'{expects[1]}',1,{len(expects[0])+1})\n"
            f"(IDENTIFIER,'{expects[2]}',1,{len(expects[0])+len(expects[1])+2})"
        ))

    def test_optional_short_f(self):
        lex.lex(module=lex_filelist)
        data = '-f path-f_no_optional -f_no_optional'
        result = lex.runmain(data=data)
        result = sys.stdout.getvalue()
        expects = data.split(' ')
        self.assertTrue(check_expected(result,
            f"(SHORT_F,'{expects[0]}',1,0)\n"
            f"(IDENTIFIER,'{expects[1]}',1,{len(expects[0])+1})\n"
            f"(SHORT_F,'{expects[2][:2]}',1,{len(expects[0])+len(expects[1])+2})\n"
            f"(IDENTIFIER,'{expects[2][2:]}',1,{len(expects[0])+len(expects[1])+len(expects[2][:2])+2})"
        ))

    def test_optional_short_y(self):
        lex.lex(module=lex_filelist)
        data = '-y path-y_no_optional -y_no_optional'
        result = lex.runmain(data=data)
        result = sys.stdout.getvalue()
        expects = data.split(' ')
        self.assertTrue(check_expected(result,
            f"(SHORT_Y,'{expects[0]}',1,0)\n"
            f"(IDENTIFIER,'{expects[1]}',1,{len(expects[0])+1})\n"
            f"(SHORT_Y,'{expects[2][:2]}',1,{len(expects[0])+len(expects[1])+2})\n"
            f"(IDENTIFIER,'{expects[2][2:]}',1,{len(expects[0])+len(expects[1])+len(expects[2][:2])+2})"
        ))

    def test_optional_long_top(self):
        lex.lex(module=lex_filelist)
        data = '--top module--top-no-optional --topmodule'
        result = lex.runmain(data=data)
        result = sys.stdout.getvalue()
        expects = data.split(' ')
        self.assertTrue(check_expected(result,
            f"(LONG_TOP,'{expects[0]}',1,0)\n"
            f"(IDENTIFIER,'{expects[1]}',1,{len(expects[0])+1})\n"
            f"(LONG_TOP,'{expects[2][:5]}',1,{len(expects[0])+len(expects[1])+2})\n"
            f"(IDENTIFIER,'{expects[2][5:]}',1,{len(expects[0])+len(expects[1])+len(expects[2][:5])+2})"
        ))

if __name__ == '__main__':
    unittest.main()
