#!/bin/python

# --------------------------------------
# sgyacc.py
""" Parser for SGF """
# --------------------------------------

import ply.yacc as yacc

from sgflex import tokens
from astNode import ASTNode, Property

def p_tree(p):
    '''tree : LPAREN node RPAREN
            | LPAREN tree RPAREN'''
    p[0] = p[2]

def p_node_sequence(p):
    '''node : node node'''
    p[1].addToSequence(p[2])
    p[0] = p[1]

def p_node_tree(p):
    '''node : node tree'''
    p[1].children.append(p[2])
    p[0] = p[1]

def p_node(p):
    'node : SCOLON'
    p[0] = ASTNode()

def p_node_prop(p):
    'node : node property'
    p[1].props[p[2].name] = p[2].value
    p[0] = p[1]

def p_property(p):
    'property : PROPID PROPVALUE'
    p[0] = Property(p[1], p[2])

def p_property_value(p):
    'property : property PROPVALUE'
    p[1].addValue(p[2])
    p[0] = p[1]

def p_error(_):
    """Error rule for syntax errors"""
    print("Syntax error in input!")

# Build the parser
parser = yacc.yacc()

while True:
    try:
        s = input('calc > ')
    except EOFError:
        break
    if not s:
        continue
    result = parser.parse(s)
    print(result.toString())
