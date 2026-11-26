# Dobór modelu, poziomu myślenia, doradcy i trybu

Stan na 26.11.2026. Modele i ceny zmieniają się co kilka miesięcy: gdy ten plik ma więcej niż trzy miesiące
albo pojawił się nowy model, przeczytaj strony z sekcji „Źródła”, a nowy model wprowadź regułą przyjęcia
z sekcji „Drabina ról”, zamiast przepisywać tabele.

## Zasada

Ograniczeniem autora tej umiejętności jest tygodniowy limit planu, a nie cena tokenu: jego pomocnicy
stanęli właśnie na tym limicie. Na planie Max pula jest jedna dla wszystkich modeli, a Fable ciągnie z niej
szybciej i najwyżej do 50% (https://support.claude.com/en/articles/15424964-claude-fable-models-on-your-plan,
odczyt 26.11.2026). Sprawdź, co ogranicza Ciebie, i popraw ten akapit. Dlatego Fable pracuje tylko tam, gdzie rozstrzyga się wynik (diagnoza, plan, osąd), a rutynę
wykonują tańsze modele. Poziom myślenia jest tańszą dźwignią niż zmiana modelu, więc najpierw ruszasz
poziom.

## Cztery cechy zadania, które decydują

Ustalasz je przed wyborem, każdą jako „tak” albo „nie”, na podstawie plików, a nie wrażenia:

1. **Koniec da się sprawdzić** poleceniem albo liczbą widoczną w rozmowie.
2. **Droga jest znana:** istnieje spisany plan z krokami albo zadanie jest jednym krokiem.
3. **Błąd jest odwracalny:** nic nie wychodzi na zewnątrz i nic nie ginie.
4. **Poprzednie podejścia:** ile stanęło i w jakiej klasie przyczyny (krok „Historia” w `SKILL.md`);
   zadanie odłożone świadomie liczy się jak nowe.

| Cechy | Układ |
| --- | --- |
| Koniec sprawdzalny, droga znana, błąd odwracalny | Rola „Wykonanie według opisu” (dziś Opus 5.5 medium). Tryb auto. |
| Koniec sprawdzalny, droga znana, błąd nieodwracalny | Rola „Wykonanie według opisu”, tryb planowania, lista zgód. |
| Koniec sprawdzalny, droga nieznana | Rola „Budowa” (dziś Opus 5.5 high), tryb planowania. |
| Koniec oceniany okiem albo osądem, albo droga nieznana i podejście stanęło na złym planie | Dwie rozmowy: rola „Diagnoza i plan” planuje, rola „Wykonanie według opisu” z doradcą wykonuje. |
| Podejście stanęło na wykonaniu | Jeden szczebel wyżej niż model, który pracował poprzednio. |
| Podejście stanęło na zgodach | Ten sam układ co poprzednio; zmieniają się zasady zgód. |
| Podejście stanęło na granicy zewnętrznej | Nie zlecasz; zmienia się cel. |
| Zadanie odłożone świadomie, nikt go nie próbował | Układ według pozostałych cech, jak dla nowego zadania; gdy powód odłożenia trwa, nie zlecasz. |

## Kiedy model „nie daje rady” — próg przejścia szczebel wyżej

Szczeble (modele według „Drabiny ról”, stan 26.11.2026): Sonnet 5.5 medium → Opus 5.5 medium → Opus 5.5 high →
Opus 5.5 medium z doradcą Fable → Fable 5.2 high. Modelu i poziomu myślenia rozmowa nie zmieni sobie sama: robi to tylko użytkownik poleceniem
`/model` albo `/effort`. Dlatego rozmowa wykonująca zatrzymuje się, pisze użytkownikowi gotowe polecenie do
wpisania (na przykład `/effort high`) i powód, a po jego wpisaniu pracuje dalej. Robi to, gdy zajdzie
jedno z trzech zdarzeń:

