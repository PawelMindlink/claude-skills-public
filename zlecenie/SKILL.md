---
name: zlecenie
description: Układa gotowe polecenie do zadania i mówi, jak je uruchomić — model, poziom myślenia, doradca, tryb planowania albo auto, zwykłe polecenie albo /goal, umiejętności do wpisania w polecenie. Najpierw sprawdza, czy zadanie było już podejmowane i dlaczego stanęło, proste sprawdzenie wykonuje od razu, a przy niejasnej drodze zadaje użytkownikowi pytania zamiast zgadywać. Używaj zawsze, gdy użytkownik prosi o polecenie dla nowej rozmowy albo innego agenta, pyta, na jakim modelu i poziomie coś uruchomić, czy to ma być /goal, albo opisuje duże zadanie, które chce komuś zlecić — także gdy nie pada słowo „prompt”. Zwroty użytkownika: daj prompt, model, poziom myślenia; przygotuj prompt dla nowego agenta; stwórz /goal; rozpisz /goal; przygotuj polecenie celu; czy to ma być /goal; na jakim modelu mam to uruchomić; jaki poziom myślenia ustawić; sonnet wystarczy; opus czy fable; tryb auto czy plan; wkleję to osobnemu agentowi; to zadanie znowu nie wyszło. Nie używaj do zamknięcia trwającej rozmowy, do pisania poleceń dla modeli obrazu ani do samej decyzji bez zlecania pracy.
---

# Zlecenie: polecenie i sposób jego uruchomienia

Zadania użytkownika rzadko wykładają się na słabym modelu. Wykładają się na tym, że nikt nie sprawdził, co już
próbowano, nikt nie dopytał o brakującą wiedzę, końca nie dało się sprawdzić, a droga do wyniku zginęła
po drodze. Ta umiejętność usuwa te cztery przyczyny, zanim praca ruszy, i dobiera najtańszy układ, który
jeszcze daje dobry wynik. Użytkownik chce najlepszej jakości przy możliwie małym koszcie, za pierwszym razem.

Użytkownik nie musi być programistą i nie ocenia poleceń na oko. Dostaje werdykt, kroki do przeklikania i blok do
wklejenia; o jakości rozstrzyga dziennik wyników, a nie jego opinia o tekście. Odpowiadasz po polsku.
Polecenie też jest po polsku.

## Kroki

### 1. Zamiar

Ustal dla siebie: co ma być prawdą na końcu i po czym to poznamy. Miarą jest wynik dla użytkownika (umówione
rozmowy, zysk, materiał gotowy do wysłania), a nie wykonana czynność. Tego nie wypisujesz użytkownikowi osobno:
trafia do sekcji „Cel” i „Gotowe, gdy” w poleceniu.

### 2. Historia

Sprawdź, czy to zadanie było już podejmowane. Tylko 3 z 14 dawnych poleceń celu użytkownika mówiły, co próbowano
wcześniej, i te same ślepe uliczki wracały po kilka razy.

Gdzie szukasz (czytaj spis, potem tylko pasujące pliki; miejsca, którego w projekcie nie ma, pomijasz):

- katalog pamięci projektu: `MEMORY.md`, pliki `ZLECENIE-*.md`, `HANDOFF*.md` (sekcja „Nie próbuj
  ponownie”), `active-goal-resume-*`, `goal-closed-*`, `*-stall-lessons-*`, `*-restart*`, `*-v2*`;
- w projekcie: `docs\hot.md`, `docs\LOG.md`, pliki z „goal” w nazwie;
- plik z Twoimi zapisanymi decyzjami, jeśli go prowadzisz (dopisz tu jego ścieżkę);
- zlecenia, które ruszyły i nie zapisały wyniku:
  `python3 -X utf8 ~/.claude/skills/zlecenie/scripts/dziennik.py wiszace` — powiedz o nich
  użytkownikowi jednym zdaniem i zapytaj, czym się skończyły, bo urwana rozmowa sama tego nie zapisze;
- `git log --oneline -20` z nazwą tematu, gdy projekt jest repozytorium.

Wynik tego kroku to trzy rzeczy: ile było podejść i kiedy, czym każde się skończyło, dlaczego stanęło.
Przyczynę przepisujesz z pliku, nie zgadujesz. Gdy nic nie znajdziesz, wymień sprawdzone miejsca i uznaj
zadanie za nowe. Przy dużym projekcie zleć ten krok pomocnikowi z `model: sonnet`.

