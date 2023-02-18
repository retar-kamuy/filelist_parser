import ply.lex as lex

reserved = {
   'I'      : 'I',
   'incdir' : 'INCDIR',
   'define' : 'DEFINE',
   'f'      : 'F',
   'F'      : 'F_REL',
   'D'      : 'D',
   'top'    : 'TOP',
   'top-module' : 'TOP_MODULE',
   'y'      : 'Y',
}

tokens = [
    'STRING',
    'PLUS',
    'SHORT',
    'LONG',
    'EQUALS',
    'LPAREN',
    'RPAREN',
    'LBRACKETS',
    'RBRACKETS',
    'DOLLER',
] + list(reserved.values())

t_PLUS = r'\+'
t_SHORT = r'-'
t_LONG = r'--'
t_EQUALS = r'='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACKETS = r'\{'
t_RBRACKETS = r'\}'
t_DOLLER = r'\$'

t_ignore = ' \t'
t_ignore_COMMENT = r'\#.*'

def t_STRING(t):
    r'[^-+=(){}$\s\t]+'
    t.type = reserved.get(t.value,'STRING')
    return t

def t_newline(t):
    r"""\n+"""
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(t)

lexer = lex.lex()

data =  '''
src/test.sv +define+macro1+macro2 -f run.f ${SRC}/main.sv --top main
'''

lexer.input(data)

if __name__ == '__main__':
    while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok)