- to samo sprawdzenie nie przechodzi po dwóch próbach naprawy;
- użytkownik dwa razy odrzucił wynik z tego samego powodu;
- minęła granica tur z polecenia, a spełniona jest mniej niż połowa punktów „Gotowe, gdy”.

Bez żadnego z tych zdarzeń model zostaje. Liczby 2, 2 i połowa są założeniem startowym z 25.11.2026,
a nie pomiarem: po dziesięciu wierszach w dzienniku popraw je według tego, co pokazują wyniki.

## Dziennik wyników

Plik `~/.claude/zlecenia-wyniki.csv`, jeden wiersz na zlecenie. Zapisuje go i czyta wyłącznie
program `~/.claude/skills/zlecenie/scripts/dziennik.py` (uruchamiany przez `python3 -X utf8`), bo
ręcznie dopisany wiersz psuje się na średniku w treści pola:

- `dziennik.py start …` uruchamia umiejętność w chwili oddania polecenia. Wiersz dostaje stan `w_toku`
  i numer, który trafia do polecenia.
- `dziennik.py koniec --id N …` uruchamia rozmowa wykonująca na końcu pracy.
- `dziennik.py wiszace` pokazuje zlecenia, które ruszyły i nie zapisały wyniku. Krok „Historia” czyta tę
  listę: rozmowa urwana na limicie nie zapisze wyniku sama, a bez tego dziennik pokazywałby same sukcesy.
- `dziennik.py podsumowanie` liczy dla każdego układu, ile zleceń osiągnęło wynik i za ile tokenów.

Pola wyniku:

- `wynik`: `osiagniety`, `nieosiagniety` albo `przerwany` — według sprawdzenia z „Gotowe, gdy”, nie według
  opinii.
- `dowod`: polecenie albo liczba, która to pokazuje.
- `tokeny`: suma z zapisu rozmowy i jej pomocników, razem z odczytem z pamięci podręcznej. Liczy ją sam
  `dziennik.py koniec` (albo `dziennik.py zuzycie`); model nie czyta `/usage`, a meldunki pomocników
  pomijają odczyt z pamięci podręcznej, więc obie drogi zaniżały wynik kilkadziesiąt razy (25.11.2026).
- `poprawki_uzytkownika`: ile razy użytkownik musiał poprawić kierunek albo odrzucił wynik.
- `przejscie_wyzej`: puste albo zdarzenie, które wymusiło mocniejszy układ.

Ten plik jest jedyną miarą, czy umiejętność działa: odsetek zleceń z wynikiem `osiagniety`, tokeny na
osiągnięty wynik i liczba poprawek użytkownika, liczone osobno dla każdego układu.

## Drabina ról

Reguły tej umiejętności mówią o rolach, a nie o nazwach modeli. Nazwa modelu stoi tylko w kolumnie „Model dziś”,
więc nowy model zmienia jeden wiersz tej tabeli, a nie reguły (użytkownik, 26.11.2026: „To musi być elastyczny,
aktualizujący się system”). Rolę wyznaczają cztery cechy zadania z tabeli wyżej; rodzaj w dzienniku (`dziennik.py start --rodzaj`) pozwala potem porównać wyniki.

