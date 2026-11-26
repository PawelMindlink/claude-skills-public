# Umiejętności dla Claude

Na razie jest tu jedna umiejętność: `zlecenie`. Opisujesz jej zadanie, a ona oddaje gotowy prompt do nowej
rozmowy razem z modelem, poziomem myślenia i trybem (planowanie albo auto). Zanim ułoży prompt, sprawdza
w plikach projektu, czy to zadanie było już podejmowane i dlaczego stanęło. Gdy przyczyną był brak popytu
albo dostępu, odpowiada „nie zlecaj”, bo mocniejszy model tego nie zmieni.

Umiejętność jest po polsku. Zakłada wtyczkę superpowers do Claude Code; bez niej działa, ale część nazw
umiejętności w promptach nie zadziała.

## Instalacja w trzech krokach

1. Pobierz repozytorium:
   `git clone https://github.com/PawelMindlink/claude-skills-public`
2. Skopiuj katalog `zlecenie` do `~/.claude/skills/` (w Windows: `%USERPROFILE%\.claude\skills\`).
3. Sprawdź program dziennika:
   `python3 -X utf8 ~/.claude/skills/zlecenie/scripts/dziennik.py podsumowanie`
   Na czystej instalacji wypisuje „Dziennik jest pusty.” Potem otwórz nową rozmowę w Claude Code i napisz
   na przykład: „Przygotuj prompt dla nowej rozmowy: przebuduj stronę cennika”.

## Co podmienić u siebie

1. **Listę umiejętności** w `zlecenie/references/dobor-umiejetnosci.md`. Zostawiłem tylko umiejętności
   superpowers i Anthropic. Dopisz własne w dwóch wierszach oznaczonych „Dopisz własne”, bo prompt wpisuje
   wyłącznie nazwy z tej listy.
2. **Polecenie Pythona.** W Windows zamień `python3` na `py` w plikach `SKILL.md` i `references/*.md`,
   jeśli `python3` u Ciebie nie działa.
3. **Miejsce dziennika.** Program `dziennik.py` zapisuje wynik każdego zlecenia do
   `~/.claude/zlecenia-wyniki.csv`. Inny plik ustawisz zmienną środowiskową `ZLECENIA_DZIENNIK`.
4. **Plik z decyzjami.** W `SKILL.md`, w kroku „Historia”, jest wiersz o pliku z Twoimi zapisanymi
   decyzjami. Wpisz tam jego ścieżkę albo usuń wiersz.
5. **Limity i ceny modeli** w `zlecenie/references/modele.md`. Plik zakłada, że wąskim gardłem jest
   tygodniowy limit najmocniejszego modelu, a nie cena tokenu. Ceny i wersje są z 23–25 listopada 2026;
   umiejętność sama każe je odświeżyć, gdy plik ma więcej niż trzy miesiące.
6. **Przykłady z datami.** Reguła z datą i zdarzeniem opisuje przebieg u autora, a nie u Ciebie. Liczby
   w części „Co sugerują dane autora” w `references/modele.md` zastąpi Twój dziennik po kilku zleceniach,
   a wersję programu i limity modeli sprawdź u siebie.

## Jak sprawdzam, czy działa

Każde zlecenie dostaje wiersz w dzienniku: model, poziom, wynik według warunków z promptu, liczba tur,
tokeny i liczba poprawek kierunku. `dziennik.py podsumowanie` liczy dla każdego układu, ile zleceń
osiągnęło wynik i za ile tokenów. Progi przejścia na mocniejszy model w `modele.md` są założeniem
startowym; poprawiam je dopiero po dziesięciu zamkniętych zleceniach.

## Licencja

MIT, w pliku `LICENSE`.
