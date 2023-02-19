import ply.yacc as yacc
from lex import tokens
import random
import os

precedence = (
    ('right', 'PLUS', 'SHORT', 'LONG', 'EQUAL'),
    ('right', 'DOLLER'),
)

def p_statement_assign(p):
    """statement : factor"""
    p[0] = p[1]

# def p_statement_incdir(p):
#     """statement : PLUS INCDIR PLUS expression"""
#     p[0] = {
#         'tag': 'argumentType',
#         'text': p[4],
#     }

def p_factor_variable(p):
    '''factor : DOLLER factor
              | DOLLER LPAREN factor RPAREN
              | DOLLER LCURLY factor RCURLY'''
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
    '''factor : IDENTIFIER'''
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
    data = '$OS'
    result = yacc.parse(data)
    print("  [%s] -> " % data + str(result))