| Rola | Kiedy | Model dziś | Doradca | Tryb | Na czym stoi (data, wiersze dziennika) |
| --- | --- | --- | --- | --- | --- |
| Czytanie | odczyt, jedno sprawdzenie, przeczytanie zapisów rozmów; obejrzenie jednego obrazu | pomocnik Sonnet 5.5; obraz: Haiku 5.5; kandydat od 26.11.2026: Gemini 4 Hydrogen high przez `scripts/agy_zlec.py` przy czytaniu dużej ilości tekstu i wykonaniu według opisu ze sprawdzeniem poleceniem (`references/gemini.md`) | brak | — | założenie z 25.11; kalibracja 26.11 użyła dwóch pomocników Sonnet do zapisów rozmów (ok. 0,37 mln tokenów razem); próba 26.11 (zlecenie 21): Sonnet i Hydrogen po 3 z 3, Hydrogen bez limitu Claude |
| Wykonanie według opisu | rodzaj „wykonanie wedlug opisu”, także z „+ oceniane okiem”: pismo, publikacja, slajdy z gotowej treści | Opus 5.5 medium; high tylko z podanym powodem przy krótkim piśmie | brak; `/advisor fable` tylko przy ocenie okiem z gotowym planem z rozmowy 1 | auto; planowania, gdy coś wychodzi na zewnątrz | 26.11: 9 z 9 osiągniętych (1, 4, 5, 6, 11, 13, 14, 15, 16) |
| Budowa | rodzaj „budowa z podzadaniami” albo „niejasna droga” ze sprawdzalnym końcem (tabela cech: koniec sprawdzalny, droga nieznana) | Opus 5.5 high kieruje, pomocnicy Sonnet (czytanie) i Opus (kod); sprawdzenie planu: kandydat Gemini 4 Neon high przez `scripts/agy_zlec.py` od 26.11.2026 | brak | planowania na początku | założenie; 26.11 brak zamkniętych wierszy (17, 19, 20 w toku) |
| Diagnoza i plan | koniec oceniany okiem albo osądem, albo podejście stanęło na złym planie (rodzaj „niejasna droga” albo „po nieudanych podejsciach”) | Fable 5.2 high; medium, gdy użytkownik prowadzi rozmowę na bieżąco | brak | planowania, osobna rozmowa | 26.11: 2 z 3 osiągnięte (9, 10; 2 nie, z braku wzoru) |
| Doradca | długa praca z rutynowymi turami, w której o wyniku decyduje plan | Fable 5.2 | — | — | 26.11: 2 z 2 osiągnięte (14, 16), ale najdroższe (średnio 94 mln tokenów) |

Wiersz „Model dziś” zmienia tylko kalibracja, według reguły przyjęcia nowego modelu albo według danych
z dziennika, i zawsze dopisuje datę oraz numery wierszy w ostatniej kolumnie.

## Reguła przyjęcia nowego modelu (przyjęta przez użytkownika 26.11.2026)

1. **Kto i kiedy.** Gdy nowy model pojawi się na liście `/model` (sprawdzasz przy kroku 5, a także gdy użytkownik
   o nim wspomni), staje się kandydatem do ról poprzednika z tej samej rodziny: nowy Opus do ról Opusa,
   nowy Fable do ról Fable, nowy Sonnet do ról Sonneta. Pogłoska bez modelu na liście niczego nie zmienia.
2. **Co zmienia się w drabinie.** W kolumnie „Model dziś” dopisujesz „kandydat: <nazwa> od <data>” obok
   poprzednika. Od tej chwili umiejętność wskazuje kandydata w tej roli, a `dziennik.py start --model`
   zapisuje jego nazwę (np. `opus-5-6`).
3. **Jak trafia do dziennika i kiedy zapada decyzja.** Po trzech zamkniętych wierszach kandydata w danej roli
   kalibracja porównuje w `dziennik.py podsumowanie` jego odsetek osiągniętych, tokeny na osiągnięty wynik
   i poprawki użytkownika z poprzednikiem w tej samej roli. Nie gorzej na żadnej z trzech miar → kandydat zostaje
   jedynym modelem w roli; gorzej → wraca poprzednik. Decyzję wpisujesz z datą i numerami wierszy.
4. **Granica bezpieczeństwa.** Gdy kandydat dwa razy z rzędu zakończy się wynikiem `nieosiagniety` z przyczyny
   „wykonanie” (krok 2 w `SKILL.md`), wraca poprzednik od razu, bez czekania na trzeci wiersz.

Przykład: Opus 5.6 (26.11.2026 tylko zapowiedź, na liście `/model` go nie ma). Gdy się
pojawi, wiersze „Wykonanie według opisu” i „Budowa” dostają dopisek „kandydat: Opus 5.6”. Po trzech
zamkniętych zleceniach wykonania porównujesz go z Opusem 5.5 medium, który ma 9 z 9 osiągniętych.