Każdą przyczynę zastoju przypisz do jednej z czterech klas, bo od klasy zależy, co trzeba zmienić. Mocniejszy
model pomaga tylko w dwóch z nich:

| Klasa przyczyny | Po czym poznasz | Co zmieniasz |
| --- | --- | --- |
| Granica zewnętrzna | Popytu, dostępu albo danych nie ma, niezależnie od jakości pracy. | Nie zlecasz. Żaden model tego nie zmieni; proponujesz inny cel albo zamknięcie tematu. |
| Zgody | Gotowa praca czekała na decyzje użytkownika. | Układ zostaje. Zmieniasz zasady zgód: jedna zgoda na cały rodzaj działań i nazwany warunek zakończenia. |
| Zły plan | Praca była wykonana poprawnie, ale nie prowadziła do celu. | Diagnozę i plan robi mocniejszy model w osobnej rozmowie. |
| Wykonanie | Błędy, niska jakość, niedokończone kroki przy dobrym planie. | Jeden szczebel wyżej niż model, który pracował poprzednio. Sprawdź go w dzienniku albo w zapisach rozmów, zamiast zakładać. |

Przykład: zadanie z wyszukiwarką prowadziły kolejno dwa różne modele i żaden nie przyniósł klientów.
Audyt wskazał popyt (typowa fraza miała kilka wyświetleń w miesiącu), czyli granicę zewnętrzną,
a wcześniej dwa miesiące zeszły na zgodach. Wybór modelu niczego tu nie rozstrzygał, więc poprawną
odpowiedzią było „nie zlecaj kolejnej budowy stron”, a nie nowe polecenie.

### 3. Rodzaj zadania

| Rodzaj | Po czym poznasz | Co robisz |
| --- | --- | --- |
| Proste sprawdzenie | Jedno pytanie o fakt, odczyt z pliku albo z konta, nic nie powstaje. | Wykonujesz od razu pomocnikiem na Sonnecie albo sam, gdy to jedno wywołanie. Podajesz wynik i źródło. Polecenia nie układasz. |
| Wykonanie według opisu | Wiadomo dokładnie, co ma powstać i jak to sprawdzić. | Kroki 5–7. |
| Budowa z podzadaniami | Kilka części, część niezależnych od siebie. | Kroki 4–7, wstawka „Podzadania”. |
| Niejasna droga | Użytkownik zna cel, ale nie zna drogi albo sam mówi, że nie wie, jak to opisać. | Krok 4 jest obowiązkowy; układ według cech z `references\modele.md`. |
| Po nieudanych podejściach | Krok 2 znalazł co najmniej jedno podejście, które stanęło. | Układ według klasy przyczyny z kroku 2, plus wstawka „Po nieudanych podejściach”. |
| Oceniane okiem | Wygląd strony, panelu, prezentacji, reklamy. | Dodatkowo wstawka „Zadanie oceniane okiem”. |

Jedno zadanie może należeć do kilku rodzajów. Bierzesz wtedy wszystkie pasujące wstawki.

### 4. Pytania do użytkownika

Pytania dzielisz na dwie grupy, żeby użytkownik zawsze wiedział, gdzie odpowiada:

- **Pytanie, od którego zależy werdykt albo układ** (czy w ogóle zlecać, który model, czy `/goal`),
  zadajesz tutaj, jedno, z własnym zaleceniem, i czekasz na odpowiedź. Bloku jeszcze nie pokazujesz.
- **Pozostałe pytania** wpisujesz do polecenia jako „Pytania na start”: zada je nowa rozmowa, zanim
  cokolwiek zmieni. W odpowiedzi do użytkownika ich nie powtarzasz.

Do polecenia jako fakt wpisujesz tylko to, co użytkownik powiedział albo co stoi w pliku. Kto wybiera i ocenia
wynik, na jakim ekranie i w jakiej sytuacji jest używany, czemu ma służyć i czego nie wolno, to nie są
rzeczy do zgadnięcia: gdy nie padły, idą do „Pytań na start”. Reguły domyślnej (na przykład „najpierw
telefon” albo „materiały prywatne nie na konto firmowe bez zgody”) nie zamieniasz w zakaz w poleceniu;
wpisujesz ją jako pytanie o zgodę. W jednej z prób wpisałem do polecenia, kto wybiera wynik,
że ekran jest na telefon i że artefakty są zakazane, a żadna z tych trzech rzeczy nie była prawdą.

