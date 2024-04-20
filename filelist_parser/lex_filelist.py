import ply.lex as lex

reserved = {
    '-f' : 'SHORT_F',
    '-F' : 'SHORT_UPPER_F',
    '-y' : 'SHORT_Y',
    '--top' : 'LONG_TOP',
    '--top-module' : 'LONG_TOP_MODULE',
    '+define' : 'PLUS_DEFINE'
}

tokens = [
    'SPACES',
    'SHORT_D',
    'SHORT_F',
    'SHORT_UPPER_F',
    'SHORT_I',
    'SHORT_Y',
    'LONG_TOP',
    'LONG_TOP_MODULE',
    'PLUS_DEFINE',
    'INCDIR',
    'VARIABLE',
    'PLUS_IDENTIFIER',
    'IDENTIFIER',
    'PLUS',
#   'MINUS',
    'EQUAL',
#   'LPAREN',
#   'RPAREN',
#   'LCURLY',
#   'RCURLY',
#   'DOLLER',
]

t_SPACES = r'[\s\t]+'
t_PLUS = r'\+'
# t_MINUS = r'-'
t_EQUAL = r'='
# t_LPAREN = r'\('
# t_RPAREN = r'\)'
# t_LCURLY = r'\{'
# t_RCURLY = r'\}'
# t_DOLLER = r'\$'

# t_ignore = ' \t'
t_ignore_COMMENT = r'\#.*'

def t_SHORT_D(t):
    r'-D'
    return t

def t_SHORT_I(t):
    r'-I'
    return t

def t_INCDIR(t):
    r'incdir'
    return t

def t_VARIABLE(t):
    r'\$[({]?[a-zA-Z0-9_-]+[})]?'
    return t

def t_IDENTIFIER(t):
    # r'([a-zA-Z0-9_]|[!"#$%&\'\(\)\*\+,-\./:;<=>?@\[\\\]\\^`\{|\}~]){2,}'
    r'([a-zA-Z_]|[!"#%&\'\*,-\./:;<>?@\[\\\]\\^`|~])([a-zA-Z0-9_]|[!"#%&\'\*\+,-\./:;<>?@\[\\\]\\^`|~])+'
    t.type = reserved.get(t.value,'IDENTIFIER')
    return t

def t_newline(t):
    r"""\n+"""
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(t)

lexer = lex.lex()
