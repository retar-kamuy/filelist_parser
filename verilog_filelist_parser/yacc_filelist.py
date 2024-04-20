import os
import re
from typing import Any

import ply.yacc as yacc
from lex_filelist import tokens

def p_command(p):
    """command : arguments"""
    p[0] = {'tag': 'kFilelistDeclaration', 'children': p[1]}

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
        # print(p[1])
        None
    else:
        p[0] = {
            'tag': 'kPositionalArgument',
            'children': [p[1]],
        }

def p_argument_optional(p):
    """argument : PLUS INCDIR plus_factor
                | SHORT_I factor
                | SHORT_I SPACES factor
                | SHORT_F SPACES factor
                | SHORT_Y SPACES factor
                | SHORT_UPPER_F SPACES factor"""
    # print(p[1])
    if p[1] == '+':
        p[0] = {
            'tag': 'kIncludeArgument',
            'children': [
                {
                    'tag': 'option',
                    'text': p[1] + p[2],
                },
                *p[3],
            ]
        }
    elif len(p) > 3:
        if p[1] == '-F' or p[1] == '-f':
            p[0] = {
                'tag': 'kFileArgument',
                'children': [
                    {
                        'tag': 'option',
                        'text': p[1],
                    },
                    p[3],
                ]
            }
        elif p[1] == '-y':
            p[0] = {
                'tag': 'kSearchDirectoryArgument',
                'children': [
                    {
                        'tag': 'option',
                        'text': p[1],
                    },
                    p[3],
                ]
            }
        else:
            p[0] = {
                'tag': 'kIncludeArgument',
                'children': [
                    {
                        'tag': 'option',
                        'text': p[1],
                    },
                    p[3],
                ]
            }
    else:
        if p[1] == '-F' or p[1] == '-f':
            p[0] = {
                'tag': 'kFileArgument',
                'children': [
                    {
                        'tag': 'option',
                        'text': p[1],
                    },
                    p[2],
                ]
            }
        elif p[1] == '-y':
            p[0] = {
                'tag': 'kSearchDirectoryArgument',
                'children': [
                    {
                        'tag': 'option',
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
                        'tag': 'option',
                        'text': p[1],
                    },
                    p[2],
                ]
            }

def p_plus_factor_identifier(p):
    """plus_factor : PLUS IDENTIFIER plus_factor
                   | PLUS IDENTIFIER"""
    # print(p[1])
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

def p_factor_identifier(p):
    """factor : variable factor
              | IDENTIFIER factor
              | variable
              | IDENTIFIER"""
    # print(p[1])
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

def get_result(data: str) -> Any:
    return yacc.parse(data)