Najczęściej brakuje czterech rzeczy: miary sukcesu w liczbie albo w stanie, który widać; wzoru „dobrze”
przy zadaniu ocenianym okiem; listy działań czekających na zgodę; granicy, po której praca ma się
zatrzymać i zameldować.

Gdy użytkownik nie umie jeszcze nazwać celu albo wybiera między kierunkami, nie układaj polecenia na domysłach.
Powiedz to wprost i wywołaj swoją umiejętność do decyzji (decyzja, kierunek, model biznesowy) albo
`superpowers:brainstorming` (coś do zbudowania). Polecenie układasz po tej rozmowie.

Gdy pracujesz bez użytkownika (uruchomienie próbne, pomocnik), przyjmij własne zalecenie jako założenie, zapisz
je jednym zdaniem i idź dalej.

### 5. Układ wykonania

Przeczytaj `references\modele.md` i wybierz: model, poziom myślenia, doradcę, tryb oraz to, czy praca idzie
w jednej rozmowie, czy w dwóch (diagnoza i plan osobno, wykonanie osobno). Przeczytaj `references\goal.md`,
zanim wskażesz `/goal`.

Wybór wynika z czterech cech zadania opisanych w `references\modele.md` i z dziennika wyników, a nie
z wrażenia, że zadanie „wymaga osądu”. Gdy podobne zadania kończyły się w dzienniku bez wyniku na danym
układzie, weź szczebel wyżej; gdy kończyły się wynikiem, zostań przy nim albo spróbuj szczebla niżej.
Gdy dziennika jeszcze nie ma albo nie ma w nim podobnych zadań, decydują same cechy.

### 6. Polecenie

Złóż je ze szkieletu i wstawek w `references\szablon-polecenia.md`. Nazwy umiejętności bierzesz
z `references\dobor-umiejetnosci.md` i sprawdzasz na liście dostępnej w tej rozmowie: przepisujesz nazwę
dosłownie, bo zgadnięta nazwa zawiedzie po cichu.

Polecenie pisze się dla czytelnika, który nie zna tej rozmowy: pełne ścieżki, fakty wpisane wprost zamiast
„jak ustaliliśmy”, powód przy każdej regule. Ton jest spokojny, bez wersalików i bez „MUSISZ”: nowe modele
reagują na krzyk nadgorliwością. Ostatnim akapitem jest zawsze wstawka „Zapis wyniku”: przed oddaniem
zakładasz wiersz w dzienniku programem `scripts\dziennik.py start` i wpisujesz jego numer do polecenia.

Gdy polecenie przekracza około 2500 znaków albo praca idzie przez `/goal`, zapisz pełną treść w pliku
`ZLECENIE-<temat>.md` w katalogu pamięci projektu (jego ścieżka stoi w poleceniach systemowych rozmowy,
w sekcji o pamięci; gdy jej tam nie ma, zapisz plik w katalogu projektu) i dopisz
linię do `MEMORY.md`:
`- [Zlecenie](ZLECENIE-<temat>.md) — <cel w kilku słowach>; uruchomione <RRRR-MM-DD>.`
Polecenie do wklejenia jest wtedy krótkie i wskazuje ten plik pełną ścieżką. Zanim oddasz odpowiedź,
sprawdź, że plik istnieje dokładnie pod ścieżką wpisaną w poleceniu.

### 7. Oddanie

Odpowiedź ma jedną z trzech postaci. Poza blokiem mieści się w 150 słowach.

**Nie zlecać.** Jedno zdanie powodu pełnym zdaniem („ruch z wyszukiwarki nie przyniesie więcej niż
jednego klienta miesięcznie, bo typowa fraza ma kilka wyświetleń w miesiącu”), źródło tej liczby i jeden inny cel, który
proponujesz. Bez bloku i bez polecenia.

**Najpierw pytanie.** Jedno pytanie z kroku 4 z własnym zaleceniem. Bez bloku.

