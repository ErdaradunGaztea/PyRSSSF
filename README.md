# PyRSSSF

Skrypt wspomagający tworzenie artykułów opisujących sezony lig piłkarskich na polskiej Wikipedii przy użyciu tabel ze stron RSSSF.

## Sposób użycia

Przypuśćmy, że chcemy wygenerować tabelę końcową i macierz meczów na podstawie [artykułu na RSSSF dot. ligi malawijskiej w 2019 roku](http://www.rsssf.com/tablesm/malaw2019.html). W takim wypadku wywołujemy funkcję `main` z pliku `main.py` z parametrami `country` i `year` skonstruowanymi według tych prostych zasad:

* `country` odnosi się do części linku strony po ostatnim slashu, a przed rokiem -- w rozważanym przypadku jest to `malaw`, jako część wydzielona z pełnego `malaw2019.html`
* `year` należy podać pełny, czyli `2019`, nie `19`; nawet jeżeli w adresie występuje rok skrócony, skrypt sam wypróbuje obydwie możliwości

## Znane problemy

Mnóstwo, dlatego jest we wczesnej fazie alpha. W miarę możliwości będą usuwane, tak jak i dodawane nowe:

* Możliwy jest wybór jedynie pomiędzy zwycięstwem za 2 i 3 punkty, skrypt nie dysponuje obsługą innych rodzajów szablonów.
* Tabela meczów zostanie wygenerowana poprawnie tylko w przypadku gdy dla dowolnej pary gospodarzy ZespółX i gości ZespółY rozegrany został najwyżej jeden mecz ZespółX - ZespółY.
[x] Skrypt nie generuje uwagi na boku o spadku (dodaje jednak kolor i dodawanie **(S)**).
[x] Skrypt jest póki co dostosowany do pierwszych lig, więc nie dysponuje obsługą awansów.
[x] Skrypt oddziela nazwę zespołu od liczby meczów i reszty statystyk na podstawie przynajmniej podwójnej spacji (gdyż nierzadko pojedyncza spacja występuje w nazwie zespołu). Jeżeli nazwa zespołu jest na tyle długa, że oddzielona jest pojedynczą spacją, skrypt nie zadziała.
[x] Jednocyfrowa liczba straconych bramek spowoduje wyrzucenie wyjątku albo nieprawidłowe wyniki (z powodu zapisu w postaci `00- 0`, z naciskiem na spację po myślniku).
