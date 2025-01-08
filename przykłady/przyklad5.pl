funkcja powiel_tekst[n]: {
    załóżmy tmp równe tekstG;
    załóżmy i równe 0;
    dopóki [i mniejsze n minus 1]: {
        i przypisz i plus 1;
        tekstG przypisz tekstG plus tmp;
    }
}
załóżmy tekstG równe "a";
powiel_tekst[10];
wypisz[tekstG];