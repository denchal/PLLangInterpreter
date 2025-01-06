# PLLangInterpreter
## Ta strona zawiera podstawowe informacje na temat zaprojektowanego przeze mnie języka programowania, wraz z instrukcją uruchomienia.

### Wymagania:
<ul>
  <li>Python 3</li>
  <li>Biblioteki znajdujące się w pliku requirements.txt</li>
</ul>

Należy sklonować lub pobrać repozytorium, a następnie zainstalować wymagane biblioteki uruchamiając polecenie 
```
pip install -r requirements.txt
```

Następnie polecam przejżeć przykłady, uruchomić każdy z nich można np. poleceniem
```
python3 main.py przykłady/przyklad2.pl
```
Wnętrze języka korzysta z generatora PLY.

### Aktualnie interpreter obsługuje:
<ul>
  <li>Deklaracje zmiannych (typu numerycznego)</li>
  <li>Deklaracje funkcji wraz z ich wywoływaniem</li>
  <li>Zmianę wartości zmiennej po jej deklaracji wraz z przypisaniem wyniku funkcji</li>
  <li>Wypisywanie na standardowym wyjściu tekstów oraz wartości zmiennych</li>
  <li>Pętle</li>
  <li>Wprowadzanie wartości ze standardowego wejścia</li>
  <li>Rekurencję</li>
</ul>

Przykładowa funkcja obliczająca n-ty wyraz ciągu fibonacciego w tym języku:
```
funkcja fib[n]: {
    jeżeli [n wynosi 1]: {
        zwróć [1];
    }
    jeżeli [n wynosi 2]: {
        zwróć [1];
    }
    zwróć [fib[n minus 1] plus fib[n minus 2]];
}
```

Jak widać język ten składnią inspirowany jest językiem C, ale starałem się, żeby znalazło się w nim jak najwięcej polskich zwrotów i określeń. Szczególnie widać to w deklaracji zmiennych:
```
załóżmy x równe fib[15];
```

Po zadeklarowaniu zmiennej w taki sposób przechowana zostanie pod nią wartość fib[15] czyli 610.
Możemy następnie wypisać ją na ekranie:
```
wypisz [x];
```

Alternatywnie możemy od razu wyświetlić zwróconą przez funkcję wartość, np.:
```
wypisz [fib[15]];
```