**Zlecać.** Jedno zdanie werdyktu, najwyżej cztery wiersze historii, potem blok:

~~~
Ścieżka: <pełna ścieżka katalogu>
Model: <opus | sonnet | fable>
Poziom: <low | medium | high | xhigh>
Tryb: <PLAN | AUTO | PLAN, po zatwierdzeniu drogi AUTO>
Doradca: fable, po pracy wyłącz
ULTRACODE ON
Forma: /goal

Prompt:
<treść>
~~~

Gdy użytkownik ma coś dołączyć do promptu (zrzut ekranu, plik, czyjąś odpowiedź), dopisz w nagłówku wiersz
`Załącz: <co>` i nie pisz w prompcie w pierwszej osobie, że to zrobił. Użytkownik nie czyta promptu, więc
zdanie „wzorem jest zrzut, który wkleiłem” jest nieprawdą, jeśli go nie wkleił: W jednej z prób rozmowa
o panelu zapytała o brakujący zrzut, użytkownik nie wiedział, o co chodzi, i zeszło na to 16 minut. Pisz
warunkowo: „jeśli dołączyłem zrzut, jest wzorem; jeśli nie, zapytaj mnie o jeden panel, który mi się
podoba, i wyjaśnij, do czego go potrzebujesz”.

Prompt nie zawiera pól do uzupełnienia w rodzaju „[TAK / NIE]”. Użytkownik wkleja prompt bez czytania, więc
puste pola trafiają do rozmowy wykonującej, a ona i tak zadaje te pytania od nowa (w jednej z prób:
pięć pustych pól i runda czterech pytań mimo zdania „nie zadawaj ich od nowa”). Decyzję, którą znasz
z góry, rozstrzygasz z użytkownikiem przed oddaniem bloku (narzędziem do pytań, z zaleceniem) i wpisujesz do
promptu jako gotową odpowiedź. Decyzję, której nie da się zadać z góry, zostawiasz w „Pytaniach na start”.
Gdy użytkownik odpowiada inaczej, niż zakłada granica w prompcie (na przykład dokłada zakres), rozmowa
wykonująca ma powiedzieć mu, że to zmienia granicę, zanim ruszy.

Ten układ ustalił użytkownik 25.11.2026: same etykiety i wartości, bez zdań i bez instrukcji klikania. Trzy
ostatnie wiersze nagłówka pokazujesz tylko wtedy, gdy dana rzecz ma być włączona; gdy nie, wiersza nie ma
wcale. Nie piszesz „bez doradcy” ani „krok pomiń”.

- **Doradca** to drugi, mocniejszy model, do którego model wykonujący sam sięga przed wyborem podejścia
  i przed ogłoszeniem końca (`/advisor fable`, potem `/advisor off`). Gdy wiersz się pojawia pierwszy raz
  w rozmowie z użytkownikiem, dopisz pod blokiem to jedno zdanie wyjaśnienia.
- **ULTRACODE ON** (`/effort ultracode on`) każe rozmowie rozbijać każde większe zadanie na wielu
  pomocników naraz i sprawdzać ich nawzajem, bez liczenia tokenów. Wskazujesz to tylko dla pracy, która
  dzieli się na wiele niezależnych części i w której pominięcie czegokolwiek kosztuje więcej niż tokeny
  (szeroki audyt, migracja, przegląd dużej zmiany). Przy zwykłej pracy, przy rozmowie z użytkownikiem o kierunku
  i przy zadaniu ocenianym okiem wiersza nie ma.
- **Forma: /goal** oznacza, że użytkownik wpisuje ręcznie `/goal `, wkleja prompt jako warunek, a potem samym
  `/goal` sprawdza, że cel jest aktywny. Ten wiersz stoi tylko obok „Tryb: AUTO” i tylko wtedy, gdy prompt
  nie ma „Pytań na start”. Gdy zadanie potrzebuje planu albo pytań, dajesz zwykły prompt w trybie PLAN,
  a warunek dla `/goal` rozmowa poda użytkownikowi po zatwierdzeniu drogi.

Pod blokiem jedno zdanie: które cechy zadania zdecydowały o układzie. Na końcu pełna ścieżka pliku
zlecenia, jeśli powstał.

Zasady tej odpowiedzi:

