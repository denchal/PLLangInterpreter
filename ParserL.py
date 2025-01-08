# -*- coding: utf-8 -*-
import ply.yacc as yacc

def p_program(p):
    '''program : instrukcje'''
    p[0] = ('program', p[1])

def p_instrukcje(p):
    '''instrukcje : instrukcja instrukcje
                  | instrukcja'''
    if len(p) == 3:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = [p[1]]

def p_instrukcja(p):
    '''instrukcja : deklaracja
                  | funkcja
                  | petla
                  | warunek
                  | wypisz
                  | zwroc
                  | przypisz
                  | wywolanie SEMIKOLON
                  | instr_warunkowa
                  | wpisz
                  | dlugosc SEMIKOLON'''
    p[0] = p[1]

def p_deklaracja(p):
    '''deklaracja : ZALOZMY IDENTYFIKATOR ROWNE wyrazenie SEMIKOLON
                  | ZALOZMY IDENTYFIKATOR ROWNE wywolanie SEMIKOLON'''
    p[0] = ('deklaracja', p[2], p[4])

def p_przypisz(p):
    '''przypisz : IDENTYFIKATOR PRZYPISZ wyrazenie SEMIKOLON
                | IDENTYFIKATOR LA LICZBA RA PRZYPISZ wyrazenie SEMIKOLON
                | IDENTYFIKATOR LA IDENTYFIKATOR RA PRZYPISZ wyrazenie SEMIKOLON'''
    if len(p) == 5:
        p[0] = ('przypisz', p[1], p[3])
    else:
        p[0] = ('przypisz', p[1], p[3], p[6])

def p_funkcja(p):
    '''funkcja : FUNKCJA IDENTYFIKATOR LP parametry RP DWUKROPEK blok'''
    p[0] = ('funkcja', p[2], p[4], p[7])

def p_parametry(p):
    '''parametry : IDENTYFIKATOR PRZECINEK parametry
                 | LICZBA PRZECINEK parametry
                 | wyrazenie PRZECINEK parametry
                 | wyrazenie
                 | '''
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    elif len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = []

def p_tablica(p):
    '''tablica : LA parametry RA'''
    p[0] = p[2]

def p_blok(p):
    '''blok : LB instrukcje RB'''
    p[0] = p[2]

def p_petla(p):
    '''petla : DOPUKI LP warunek RP DWUKROPEK blok'''
    p[0] = ('petla', p[3], p[6])

def p_instr_warunkowa(p):
    '''instr_warunkowa : JEZELI LP warunek RP DWUKROPEK blok W_PRZECIWNYM_WYPADKU DWUKROPEK blok
                       | JEZELI LP warunek RP DWUKROPEK blok'''
    if len(p) == 10:
        p[0] = ('instr_warunkowa', p[3], p[6], p[9])
    else:
        p[0] = ('instr_warunkowa', p[3], p[6])

def p_warunek(p):
    '''warunek   : wyrazenie PODZIELONE_PRZEZ wyrazenie
                 | wyrazenie MNIEJSZE_OD wyrazenie
                 | wyrazenie WIEKSZE_OD wyrazenie
                 | wyrazenie WYNOSI wyrazenie
                 | wyrazenie ROZNE wyrazenie
                 | IDENTYFIKATOR
                 | LICZBA'''
    if len(p) == 4:
        p[0] = (p[2], p[1], p[3])
    else:
        p[0] = p[1]

def p_wyrazenie(p):
    '''wyrazenie : wyrazenie PLUS wyrazenie
                 | wyrazenie MINUS wyrazenie
                 | wyrazenie RAZY wyrazenie
                 | wyrazenie PODZIELONE_PRZEZ wyrazenie
                 | wyrazenie MNIEJSZE_OD wyrazenie
                 | wyrazenie WIEKSZE_OD wyrazenie
                 | wyrazenie WYNOSI wyrazenie
                 | wyrazenie ROZNE wyrazenie
                 | wywolanie
                 | IDENTYFIKATOR LA LICZBA RA
                 | IDENTYFIKATOR LA indeksacja RA
                 | IDENTYFIKATOR
                 | LICZBA
                 | tablica
                 | TEKST
                 | dlugosc'''
    if len(p) == 4:
        p[0] = (p[2], p[1], p[3])
    elif len(p) == 5:
        p[0] = ('indeksowanie', p[1], p[3])
    else:
        p[0] = p[1]

def p_indeksacja(p):
    '''indeksacja : wyrazenie PRZECINEK indeksacja
                  | wyrazenie
                  | '''
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    elif len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = []

def p_wypisz(p):
    '''wypisz : WYPISZ LP wyrazenie RP SEMIKOLON
              | WYPISZ LP wywolanie RP SEMIKOLON'''
    p[0] = ('wypisz', p[3])

def p_zwroc(p):
    '''zwroc : ZWROC LP wyrazenie RP SEMIKOLON
             | ZWROC LP wywolanie RP SEMIKOLON'''
    p[0] = ('zwroc', p[3])

def p_wywolanie(p):
    '''wywolanie : IDENTYFIKATOR LP parametry RP'''
    p[0] = ('wywolanie', p[1], p[3])

def p_wpisz(p):
    '''wpisz : WPISZ IDENTYFIKATOR SEMIKOLON'''
    p[0] = ('wpisz', p[2])

def p_dlugosc(p):
    '''dlugosc : DLUGOSC LP wyrazenie RP'''
    p[0] = ('dlugosc', p[3])

# Obsługa błędów
def p_error(p):
    if p:
        print(f"Błąd składniowy w pobliżu tokenu: {p.value}")
    else:
        print("Błąd składniowy: koniec pliku")