Ta sama reguła służy do sprawdzenia szczebla niżej: Sonnet 5.5 jako kandydat do wykonania według opisu przy
pracy mechanicznej. Do 26.11.2026 nikt go w tej roli nie sprawdził na zleceniu użytkownika.

Reguły, których tabela nie pokazuje:

- **Opus 5.5 xhigh ma jedno zastosowanie:** programowanie według gotowej specyfikacji z testami, które
  trwa ponad 30 minut (zalecenie Anthropic dla długiej pracy w kodzie). Poziomu max nie wskazujesz. Poza
  tym przypadkiem wyższe poziomy Opusa myślą znacznie dłużej w każdej turze, a według ogłoszenia Anthropic
  Fable 5.2 na high osiąga wynik Opusa 5.5 na max przy około połowie kosztu zadania. To liczby producenta,
  niesprawdzone na pracy użytkownika.
- **Fable planuje, ale nie rozdziela pracy.** Według pomiarów Anthropic zebranych 23.11.2026 Opus 5.5
  kierujący pomocnikami na Sonnecie daje ten sam wynik za około jedną trzecią mniej, a Fable w roli
  kierującego kosztuje o 19% więcej przy tym samym wyniku. Dlatego Fable robi diagnozę i plan w osobnej
  rozmowie, a wykonaniem kieruje Opus.
- **Zlecanie pomocnikom opłaca się tylko** przy pracy rutynowej o długim ogonie albo większej niż jedna
  rozmowa. Jeden łańcuch zależnych kroków taniej wykona jedna rozmowa na niższym poziomie.
- **Start niżej, szczebel wyżej po niepowodzeniu sprawdzenia** jest według testów Anthropic około 40%
  tańszy niż wszystko od razu na wysokim poziomie, przy tym samym odsetku zaliczonych zadań. Stąd progi
  przejścia opisane wyżej. Przejście dzieje się w tej samej rozmowie i kosztuje użytkownika jedno wpisane
  polecenie.
- **Wysoka stawka nie jest powodem dla mocniejszego modelu.** Przed błędem nieodwracalnym chronią bramki:
  tryb planowania, lista zgód i człowiek, który zna się na rzeczy (prawnik, księgowa, odbiorca). Krótkie
  pismo o skutkach prawnych, z prawnikiem jako recenzentem, to droga znana i koniec sprawdzalny, czyli
  Opus 5.5; poziom high zamiast medium wolno dać z podanym powodem, bo przy krótkim zadaniu kosztuje
  niewiele. 25.11.2026 wskazałem do takiego pisma Fable 5.2 high z samego wrażenia, że „każdy krok wymaga
  osądu”, i autor słusznie to zakwestionował. Fable dostaje zadanie dopiero wtedy, gdy nie ma ani planu,
  ani taniego sprawdzianu.
- **Pomocnicy nie dziedziczą Fable.** W poleceniu podajesz model każdego pomocnika: Sonnet do czytania
  i wykonania według opisu, Opus do budowy i poprawek w kodzie, Haiku do obejrzenia jednego obrazu.
  Modelu działającego pomocnika nie da się zmienić, więc ustawia się go przy starcie.
- **Dwie rozmowy zamiast zmiany modelu w trakcie.** Zmiana modelu unieważnia zapamiętany kontekst rozmowy
  i cała historia jest czytana od nowa po pełnej cenie. Plan z rozmowy 1 trafia do pliku, a rozmowa 2
  zaczyna od niego.
- **Zapis zużycia.** Zużycie każdego zlecenia liczy `dziennik.py` z zapisu rozmowy. Po dziesięciu
  zamkniętych wierszach drabinę da się oprzeć na liczbach użytkownika, a nie producenta.

