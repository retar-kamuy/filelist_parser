import ply.lex as lex

tokens = [
    'SHORT_F',
    'SHORT_F_REL',
    'SHORT_Y',
    'SHORT_I',
    'SHORT_D',
    'LONG_TOP',
    'LONG_TOP_MODULE',
    'IDENTIFIER',
    'PLUS_INCDIR',
    'PLUS_DEFINE',
    'PLUS',
#   'SHORT',
#   'LONG',
    'EQUAL',
    'LPAREN',
    'RPAREN',
    'LCURLY',
    'RCURLY',
    'DOLLER',
    'SPACE',
    'TAB',
]

t_SPACE = r'\s'
t_TAB = r'\t'
# t_SHORT = r'-'
t_PLUS = r'\+'
t_EQUAL = r'='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LCURLY = r'\{'
t_RCURLY = r'\}'
t_DOLLER = r'\$'
# t_LONG = r'--'
t_LONG_TOP = r'--top'
t_LONG_TOP_MODULE = r'--top-module'
t_SHORT_F = r'-f'
t_SHORT_F_REL = r'-F'
t_SHORT_Y = r'-y'
t_SHORT_I = r'-I'
t_SHORT_D = r'-D'
t_PLUS_INCDIR = r'\+incdir'
t_PLUS_DEFINE = r'\+define'

t_ignore = ' \t'
t_ignore_COMMENT = r'\#.*'

def t_IDENTIFIER(t):
    r'[^-+=$(){}\s\t][^+=$(){}\s\t]*'
    return t

def t_newline(t):
    r"""\n+"""
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(t)

lexer = lex.lex()

data = '''
src/test-Itest.sv src/test+test.sv +define+macro1+macro2 -f run.f $(TB)/top_tb.sv ${SRC}/main.sv --top main src/-ysrc -y src -y src/test+test-Itest +incdir+tb1 +incdir+tb2 -Iinc -Ddef
'''

lexer.input(data)

if __name__ == '__main__':
    while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok)
