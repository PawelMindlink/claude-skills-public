# Kiedy `/goal` i jak pisać warunek

Źródło: https://code.claude.com/docs/en/goal (odczyt 25.11.2026) oraz 19 uruchomień celu w rozmowach użytkownika
z okresu 25.10–14.11.2026.

## Jak to działa

`/goal <warunek>` ustawia warunek zakończenia i od razu zaczyna pracę. Po każdej turze osobny, mały model
czyta warunek i rozmowę, po czym orzeka: spełniony, jeszcze nie, niemożliwy. Przy „jeszcze nie” Claude
dostaje powód i pracuje dalej bez popychania.

Dwie cechy rządzą tym, jak pisać warunek:

- **Oceniający niczego nie uruchamia i nie czyta plików.** Widzi tylko to, co Claude pokazał w rozmowie.
  Warunek, którego dowód nie pojawia się w rozmowie, nigdy nie zostanie uznany za spełniony.
- **Nie ma wbudowanej granicy tur.** Granicę wpisuje się do warunku.

## Kiedy `/goal`, a kiedy zwykłe polecenie

`/goal` wybierasz, gdy wszystkie trzy zdania są prawdziwe:

1. Koniec da się sprawdzić poleceniem, liczbą albo stanem, który widać w rozmowie.
2. Praca zajmie wiele tur.
3. Użytkownik nie chce popychać każdej tury, a działania po drodze są odwracalne albo mają nazwane miejsca
   czekania na jego zgodę.

`/goal` idzie tylko w parze z trybem AUTO i bez „Pytań na start”. Cel rusza od razu po wpisaniu i po
każdej turze jest popychany dalej, więc tryb planowania i czekanie na odpowiedzi użytkownika kosztują puste
tury. Gdy zadanie potrzebuje najpierw planu albo pytań, blok dostaje zwykły prompt w trybie PLAN,
a prompt każe rozmowie po zatwierdzeniu drogi podać użytkownikowi gotowy warunek do wpisania po `/goal`.
W próbie z 25.11.2026 umiejętność wskazała naraz „Tryb: PLAN”, „Forma: /goal” i pytania na start, czyli
układ, który sam sobie przeczy.

Zwykłe polecenie wybierasz, gdy:

- droga jest niejasna i najpierw potrzebna jest rozmowa z użytkownikiem (rozmowa 1 w układzie dwóch rozmów jest
  zawsze zwykłym poleceniem w trybie planowania);
- wynik ocenia się okiem albo gustem i nie ma sprawdzenia, które da się pokazać w rozmowie;
- zadanie zmieści się w kilku turach;
- praca ma biec co jakiś czas, a nie do skutku: wtedy służy do tego `/loop` albo zadanie zaplanowane.

## Warunek, który się trzyma

- **Jeden mierzalny stan końcowy** i **nazwane sprawdzenie**, którego wynik Claude pokazuje w rozmowie:
  „`py -m pytest tests -q` kończy się kodem 0 i wynik jest pokazany w rozmowie”.
- **Dowody ponumerowane.** Dawne cele użytkownika, które doszły do końca, miały listę „(1)… (2)… pokazane
  w rozmowie”.
- **Granica:** „albo zatrzymaj się po 40 turach i zamelduj, co zostało”.
- **Ograniczenia, które mają znaczenie:** czego nie wolno zmienić, co czeka na zgodę.
- **Nazwany stan czekania** (użytkownik chce pytań także w trakcie): „Gdy potrzebna jest decyzja użytkownika, zadaj
  pytanie z własnym zaleceniem, rób dalej to, co od odpowiedzi nie zależy, a gdy nic takiego nie zostało,
  napisz »Czekam na odpowiedź użytkownika« i wymień otwarte pytania”. Oceniający zna tylko trzy werdykty, więc
  na takie zdanie odpowie „jeszcze nie” i zacznie kolejną turę; pętlę zatrzyma dopiero kilka tur z rzędu
  bez użycia narzędzi, po czym cel zostaje ustawiony i rusza po następnej wiadomości użytkownika. Czekanie
  kosztuje więc kilka pustych tur. Gdy praca ma wiele miejsc czekania na użytkownika, wybierz zwykłe polecenie
  zamiast `/goal`.
- **Najwyżej 4000 znaków.** 13.11.2026 Claude Code odrzucił cel użytkownika, który miał 6508 znaków. Celuj
  w około 1500: szczegóły idą do pliku `ZLECENIE-<temat>.md`, a warunek na niego wskazuje.

Przykład:

~~~
Zlecenie z pliku ~/.claude/projects/<projekt>/memory/ZLECENIE-strony.md jest wykonane i w rozmowie pokazano: (1) listę
opublikowanych stron z adresami i kodem odpowiedzi 200, (2) wynik `py -m pytest _scripts/tests -q`
z kodem 0, (3) wpis w sekcji „Wynik” tego pliku. Gdy potrzebna jest decyzja użytkownika, zadaj pytanie
z zaleceniem i rób dalej to, co od odpowiedzi nie zależy; gdy nic takiego nie zostało, napisz „Czekam na
odpowiedź użytkownika”. Zatrzymaj się po 40 turach i zamelduj, co zostało.
~~~

## Jak użytkownik to uruchamia

- Wpisuje `/goal ` ręcznie i wkleja warunek. W zapisach jego rozmów tylko jedno uruchomienie zostało
  zapisane jako polecenie; pozostałe, wklejone jako długi tekst razem ze słowem `/goal`, są zapisane jako
  zwykłe wiadomości. Nie jest potwierdzone, że wtedy cel działał, więc po uruchomieniu użytkownik sprawdza
  znacznik `◎ /goal active` albo wpisuje samo `/goal`, które pokazuje stan.
- Jeden cel na rozmowę. Ten sam cel wklejony do dwóch rozmów daje dwóch wykonawców na tych samych plikach.
- Tryb auto przed uruchomieniem, bo cel nie zmienia trybu: w trybie ręcznym praca staje na każdej zgodzie.
- `/goal clear` zatrzymuje. Po `--continue` albo `--resume` cel wraca, a liczniki zaczynają od zera.
- Ocena po każdej turze jest płatna dodatkowo. Gdy pomocnik albo polecenie w tle jeszcze pracuje, ocena
  czeka do końca następnej tury.
