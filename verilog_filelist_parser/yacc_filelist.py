import ply.yacc as yacc
from lex_filelist import tokens
import os
import pprint
import re

def p_command(p):
    """command : arguments"""
    p[0] = p[1]

def p_arguments(p):
    """arguments : argument SPACES arguments
                 | argument SPACES
                 | argument"""
    if len(p) <= 3:
        p[0] = [p[1]]
    else:
        for v in p[3:]:
            p[0] = [p[1]] + v

def p_argument_positional(p):
    """argument : factor"""
    if len(p) != 2:
        print(p[1])
    else:
        p[0] = {
            'tag': 'kPositionalArgument',
            'children': [p[1]],
        }

def p_argument_optional(p):
    """argument : SHORT_I factor
                | SHORT_Y factor"""
    if p[1] == '+incdir':
        p[0] = {
            'tag': 'kIncludeArgument',
            'children': [
                {
                    'tag': 'keyword',
                    'text': p[1],
                },
                *p[2],
            ]
        }
    else:
        p[0] = {
            'tag': 'kIncludeArgument',
            'children': [
                {
                    'tag': 'keyword',
                    'text': p[1],
                },
                p[2],
            ]
        }

# def p_plus_factor_identifier(p):
#     """plus_factor : PLUS IDENTIFIER plus_factor
#                    | PLUS IDENTIFIER"""
#     if len(p) == 3:
#         p[0] = [
#             {
#                 'tag': 'identifier',
#                 'text': p[2],
#             }
#         ]
#     else:
#         p[0] = [
#             {
#                 'tag': 'identifier',
#                 'text': p[2],
#             },
#             *p[3],
#         ]

def p_factor_identifier(p):
    """factor : variable factor
              | IDENTIFIER factor
              | variable
              | IDENTIFIER"""
    print(p[1])
    if len(p) == 2:
        if 'tag' in p[1]:
            p[0] = {
                'tag': 'identifier',
                'text': os.environ[p[1]['text']],
            }
        else:
            p[0] = {
                'tag': 'identifier',
                'text': p[1],
            }
    else:
        if 'tag' in p[1]:
            p[0] = {
                'tag': 'identifier',
                'text': os.environ[p[1]['text']] + p[2]['text'],
            }
        else:
            p[0] = {
                'tag': 'identifier',
                'text': p[1] + p[2]['text'],
            }

def p_variable(p):
    """variable : VARIABLE"""
    if re.match(r'\$[\(\{].+[\)\}]', p[1]):
        p[0] = {
            'tag': 'variable',
            'text': p[1][2:-1],
        }
    else:
        p[0] = {
            'tag': 'variable',
            'text': p[1][1:],
        }

def p_error(p):
    print("Syntax error in input")

yacc.yacc()

# def main():
#     while True:
#         try:
#             # data = input("[DiceBot]> ")
#             data = '$OS'
#         except EOFError:
#             break
#         result = yacc.parse(data)
#         print("  [%s] -> " % data + str(result))

def main():
#     data = '''
# +define+macro1+macro2 -f run.f $(TB)/top_tb.sv ${SRC}/main.sv --top main -Ddef
# '''
#     data = '''
# $OS src/test-Itest.sv src/test+test.sv -y src/test+test-Itest +incdir+tb1+tb2 +incdir+tb1 +incdir+tb2 +incdir+src1 src/-ysrc -y src -Iinclude -Iinc
# '''

    data = '''
$(OS) $OS/main.sv src/$OS/main.sv src/${OS} src/tb/main.sv sub.sv
'''
    result = yacc.parse(data)
    print("  [%s] -> " % data)
    pprint.pprint(result, indent=4)
