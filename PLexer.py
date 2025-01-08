# -*- coding: utf-8 -*-
import ply.lex as lex

tokens = [
    'IDENTYFIKATOR', 'TEKST'
]

reserved = {'załóżmy' : 'ZALOZMY',
            'równe' : 'ROWNE',
            'różne' : 'ROZNE',
            'funkcja' : 'FUNKCJA',
            'dopóki' : 'DOPUKI',
            'jeżeli' : 'JEZELI',
            'wpw': 'W_PRZECIWNYM_WYPADKU',
            'przypisz' : 'PRZYPISZ',
            'wypisz' : 'WYPISZ',
            'zwróć' : 'ZWROC',
            'plus' : 'PLUS',
            'minus' : 'MINUS',
            'razy' : 'RAZY',
            'przez' : 'PODZIELONE_PRZEZ',
            'mniejsze' : 'MNIEJSZE_OD',
            'większe' : 'WIEKSZE_OD',
            'wynosi' : 'WYNOSI',
            'wpisz' : 'WPISZ',
            '[' : 'LP',
            ']' : 'RP',
            ':' : 'DWUKROPEK',
            ';' : 'SEMIKOLON',
            ',' : 'PRZECINEK',
            'liczba' : 'LICZBA',
            '{' : 'LB',
            '}' : 'RB',
            '<' : 'LA',
            '>' : 'RA',
            'długość' : 'DLUGOSC'
            }

tokens += reserved.values()


t_ignore = ' \t'
t_PODZIELONE_PRZEZ = r'przez'
t_MNIEJSZE_OD = r'mniejsze'
t_WIEKSZE_OD = r'większe'
t_W_PRZECIWNYM_WYPADKU = r'wpw'
t_PLUS = r'plus'
t_MINUS = r'minus'
t_RAZY = r'razy'
t_WYNOSI = r'wynosi'
t_LP = r'\['
t_RP = r'\]'
t_LB = r'\{'
t_RB = r'\}'
t_LA = r'\<'
t_RA = r'\>'
t_DWUKROPEK = r':'
t_SEMIKOLON = r';'
t_PRZECINEK = r','
t_ZALOZMY = r'załóżmy'
t_ROWNE = r'równe'
t_ROZNE = r'różne'
t_FUNKCJA = r'funkcja'
t_DOPUKI = r'dopóki'
t_JEZELI = r'jeżeli'
t_PRZYPISZ = r'przypisz'
t_WYPISZ = r'wypisz'
t_ZWROC = r'zwróć'
t_WPISZ = r'wpisz'
t_DLUGOSC = r'długość'

def t_TEKST(t):
    r'"([^"]*)"'
    t.value = str(t.value)
    return t

def t_LICZBA(t):
    r'[+-]?(\d+(\.\d*)?)'
    t.value = float(t.value)
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_IDENTYFIKATOR(t):
    r'[a-zA-ZąćęłńóśźżĄĆĘŁŃÓŚŹŻ_][a-zA-Z0-9ąćęłńóśźżĄĆĘŁŃÓŚŹŻ_]*'
    if t.value in reserved:
        t.type = reserved[ t.value ]
    return t

def t_error(t):
    print(f"Nieznany znak: {t.value[0]}")
    t.lexer.skip(1)