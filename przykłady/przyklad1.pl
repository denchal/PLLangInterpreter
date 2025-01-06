funkcja nwd[a, b]: {
    dopóki [a różne b]: {
        jeżeli [a większe b]: {
            a przypisz a minus b;
        }
        wpw: {
            b przypisz b minus a;
        }
    }
    zwróć [a];
}
załóżmy x równe nwd[30,15];
załóżmy y równe nwd[27,9];
załóżmy z równe nwd[x,y];
wypisz [z];