## Co sugerują dane autora (kalibracja 26.11.2026, 14 zamkniętych wierszy; zastąpi je Twój dziennik)

Pole „rodzaj” ujednolicone 26.11 do rodzajów z kroku 3 (kopia sprzed zmiany:
`~/.claude/zlecenia-wyniki.przed-kalibracja-2026-11-26.csv`). Tokeny wierszy 14, 15 i 16
przeliczone `dziennik.py zuzycie` na rozmowach, które uruchomiły `koniec`. Wiersz 12 (przerwany przed
startem) nie liczy się do żadnej roli. Wiersze 7, 8, 17, 18, 19, 20 są w toku.

- **Wykonanie według opisu: 9 z 9 osiągniętych** (1, 4, 5, 6, 11, 13, 14, 15, 16). Opus 5.5 medium bez
  doradcy: 5 z 5, średnio 31 mln tokenów, poprawki średnio 1. Opus 5.5 high: 2 z 2 (pismo 12 mln, slajdy
  42 mln i 3 poprawki), czyli wyższy poziom nie dał lepszego wyniku. Model w tej roli zostaje.
- **Doradca Fable przy wykonaniu: 2 z 2, ale średnio 94 mln tokenów** (14: 76 mln, 16: 113 mln) wobec 42 mln
  slajdów (13) bez doradcy przy ocenie okiem. Dwa wiersze nie pozwalają oddzielić kosztu doradcy od kosztu
  pomocników, więc doradca zostaje tylko przy ocenie okiem z planem z rozmowy 1, a nie jako ustawienie domyślne.
- **Diagnoza i plan na Fable 5.2: 2 z 3** (9 i 10 osiągnięte; 2 nieosiągnięte). Opus 5.5 high przy niejasnej
  drodze z oceną okiem: 0 z 1 (3, ekran budżetu). Obie porażki miały tę samą przyczynę: brak wzoru albo
  tego, co ma zostać ze starego rozwiązania. Przy ocenie okiem najpierw zdobywasz wzór, potem szczebel.
- **Budowa z podzadaniami: brak danych.** Wiersz „Budowa” w drabinie pozostaje założeniem.
- **Przyczyny poprawek użytkownika** (zapisy rozmów 26.11): brakujący fakt (9: wzór, 10: cel, 13: pochodzenie dań,
  16: przewaga produktu), zły kanał (17: Teams zamiast maila), żargon (18: „g(t)”, 8: „nic nie rozumiem”).
  Zły model ani zły katalog nie wystąpił ani razu. Najwięcej da więc krok 4 (pytania o fakty), a nie model.
- **Progi przejścia szczebel wyżej (2, 2, połowa) bez zmian:** żadne zamknięte zlecenie ich nie uruchomiło
  (jedyne pole `przejscie_wyzej` to limit 5 godzin w 11 i decyzja użytkownika w 12), więc nie ma czego mierzyć.
- **Rozmowa główna** zużywa większość tokenów zlecenia, prawie w całości na odczyt z pamięci podręcznej
  przy każdym kroku (25.11: od 47% do 100%). Krótsza rozmowa oszczędza więcej niż tańszy model.
- **`/goal`:** jedyna próba (14) zadziałała dopiero wpisana ręcznie; wklejona i połączona z `/advisor` nie.
  Potwierdza zasadę z kroku 7.

## Gemini 4 przez agy (decyzja autora z 26.11.2026)

Próba autora na prawdziwych planach i zadaniach: Gemini 4 Hydrogen zaliczył czytanie i wykonanie według opisu
ze sprawdzeniem poleceniem tak samo jak Sonnet, bez zużycia limitu Claude, więc jest kandydatem w roli
„Czytanie”. Recenzji planu Gemini nie dostaje: drugi recenzent dokładał mało trafnych wad. Regulamin
Antigravity zabrania łączenia konta z innymi agentami; zapasem jest klucz Gemini API. Szczegóły:
`references/gemini.md`.

