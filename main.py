# -*- coding: utf-8 -*-
import ply.lex as lex
import ply.yacc as yacc
from interpreter import Interpreter
from PLexer import *
from ParserL import *
import sys

def main():
    lexer = lex.lex()
    parser = yacc.yacc()
    filename = sys.argv[1]
    file = open(filename, "r")
    result = parser.parse(file.read())
    interpreter = Interpreter()
    for stmt in result[1]:
        interpreter.execute(stmt)

if __name__ == "__main__":
    main()