funkcja powiel_tekst[t, n]: {
    załóżmy tmp równe t;
    załóżmy i równe 0;
    dopóki [i mniejsze n minus 1]: {
        i przypisz i plus 1;
        tmp przypisz tmp plus t;
    }
    zwróć [tmp];
}
wypisz[powiel_tekst["a", 5]];