## Doradca

Doradca to drugi, mocniejszy model, do którego model wykonujący sam sięga w ważnych momentach: przed
wyborem podejścia, przy powtarzającym się błędzie i przed ogłoszeniem końca. Widzi całą rozmowę. Włącza go
polecenie `/advisor fable`, wyłącza `/advisor off`.

- Opłaca się przy długiej pracy, w której większość tur jest rutynowa, a o wyniku decyduje plan.
- Nie opłaca się przy krótkim zadaniu ani tam, gdzie każda tura wymaga najmocniejszego modelu. Każde
  sięgnięcie do doradcy czyta całą rozmowę od nowa, bez zniżki za zapamiętany kontekst.
- Doradca musi być co najmniej tak mocny jak model główny. Przy Opusie 5.5 doradcą może być Fable albo
  Opus; przy Sonnecie 5.5 Fable, Opus albo Sonnet; przy Fable 5.2 tylko Fable 5.2.
- Częstość sięgania ustawia się zdaniem w poleceniu, na przykład „poradź się doradcy przed wyborem
  podejścia i przed ogłoszeniem końca”. Nie ma ustawienia, które to wymusza albo ogranicza.
- **Ustawienie doradcy zostaje na stałe** i według dokumentacji dziedziczą je także pomocnicy. Rozmowa
  włączona z `/advisor fable` zostawia więc doradcę Fable każdej następnej rozmowie i każdemu pomocnikowi
  na Sonnecie, co po cichu zjada limit Fable. Dlatego polecenie z linią `/advisor fable` zawiera wstawkę
  „Doradca”, która każe rozmowie przypomnieć na końcu o `/advisor off` (od 26.11.2026 oddanie nie ma
  osobnych kroków uruchomienia, tylko etykiety i wiadomości do wklejenia).
  W terminalu to samo daje `claude --advisor fable`, które działa tylko na jedną rozmowę.
- Polecenie `/advisor` przyjmuje `fable`, `opus`, `sonnet`, `off` (sprawdził autor 25.11.2026). Fable 5.2
  jako doradca wymaga według dokumentacji odpowiednio nowej wersji Claude Code. Rozszerzenie VS Code
  i osobny program w terminalu (`claude --version`) mogą mieć różne wersje, a w starszej nazwa `fable`
  wskazuje starszy model. Wersję sprawdzaj tam, gdzie zlecenie ruszy: autor sprawdził 25.11.2026 terminal
  zamiast rozszerzenia i błędnie uznał, że trzeba aktualizować program.
- **Włączenie doradcy nie mieści się w prompcie.** Włącza go tylko użytkownik poleceniem `/advisor fable` albo
  ustawieniem, dlatego jest osobną wiadomością do wklejenia. W prompcie stoi natomiast zdanie, kiedy model ma do niego
  sięgać (wstawka „Doradca” w `szablon-polecenia.md`), bo częstość sięgania ustawia się tylko słowami.

## Tryb

- **Tryb planowania**, gdy droga jest niejasna, zmiana dotyka wielu plików, działanie jest nieodwracalne
  albo wychodzi na zewnątrz, albo zadanie już raz stanęło. W tym trybie pomocnicy nie mogą niczego zapisać,
  więc do badania służą pomocnicy czytający, którzy oddają tekst.
- **Tryb auto**, gdy zadanie jest dokładnie opisane, odwracalne i ma sprawdzenie. Tryb auto zdejmuje pytania
  o zgodę na pojedyncze narzędzia, a `/goal` zdejmuje potrzebę popychania każdej tury; uzupełniają się.
- Trybu ani poziomu myślenia Claude nie ustawi sam. Robi to użytkownik, dlatego są etykietami, które ustawia
  ręcznie przed wklejeniem (`SKILL.md`, krok 7, od 26.11.2026), a nie zdaniami w treści polecenia.

## Jak pisać polecenie pod wybrany model

