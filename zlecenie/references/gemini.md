# Zlecanie pracy Gemini 4 (koordynacja)

Stan na 26.11.2026. Opis na podstawie prób autora; przed użyciem sprawdź na własnych zadaniach.

## Kiedy

Tylko pomocnik od czytania dużej ilości tekstu albo od wykonania według opisu, gdy wynik sprawdza
polecenie (testy, porównanie z kluczem). W próbie autora Gemini 4 Hydrogen zaliczył takie zadania tak
samo jak pomocnik Sonnet, bez zużycia limitu Claude. Jedno sprawdzenie albo odczyt jednego pliku robisz
sam, bo wywołanie Gemini trwa od pół minuty do kilku minut. Recenzji planu Gemini nie dostaje: w próbie
drugi recenzent dokładał mało wad, a w planach, w których poprawki wynikały z brakujących faktów, żaden
recenzent ich nie znalazł.

## Kto i jak wywołuje

Rozmowa główna albo pomocnik budujący, jednym poleceniem w terminalu:

    python3 -X utf8 ~/.claude/skills/zlecenie/scripts/agy_zlec.py --model gemini-4-hydrogen-high --polecenie <plik.md> --wynik <plik.json>

Polecenie leży w pliku i ma najwyżej 28 000 znaków. Układ: `<rola>` (zadanie, data, zdanie „wszystko,
czego potrzebujesz, jest w tym poleceniu: nie czytaj plików i nie uruchamiaj narzędzi”), `<format_odpowiedzi>`
z jednym przykładem z innej dziedziny, dane w znacznikach XML, na końcu `<zadanie>` zaczynające się od
„Na podstawie … powyżej”. Bez „pomyśl krok po kroku” i bez „MUSISZ”; głębokość ustawia poziom w nazwie
modelu. Program daje pusty katalog domowy, zakazy zapisu, poleceń, sieci i MCP oraz piaskownicę.

## Jak sprawdzasz wynik

Wynik Gemini traktujesz jak meldunek pomocnika: przed użyciem przepuszczasz go przez to samo sprawdzenie,
które zlecenie opisało. Kod zapisuje do repozytorium Claude, nie Gemini. Tok myślenia Gemini leży obok
wyniku (`<wynik>-myslenie.md`); czytasz go przy niezaliczonym sprawdzeniu, żeby poprawić polecenie.

## Gdy coś zawiedzie

| Kod programu | Co się stało | Co robisz |
|---|---|---|
| 4 | wyczerpany limit Gemini | program sam powtarza przez klucz Gemini API (płatny za tokeny); bez klucza zlecasz pomocnikowi Sonnet |
| 5 | przekroczony czas | jak wyżej |
| 3 | błąd albo pusta odpowiedź | czytasz `stderr` w pliku wyniku; odmowa odczytu pliku znaczy, że polecenie odsyła do pliku zamiast podać jego treść |
| 0, ale sprawdzenie nie przechodzi | zła odpowiedź | jedna poprawka polecenia; drugie niepowodzenie oddajesz pomocnikowi Sonnet |

## Granice

- Strona pytań i odpowiedzi Antigravity (https://antigravity.google/docs/faq.md, odczyt 26.11.2026)
  zabrania łączenia konta Antigravity z innymi agentami, także z Claude Code, pod groźbą zawieszenia
  konta. Decyzja należy do Ciebie; klucz Gemini API nie ma tego ryzyka.
- Bez `--mode plan`: ten tryb dokleja instrukcję planowania i psuje zadania wykonania.
