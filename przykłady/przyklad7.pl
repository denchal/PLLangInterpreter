funkcja przeszukiwanie_wgłąb[u]: {
    wypisz[u];
    odwiedzoneG<u> przypisz 1;
    załóżmy i równe 0;
    dopóki [i mniejsze długość[grafG<u>]]: {
        jeżeli [odwiedzoneG<grafG<u,i>> wynosi 0]: {
            przeszukiwanie_wgłąb[grafG<u,i>];
        }
        i przypisz i plus 1;
    }
}


załóżmy grafG równe <
                    <1>,
                    <0>,
                    <0>
                    >;

załóżmy odwiedzoneG równe <0, 0, 0>;
przeszukiwanie_wgłąb[0];
wypisz[odwiedzoneG];