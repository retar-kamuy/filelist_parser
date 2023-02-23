import ply.yacc as yacc
from lex import tokens
import os
import pprint

precedence = (
    ('right', 'PLUS', 'EQUAL'),
    ('right', 'DOLLER'),
)

def p_command(p):
    """command : arguments"""
    p[0] = p[1]

def p_arguments(p):
    """arguments : argument arguments
               | argument"""
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        for v in p[2:]:
            p[0] = [p[1]] + v

# def p_statement_incdir(p):
#     """statement : PLUS INCDIR PLUS expression"""
#     p[0] = {
#         'tag': 'argumentType',
#         'text': p[4],
#     }

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
    """argument : SHORT_I
                | SHORT_Y factor
                | PLUS_INCDIR plus_factor"""
    if len(p) == 2:
        p[0] = {
            'tag': 'kIncludeArgument',
            'children': [
                {
                    'tag': 'keyword',
                    'text': p[1][:2],
                },
                {
                    'tag': 'identifier',
                    'text': p[1][2:],
                }
            ]
        }
    elif p[1] == '-y':
        print(p[1])
        p[0] = {
            'tag': 'kIncludeArgument',
            'children': [
                {
                    'tag': 'kArgumentType',
                    'text': p[1],
                },
                p[2],
            ]
        }
    else:
        p[0] = {
            'tag': 'kIncludeArgument',
            'children': [
                {
                    'tag': 'kArgumentType',
                    'text': p[1],
                },
                *p[2],
            ]
        }

def p_plus_factor_identifier(p):
    """plus_factor : PLUS factor plus_factor
                   | PLUS factor"""
    if len(p) == 3:
        p[0] = [
            {
                'tag': 'identifier',
                'text': p[2],
            }
        ]
    else:
        p[0] = [
            {
                'tag': 'identifier',
                'text': p[2],
            },
            *p[3],
        ]

def p_factor_variable(p):
    """factor : DOLLER factor
              | DOLLER LPAREN factor RPAREN
              | DOLLER LCURLY factor RCURLY"""
    if p[2] == '(' or p[2] == '{':
        p[0] = {
            'tag': p[3]['tag'],
            'text': os.environ[p[3]['text']],
        }
    else:
        p[0] = {
            'tag': p[2]['tag'],
            'text': os.environ[p[2]['text']],
        }

def p_factor_identifier(p):
    """factor : IDENTIFIER"""
    p[0] = {
        'tag': 'identifier',
        'text': p[1],
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
# src/test-Itest.sv src/test+test.sv +define+macro1+macro2 -f run.f $(TB)/top_tb.sv ${SRC}/main.sv --top main src/-ysrc -y src +incdir+tb1 +incdir+tb2 -Iinc -Ddef
# '''
    # data = '$OS -y src/test+test-Itest +incdir+tb1+tb2 +incdir+src1 -Iinclude'
    data = '$OS -y src/test'
    result = yacc.parse(data)
    print("  [%s] -> " % data)
    pprint.pprint(result, indent=4)