- Historię piszesz zdaniami, nie etykietami: „stanęło, bo kilkanaście szkiców czekało na Twoje zgody”, a nie
  „klasa: zgody”. Nazwy klas i szczebli są dla Ciebie, nie dla użytkownika.
- Liczba ma jednostkę i źródło. Terminu z wnętrza projektu nie zostawiasz bez wyjaśnienia.
- Katalog w kroku 1 to ten, w którym użytkownik prowadzi rozmowy o tym projekcie i w którym leży jego
  `CLAUDE.md`, bo stamtąd wczytują się zasady projektu. Sprawdź to, zanim go wpiszesz: policz zapisy rozmów
  w `~/.claude/projects/<nazwa katalogu z myślnikami>/*.jsonl`. Nie bierz katalogu z nazwy
  folderu pamięci, w którym leży przekazanie: pamięć bywa wspólna dla całego repozytorium (w jednej
  z prób wskazałem przez to katalog nadrzędny zamiast katalogu projektu, który miał ponad 200 rozmów
  i własne zasady).
- Trybu i poziomu myślenia Claude nie ustawi sam, dlatego stoją w nagłówku bloku, a nie w treści promptu.
- Polecenia `/model`, `/effort` (w tym `ultracode on`) i `/advisor` istnieją (sprawdzone 25.11.2026).
  Użytkownik wie, jak je ustawić, więc nie opisujesz tego w odpowiedzi. Gdy blok ma wiersz „Doradca”, prompt
  zawiera wstawkę „Doradca”, która mówi modelowi, kiedy ma do niego sięgać.
- Przy układzie dwóch rozmów pokazujesz kroki i polecenie dla pierwszej. Drugie polecenie układa pierwsza
  rozmowa na końcu swojej pracy, bo dopiero ona zna plan.

## Kalibracja

Gdy użytkownik pisze „skalibruj zlecenie”, „sprawdź, jak poszły zlecenia” albo gdy dziennik ma co najmniej trzy
zamknięte wiersze od ostatniej kalibracji, popraw umiejętność na podstawie przebiegów, a nie opinii:

1. Uruchom `python3 -X utf8 ~/.claude/skills/zlecenie/scripts/dziennik.py podsumowanie` oraz
   `wiszace`. O zlecenia bez wyniku zapytaj użytkownika jednym pytaniem.
2. Zleć pomocnikowi z `model: sonnet` przeczytanie zapisów rozmów zamkniętych zleceń (katalog
   `~/.claude/projects/<katalog projektu z myślnikami>/`, pliki `.jsonl` z dnia zlecenia;
   szukać po pierwszym zdaniu polecenia). Ma oddać dla każdego: ile pytań zadała rozmowa przed pracą,
   gdzie użytkownik poprawiał kierunek i jakimi słowami, gdzie rozmowa stanęła, czy sprawdzenie końcowe
   faktycznie zostało uruchomione.
3. Każdą poprawkę użytkownika przypisz do przyczyny w poleceniu: brakujący fakt, zła wstawka, zły układ, zły
   katalog. Zmień plik umiejętności, który tę przyczynę usuwa, i dopisz datę oraz zdarzenie jednym zdaniem.
4. Progi przejścia szczebel wyżej i drabinę w `references\modele.md` zmieniaj dopiero przy dziesięciu
   zamkniętych wierszach; wcześniej to za mało danych.

Kalibrację rób w nowej rozmowie, nie w tej, która układała polecenia.

## Czego nie robisz

- Nie układasz polecenia dla prostego sprawdzenia. Odpowiedź jest tańsza niż zlecenie.
- Nie układasz polecenia, gdy przyczyną zastoju jest granica zewnętrzna.
- Nie wskazujesz Opusa 5.5 na poziomie max, a xhigh tylko do długiego programowania według specyfikacji
  z testami. Powód stoi w `references\modele.md`.
- Nie wpisujesz do polecenia umiejętności „na wszelki wypadek”. Każda nazwa ma krok, którym rządzi.
- Nie zostawiasz warunku końca w rodzaju „SEO działa”. Koniec ma sprawdzenie, które widać w rozmowie.
- Nie uruchamiasz dużej pracy sam w tej rozmowie. Długa rozmowa czyta całą swoją historię przy każdym
  kroku, więc nowa rozmowa z gotowym poleceniem kosztuje kilka razy mniej.
