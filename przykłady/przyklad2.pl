funkcja fib[n]: {
    jeżeli [n wynosi 1]: {
        zwróć [1];
    }
    jeżeli [n wynosi 2]: {
        zwróć [1];
    }
    zwróć [fib[n minus 1] plus fib[n minus 2]];
}
wypisz[fib[15]];