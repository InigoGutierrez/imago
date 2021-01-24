#!/bin/python

# --------------------------------------
# sgflex.py
""" Tokenizer for SGF """
# --------------------------------------

import ply.lex as lex

# List of token names
tokens = (
    'LPAREN',
    'RPAREN',
    'SCOLON',
    'LSQBRACKET',
    'RSQBRACKET',
    'PROPID',
    'UCLETTER',
    'DIGIT',
    'NUMBER',
    'REAL',
    'DOUBLE',
    'COLOR',
    'PROPVALUE'
)

# Regular expression rules for simple tokens

t_LPAREN = r'\('
t_RPAREN = r'\)'
t_SCOLON = r';'
t_LSQBRACKET = r'\['
t_RSQBRACKET = r'\]'
t_PROPID = r'[A-Z][A-Z]?'
t_UCLETTER = r'[A-Z]'
t_DIGIT = r'[0-9]'
t_COLOR = r'[BW]'

def t_NUMBER(t):
    r'[+-]?[0-9]+'
    t.value = int(t.value)
    return t

def t_REAL(t):
    r'[+-]?[0-9]+\.[0-9]+'
    t.value = int(t.value)
    return t

def t_DOUBLE(t):
    r'[12]'
    t.value = int(t.value)
    return t

def t_PROPVALUE(t):
    r'\[[^\]]*\]'
    t.value = t.value.strip('[').strip(']')
    return t

# Rule to track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore = ' \t'

def t_error(t):
    """Error handling rule"""
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

#data='''
#B[aa  ]
#W[AB]W[ab]
#B[bb]
#'''

lexer = lex.lex()
#lexer.input(data)

#for token in lexer:
#    print(token)
