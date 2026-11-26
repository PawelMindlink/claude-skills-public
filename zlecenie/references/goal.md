# Kiedy `/goal` i jak pisać warunek

Źródło: https://code.claude.com/docs/en/goal (odczyt 25.11.2026) oraz 19 uruchomień celu w rozmowach autora tej umiejętności
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
- **Dowody ponumerowane.** Dawne cele autora, które doszły do końca, miały listę „(1)… (2)… pokazane
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

- Audyt 26.11.2026 zapisów rozmów autora (dwa projekty, 25.10–14.11.2026): 19 prób `/goal`.
  18 to wklejone bloki wielowierszowe, które Claude Code zapisał jako `<pasted_content>` z `/goal`
  w środku, czyli jako zwykłą wiadomość; po żadnej nie ma komunikatu „Goal set”, więc cel nie ruszył. Jedna próba (13.11) została zapisana jako polecenie, bez znacznika wklejonej
  treści, ale odrzucił ją limit 4000 znaków. Najmniejszy
  zawinięty wklejony tekst miał 141 znaków i 5 wierszy; wklejenia jednego wiersza nie znaleziono.
- 26.11.2026 wklejony sam wiersz `/goal …` (959 znaków, osobna wiadomość) też został zapisany jako
  wklejona treść, bez „Goal set”. Dlatego użytkownik wpisuje ręcznie `/goal ` ze spacją i wkleja sam warunek,
  a potem sprawdza, czy program odpisał „Goal set: …”. Samo `/goal` pokazuje stan celu.
- Potwierdzone 26.11.2026 (jedna z rozmów autora): wpisane ręcznie `/goal ` i wklejony warunek
  program zapisał jako polecenie i odpisał „Goal set: …”. Wysłane w trakcie pracy modelu trafiło do
  kolejki i zostało wykonane jako polecenie dopiero po zakończeniu bieżącego ruchu (9 minut później),
  a nie wstawione jako tekst.
- Jeden cel na rozmowę. Ten sam cel wklejony do dwóch rozmów daje dwóch wykonawców na tych samych plikach.
- Tryb auto przed uruchomieniem, bo cel nie zmienia trybu: w trybie ręcznym praca staje na każdej zgodzie.
- `/goal clear` zatrzymuje. Po `--continue` albo `--resume` cel wraca, a liczniki zaczynają od zera.
- Ocena po każdej turze jest płatna dodatkowo. Gdy pomocnik albo polecenie w tle jeszcze pracuje, ocena
  czeka do końca następnej tury.