Wspólne dla wszystkich: mów wprost, czego chcesz; podawaj powód reguły; pisz, co robić, zamiast czego nie
robić; spokojny ton zamiast „KRYTYCZNE” i „MUSISZ”; „zmień” daje zmianę, „zaproponuj” daje tylko propozycję;
wszystkie stałe reguły idą w pierwszej wiadomości, bo dopisane w trakcie psują zapamiętany kontekst.

| Model | Co dopisać do polecenia |
| --- | --- |
| Opus 5.5 | Rusza do pracy szybko, więc przy luźno opisanym zadaniu każ mu najpierw szeroko przejrzeć źródła, także te, których zadanie nie wymienia. Nazwij zatrzymania, których nie chcesz (zapowiedź kroku bez wykonania, oferta „mogę kontynuować”, lista decyzji, które niczego nie blokują), i te, które są w porządku. Poproś o jedno zdanie zamiaru przed pierwszym narzędziem i podsumowanie na końcu. |
| Fable 5.2 | Na poziomach low i medium częściej kończy przed czasem, więc dodaj wstawkę „Dokończenie pracy”. Słowo „nigdy” traktuje bezwzględnie: zamiast „nigdy nie usuwaj plików” napisz „zapytaj o zgodę przed usunięciem plików”. Wymień konkretne działania wymagające zgody, bo ogólne „pytaj przed wysłaniem czegokolwiek” blokuje też rutynę. W długiej pracy milczy, więc poproś o jedno zdanie co kilka kroków. Zdanie „jesteś właścicielem tego kodu” wywołuje przebudowy i około 70–80% więcej tokenów: dodawaj je tylko, gdy użytkownik chce porządków. Zatwierdzenia pisz pełnym zdaniem, nie samym „tak”. |
| Sonnet 5.5 | Dodaj trzy zdania: pracuj, aż wszystko będzie zrobione, i pytaj tylko, gdy bez użytkownika nie da się iść dalej; gdy praca jest zrobiona i sprawdzona, zatrzymaj się i nie dodawaj testów, plików ani przebudów, o które nikt nie prosił; uruchom prawdziwe sprawdzenie zmiany, a gdy się nie da, napisz, którego nie uruchomiłeś i dlaczego. Do najtrudniejszej długiej pracy dokumentacja zaleca Opusa. |
| Haiku 5.5 | Podaj dzisiejszą datę. Zadanie ma być wąskie i w pełni opisane, z poleceniem, którym samo się sprawdzi. Na poziomie low częściej pomija sprawdzenie i kończy przed czasem. |

Nazwy poziomów (low, medium, high, xhigh, max) nie znaczą tego samego w różnych modelach. Domyślny poziom
w Claude Code to medium dla Opusa 5.5 i dla Fable 5.2.

## Źródła (odczyt 25.11.2026)

- https://platform.claude.com/docs/en/about-claude/models/choosing-a-model
- https://www.anthropic.com/claude-fable-and-mythos-5-2
- https://code.claude.com/docs/en/advisor
- https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
- https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5-5
- https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-2
- https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5
- https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-haiku-5-5
- https://platform.claude.com/docs/en/managed-agents/multiagent-orchestration (osobna usługa dla
  programistów, nie Claude Code; stąd tylko zasady: zlecaj części niezależne, wyspecjalizowane albo
  wymagające mocniejszego modelu, bo każdy pomocnik zużywa tokeny)

Ceny za milion tokenów (wejście / wyjście), odczyt 23.11.2026 z dokumentacji Anthropic: Fable 5.2
8 / 40 USD, Opus 5.5 4 / 20 USD, Sonnet 5.5 2 / 10 USD, Haiku 5.5 0,10 / 0,50 USD. Token Fable kosztuje
więc dwa razy tyle co token Opusa i cztery razy tyle co token Sonneta. Pomiary o kierowaniu pomocnikami
pochodzą z notatki autora z materiałów Anthropic (23.11.2026).
