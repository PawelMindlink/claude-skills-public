---
name: zlecenie
description: Układa gotowe polecenie do zadania i mówi, jak je uruchomić — model, poziom myślenia, doradca, tryb planowania albo auto, zwykłe polecenie albo /goal, umiejętności do wpisania w polecenie. Najpierw sprawdza, czy zadanie było już podejmowane i dlaczego stanęło; proste sprawdzenie albo drobną resztę robi od razu, a o brakującą wiedzę pyta użytkownika zamiast zgadywać. Używaj zawsze, gdy użytkownik prosi o polecenie dla nowej rozmowy albo innego agenta, pyta, na jakim modelu i poziomie coś uruchomić, czy to ma być /goal, albo chce komuś zlecić duże zadanie — także bez słowa „prompt”. Zwroty użytkownika: daj prompt, model, poziom myślenia; przygotuj prompt dla nowego agenta; stwórz /goal; przygotuj polecenie celu; na jakim modelu mam to uruchomić; jaki poziom myślenia ustawić; opus czy fable; tryb auto czy plan; to zadanie znowu nie wyszło. Nie używaj do zamknięcia trwającej rozmowy, do pisania poleceń dla modeli obrazu ani do samej decyzji bez zlecania pracy.
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

Sprawdź, czy to zadanie było już podejmowane. U autora tej umiejętności mniej niż co czwarte dawne polecenie celu
mówiło, co próbowano wcześniej, i te same ślepe uliczki wracały po kilka razy.

Gdzie szukasz (czytaj spis, potem tylko pasujące pliki; miejsca, którego w projekcie nie ma, pomijasz):

- katalog pamięci projektu: `MEMORY.md`, pliki `ZLECENIE-*.md`, `HANDOFF*.md` (sekcja „Nie próbuj
  ponownie”), `active-goal-resume-*`, `goal-closed-*`, `*-stall-lessons-*`, `*-restart*`, `*-v2*`;
- w projekcie: `docs/hot.md`, `docs/LOG.md`, pliki z „goal” w nazwie, katalog `.superpowers/sdd/`
  (specyfikacje i plany z umiejętności superpowers);
- pamięć w katalogu domowym: `~/.claude/projects/*/memory/` także katalogów o podobnej
  nazwie, bo repozytorium przeniesione albo otwierane z podkatalogu zostawia pamięć pod starą nazwą
  (26.11.2026, recenzja zewnętrznego testera: w jednym zadaniu odpowiedź leżała w `.superpowers/sdd/`
  i w pamięci z katalogu domowego, a lista nie wymieniała tych miejsc);
- plik z Twoimi zapisanymi decyzjami, jeśli go prowadzisz (dopisz tu jego ścieżkę);
- zlecenia, które ruszyły i nie zapisały wyniku:
  `python3 -X utf8 ~/.claude/skills/zlecenie/scripts/dziennik.py wiszace` — powiedz o nich
  użytkownikowi jednym zdaniem i zapytaj, czym się skończyły, bo urwana rozmowa sama tego nie zapisze;
- `git log --oneline -20` z nazwą tematu, gdy projekt jest repozytorium.

Wynik tego kroku to trzy rzeczy: ile było podejść i kiedy, czym każde się skończyło, dlaczego stanęło.
Przyczynę przepisujesz z pliku, nie zgadujesz. Gdy nic nie znajdziesz, wymień sprawdzone miejsca i uznaj
zadanie za nowe. Przy dużym projekcie zleć ten krok pomocnikowi z `model: sonnet`.

Pliki nie mówią, co użytkownik ma poza nimi. Gdy znalazłeś tylko streszczenie, odwołanie do dokumentu, którego
nie ma na dysku, albo fakt, który może stać w kilku miejscach materiału, pytasz go, gdzie leży pełny tekst
(pytanie z kroku 4, przed oddaniem). Fakt z kilku miejsc wpisujesz do polecenia razem z poleceniem
znalezienia wszystkich wystąpień. 26.11.2026 (recenzja zewnętrznego testera, poprawka manuskryptu):
zlecenie pytało o wersję w jednym miejscu, choć tekst miał ją w trzech, i jako źródło podało streszczenie,
choć pełny tekst leżał u zlecającego; zeszły na to dwie dodatkowe rundy pytań.

Każdą przyczynę zastoju przypisz do jednej z pięciu klas, bo od klasy zależy, co trzeba zmienić. Mocniejszy
model pomaga tylko w dwóch z nich:

| Klasa przyczyny | Po czym poznasz | Co zmieniasz |
| --- | --- | --- |
| Granica zewnętrzna | Popytu, dostępu albo danych nie ma, niezależnie od jakości pracy. | Nie zlecasz. Żaden model tego nie zmieni; proponujesz inny cel albo zamknięcie tematu. |
| Zgody | Gotowa praca czekała na decyzje użytkownika. | Układ zostaje. Zmieniasz zasady zgód: jedna zgoda na cały rodzaj działań i nazwany warunek zakończenia. |
| Zły plan | Praca była wykonana poprawnie, ale nie prowadziła do celu. | Diagnozę i plan robi mocniejszy model w osobnej rozmowie. |
| Wykonanie | Błędy, niska jakość, niedokończone kroki przy dobrym planie. | Jeden szczebel wyżej niż model, który pracował poprzednio. Sprawdź go w dzienniku albo w zapisach rozmów, zamiast zakładać. |
| Odłożone | Nikt tego nie próbował: temat odłożono świadomie (decyzja, kolejność prac, czekanie na dane). | Zadanie traktujesz jak nowe, ale najpierw sprawdzasz, czy powód odłożenia nadal trwa. Gdy trwa, nie zlecasz i mówisz, na co zadanie czeka. |

Klasa „odłożone” dodana 26.11.2026: w recenzji zewnętrznego testera w dwóch z trzech zadań żadna z czterech
dawnych klas nie pasowała, bo zadań nikt wcześniej nie próbował.

Przykład: zadanie z wyszukiwarką prowadziły kolejno dwa różne modele i żaden nie przyniósł klientów.
Audyt wskazał popyt (typowa fraza miała kilka wyświetleń w miesiącu), czyli granicę zewnętrzną,
a wcześniej dwa miesiące zeszły na zgodach. Wybór modelu niczego tu nie rozstrzygał, więc poprawną
odpowiedzią było „nie zlecaj kolejnej budowy stron”, a nie nowe polecenie.

### 3. Rodzaj zadania

| Rodzaj | Po czym poznasz | Co robisz |
| --- | --- | --- |
| Proste sprawdzenie | Jedno pytanie o fakt, odczyt z pliku albo z konta, nic nie powstaje. | Wykonujesz od razu pomocnikiem na Sonnecie albo sam, gdy to jedno wywołanie. Podajesz wynik i źródło. Polecenia nie układasz. |
| Drobna reszta | Zostały najwyżej trzy małe kroki: zmiana jednego ustawienia, decyzja użytkownika, próba, której jeszcze nie da się zmierzyć. | Nie zlecasz. To, co da się zrobić od razu, robisz albo podajesz gotowe; resztę wymieniasz z tym, na co czeka (postać „Nie zlecać” w kroku 7). |
| Wykonanie według opisu | Wiadomo dokładnie, co ma powstać i jak to sprawdzić. | Kroki 5–7. |
| Budowa z podzadaniami | Kilka części, część niezależnych od siebie. | Kroki 4–7, wstawka „Podzadania”. |
| Niejasna droga | Użytkownik zna cel, ale nie zna drogi albo sam mówi, że nie wie, jak to opisać. | Krok 4 jest obowiązkowy; układ według cech z `references/modele.md`. |
| Po nieudanych podejściach | Krok 2 znalazł co najmniej jedno podejście, które stanęło. | Układ według klasy przyczyny z kroku 2, plus wstawka „Po nieudanych podejściach”. |
| Oceniane okiem | Wygląd strony, panelu, prezentacji, reklamy. | Dodatkowo wstawka „Zadanie oceniane okiem”. |

Jedno zadanie może należeć do kilku rodzajów. Bierzesz wtedy wszystkie pasujące wstawki.

Rodzaj „drobna reszta” dodany 26.11.2026 (recenzja zewnętrznego testera, audyt konfiguracji): umiejętność
zrobiła od razu dwa z trzech sprawdzeń, a resztę, czyli jedną zmianę ustawień, jedną decyzję i jedną próbę
jeszcze niemierzalną, i tak zleciła na Opusie high w trybie planu, z plikiem zlecenia na 9 KB.

### 4. Pytania do użytkownika

Pytania dzielisz jedną regułą: o to, co zmienia sam blok, pytasz przed oddaniem; o to, na co da się
odpowiedzieć dopiero po przeczytaniu materiału albo w trakcie pracy, pyta rozmowa wykonująca.

- **Pytania, od których zależy blok**: czy w ogóle zlecać, układ (model, poziom, tryb, `/goal`), katalog,
  lista zgód, gdzie leży pełny tekst źródła. Zadajesz je tutaj wszystkie naraz, jednym wywołaniem narzędzia
  do pytań, każde z własnym zaleceniem, i czekasz na odpowiedź. Bloku jeszcze nie pokazujesz. Odpowiedzi
  wpisujesz do polecenia jako gotowe.
- **Pytania, które wymagają materiału**, wpisujesz do polecenia jako „Pytania na start”: zada je nowa
  rozmowa, zanim cokolwiek zmieni. W odpowiedzi do użytkownika ich nie powtarzasz.

Przykład z dziennika (zlecenie 19, 26.11.2026): to, czy wysłanie odpowiedzi do recenzenta czeka na zgodę,
zmienia sekcję „Zgody”, więc pada przed oddaniem; to, które uwagi recenzenta odrzucić, wymaga porównania
dwóch wersji umiejętności, więc idzie do „Pytań na start”. Reguła z 26.11.2026 zastąpiła dwie sprzeczne:
krok 4 kazał zadać jedno pytanie, a krok 7 rozstrzygnąć z góry wszystko, co znane (uwaga 4 zewnętrznego
testera).

Do polecenia jako fakt wpisujesz tylko to, co użytkownik powiedział albo co stoi w pliku. Kto wybiera i ocenia
wynik, na jakim ekranie i w jakiej sytuacji jest używany, czemu ma służyć i czego nie wolno, to nie są
rzeczy do zgadnięcia: gdy nie padły, idą do „Pytań na start”. Reguły domyślnej (na przykład „najpierw
telefon” albo „materiały prywatne nie na konto firmowe bez zgody”) nie zamieniasz w zakaz w poleceniu;
wpisujesz ją jako pytanie o zgodę. W jednej z prób wpisałem do polecenia, kto wybiera wynik,
że ekran jest na telefon i że artefakty są zakazane, a żadna z tych trzech rzeczy nie była prawdą.

Do „Pytań na start” nie wpisujesz tego, co da się sprawdzić w plikach, poczcie, kalendarzu albo danych:
sprawdzasz sam albo każesz to sprawdzić rozmowie wykonującej. Nie wpisujesz też własnej propozycji jako
gotowej decyzji, której nie sprawdziłeś z użytkownikiem. 25.11.2026 zlecenie wersjonowania podsunęło nazwę
`claude-code-skills` i pytało o godzinę automatu; autor odrzucił nazwę i kazał godzinę sprawdzić samemu.

Przy przebudowie czegoś, czego użytkownik już używa, wpisujesz do polecenia, co w starym rozwiązaniu działa
i ma zostać, a gdy tego nie wiesz, stawiasz to jako pierwsze pytanie na start. 25.11.2026 ekran budżetu
zgubił tabelę „plan, wykonanie, różnica”, którą autor cenił w arkuszu.

Najczęściej brakuje czterech rzeczy: miary sukcesu w liczbie albo w stanie, który widać; wzoru „dobrze”
przy zadaniu ocenianym okiem; listy działań czekających na zgodę; granicy, po której praca ma się
zatrzymać i zameldować.

Gdy użytkownik nie umie jeszcze nazwać celu albo wybiera między kierunkami, nie układaj polecenia na domysłach.
Powiedz to wprost i wywołaj swoją umiejętność do decyzji (decyzja, kierunek, model biznesowy) albo
`superpowers:brainstorming` (coś do zbudowania). Polecenie układasz po tej rozmowie.

Gdy pracujesz bez użytkownika (uruchomienie próbne, pomocnik), przyjmij własne zalecenie jako założenie, zapisz
je jednym zdaniem i idź dalej.

### 5. Układ wykonania

Przeczytaj `references/modele.md` i wybierz rolę z „Drabiny ról”, a z niej: model, poziom myślenia, doradcę, tryb oraz to, czy praca idzie
w jednej rozmowie, czy w dwóch (diagnoza i plan osobno, wykonanie osobno). Przeczytaj `references/goal.md`,
zanim wskażesz `/goal`. Gdy polecenie zleca czytanie dużej ilości tekstu albo wykonanie według opisu ze
sprawdzeniem poleceniem, przeczytaj `references/gemini.md`: taką część może zrobić Gemini bez limitu Claude.

Wybór wynika z czterech cech zadania opisanych w `references/modele.md` i z dziennika wyników, a nie
z wrażenia, że zadanie „wymaga osądu”. Gdy podobne zadania kończyły się w dzienniku bez wyniku na danym
układzie, weź szczebel wyżej; gdy kończyły się wynikiem, zostań przy nim albo spróbuj szczebla niżej.
Gdy dziennika jeszcze nie ma albo nie ma w nim podobnych zadań, decydują same cechy.

### 6. Polecenie

Złóż je ze szkieletu i wstawek w `references/szablon-polecenia.md`. Nazwy umiejętności bierzesz
z `references/dobor-umiejetnosci.md` i sprawdzasz na liście dostępnej w tej rozmowie: przepisujesz nazwę
dosłownie, bo zgadnięta nazwa zawiedzie po cichu.

Polecenie pisze się dla czytelnika, który nie zna tej rozmowy: pełne ścieżki, fakty wpisane wprost zamiast
„jak ustaliliśmy”, powód przy każdej regule. Ton jest spokojny, bez wersalików i bez „MUSISZ”: nowe modele
reagują na krzyk nadgorliwością. Ostatnim akapitem jest zawsze wstawka „Zapis wyniku”: przed oddaniem
zakładasz wiersz w dzienniku programem `scripts/dziennik.py start` i wpisujesz jego numer do polecenia.
`--rodzaj` to rodzaj główny z kroku 3 (wykonanie wedlug opisu, budowa z podzadaniami, niejasna droga, po
nieudanych podejsciach), przy ocenie okiem z dopiskiem „ + oceniane okiem”; program odrzuca inne wartości,
bo 26.11.2026 wolny tekst dał 16 rodzajów na 20 wierszy i `podsumowanie` niczego nie porównywało.
Gdy pasuje kilka rodzajów, wpisujesz ten, który wyznacza rolę w `references/modele.md`, w kolejności: po
nieudanych podejsciach, niejasna droga, budowa z podzadaniami, wykonanie wedlug opisu. Ostrzeżenie o długości
liczy cały plik, więc przy dołączonym tekście źródłowym sprawdzasz `len()` bez niego i ostrzeżenie pomijasz,
gdy reszta mieści się w progu.

Gdy polecenie przekracza około 2500 znaków albo praca idzie przez `/goal`, zapisz pełną treść w pliku
`ZLECENIE-<temat>.md` w katalogu pamięci projektu (jego ścieżka stoi w poleceniach systemowych rozmowy,
w sekcji o pamięci; gdy jej tam nie ma, zapisz plik w katalogu projektu) i dopisz
linię do `MEMORY.md`:
`- [Zlecenie](ZLECENIE-<temat>.md) — <cel w kilku słowach>; uruchomione <RRRR-MM-DD>.`
Polecenie do wklejenia jest wtedy krótkie i wskazuje ten plik pełną ścieżką. Wiersz w dzienniku zakładasz
wtedy z `--plik <ta ścieżka>`: program odmawia, gdy pliku pod nią nie ma, i ostrzega, gdy plik przekracza
progi długości z następnego akapitu.

Plik zlecenia w chwili oddania ma najwyżej około 4000 znaków przy wykonaniu według opisu i około 7000 przy
pozostałych rodzajach, nie licząc dołączonego tekstu źródłowego (policz `len()` w Pythonie). Nadmiar
skracasz w „Co już wiadomo”: fakt, który rozmowa wykonująca przeczyta jednym odczytem pliku, zastępujesz
ścieżką i zdaniem, po co go czytać. Wstawki bierzesz tylko wtedy, gdy zachodzi ich warunek: zadanie na
kilka tur według opisu nie dostaje „Pierwszego etapu”, „Podzadań” ani „Dokończenia pracy”. Próg
z 26.11.2026: zewnętrzny tester zauważył, że każdy plik miał około 9 KB, także przy zadaniach na kilka tur,
a pomiar 14 plików `ZLECENIE-*.md` z 25–26.11 pokazał, że stałe wstawki zajmowały w nich średnio około
3600 znaków. Zlecenia 11 i 13 z plikami na 4,0 i 4,4 tys. znaków doszły do wyniku.

### 7. Oddanie

Odpowiedź ma jedną z trzech postaci. Poza blokiem mieści się w 150 słowach.

**Nie zlecać.** Jedno zdanie powodu pełnym zdaniem („ruch z wyszukiwarki nie przyniesie więcej niż
jednego klienta miesięcznie, bo typowa fraza ma kilka wyświetleń w miesiącu”). Przy granicy zewnętrznej dodajesz źródło tej
liczby i jeden inny cel, który proponujesz. Przy drobnej reszcie albo zadaniu odłożonym wymieniasz kroki,
które zostały, z tym, na co każdy czeka. Bez bloku i bez polecenia.

**Najpierw pytania.** Pytania z kroku 4, wszystkie naraz, każde z własnym zaleceniem. Bez bloku.

**Zlecać.** Jedno zdanie werdyktu, najwyżej cztery wiersze historii, potem etykiety i linie do wklejenia.

Etykiety użytkownik ustawia ręcznie w nowej rozmowie, zanim cokolwiek wklei (decyzja autora z 26.11.2026). Podajesz
je zawsze, także gdy pokrywają się z jego ustawieniami domyślnymi:

~~~
Ścieżka: <pełna ścieżka katalogu, w którym otwiera nową rozmowę>
Model: <opus | sonnet | fable>
Poziom: <low | medium | high | xhigh>, a przy ULTRACODE dopisek „+ /effort ultracode on”
Tryb: <AUTO | PLAN>
~~~

Pod etykietami stoją najwyżej dwie wiadomości, każda z podpisem „Wiadomość 1:”, „Wiadomość 2:”. Użytkownik
wysyła następną dopiero po potwierdzeniu programu:

1. Gdy ma być doradca: blok kodu z `/advisor fable` do wklejenia. Program odpowiada „Advisor set to …”.
2. Polecenie pracy, w jednej z dwóch postaci:
   - przy celu: zdanie „Wpisz ręcznie /goal ze spacją, potem wklej:” i blok kodu z samym warunkiem,
     bez słowa `/goal`, w jednym wierszu; policz znaki (`len()` w Pythonie), zmieść się w 4000, celuj
     w około 1500. Program odpowiada „Goal set: …”; gdy tego nie ma, cel nie działa;
   - bez celu: zwykły prompt w bloku kodu, może mieć wiele wierszy.

Przy pierwszym oddaniu w rozmowie powiedz jednym zdaniem, dlaczego tak: jedna wiadomość uruchamia
najwyżej jedno polecenie z ukośnikiem, a długi wklejony tekst Claude Code zapisuje jako wklejoną treść,
więc `/goal` na jego początku nie działa.

Dlaczego tak (audyt zapisów rozmów autora tej umiejętności z jesieni 2026; u siebie sprawdzisz to samo
w kalibracji):
- model nie wykona `/model`, `/effort` ani `/advisor` z treści promptu, bo to polecenia programu;
- 19 prób od 25.10 do 14.11.2026 i jedna z 26.11 (wklejony sam wiersz `/goal …`) program zapisał jako
  wklejoną treść i po żadnej nie wypisał „Goal set”;
- 26.11 autor wkleił `/advisor fable` i `/goal …` jedną wiadomością: program wziął całą resztę za nazwę
  modelu doradcy i nie ustawił niczego. Krótki wklejony `/advisor fable` osobno zadziałał;
- jedyna próba zapisana jako polecenie z długim warunkiem (13.11) zaczynała się od `/goal` w polu, a reszta
  była wklejona; odrzucił ją tylko limit 4000 znaków.
Autor chciał 26.11 jednego bloku wklejanego naraz; odrzucone, bo dokładnie to zawiodło tego dnia.
W programie (w wersji sprawdzonej przez autora) istnieje też ustawienie `advisorModel`; nie używasz go, bo w pliku ustawień
włączyłoby doradcę we wszystkich rozmowach użytkownika.

Gdy użytkownik ma coś dołączyć do promptu (zrzut ekranu, plik, czyjąś odpowiedź), dopisz w nagłówku wiersz
`Załącz: <co>` i nie pisz w prompcie w pierwszej osobie, że to zrobił. Użytkownik nie czyta promptu, więc
zdanie „wzorem jest zrzut, który wkleiłem” jest nieprawdą, jeśli go nie wkleił: W jednej z prób rozmowa
o panelu zapytała o brakujący zrzut, autor nie wiedział, o co chodzi, i zeszło na to 16 minut. Pisz
warunkowo: „jeśli dołączyłem zrzut, jest wzorem; jeśli nie, zapytaj mnie o jeden panel, który mi się
podoba, i wyjaśnij, do czego go potrzebujesz”.

Prompt nie zawiera pól do uzupełnienia w rodzaju „[TAK / NIE]”. Użytkownik wkleja prompt bez czytania, więc
puste pola trafiają do rozmowy wykonującej, a ona i tak zadaje te pytania od nowa (w jednej z prób:
pięć pustych pól i runda czterech pytań mimo zdania „nie zadawaj ich od nowa”). Pytania dzielisz
regułą z kroku 4, a odpowiedzi zebrane przed oddaniem wpisujesz do promptu jako gotowe.
Gdy użytkownik odpowiada inaczej, niż zakłada granica w prompcie (na przykład dokłada zakres), rozmowa
wykonująca ma powiedzieć mu, że to zmienia granicę, zanim ruszy.

Ten układ ustalił autor 25.11.2026 i poprawił 26.11.2026: etykiety ustawia ręcznie, a doradcę i cel
wkleja. Linię, której nie trzeba wysyłać, pomijasz całkiem; nie piszesz „bez doradcy” ani „krok pomiń”.

- **Doradca** to drugi, mocniejszy model, do którego model wykonujący sam sięga przed wyborem podejścia
  i przed ogłoszeniem końca. Gdy linia `/advisor fable` pojawia się pierwszy raz w rozmowie z użytkownikiem,
  dopisz pod blokiem jedno zdanie wyjaśnienia. Wyłączenie (`/advisor off`) przypomina rozmowa wykonująca
  na końcu, bo prompt zawiera wstawkę „Doradca”.
- **ULTRACODE** (dopisek przy etykiecie „Poziom”, użytkownik wpisuje `/effort ultracode on` sam) każe rozmowie rozbijać każde większe zadanie na wielu pomocników
  naraz i sprawdzać ich nawzajem, bez liczenia tokenów. Wskazujesz to tylko dla pracy, która dzieli się
  na wiele niezależnych części i w której pominięcie czegokolwiek kosztuje więcej niż tokeny (szeroki
  audyt, migracja, przegląd dużej zmiany). Przy zwykłej pracy, przy rozmowie z użytkownikiem o kierunku i przy
  zadaniu ocenianym okiem dopisku nie ma.
- **Cel (`/goal`)** stoi tylko przy trybie AUTO i tylko wtedy, gdy prompt nie ma „Pytań na start”. Gdy
  zadanie potrzebuje planu albo pytań, ostatnią linią jest zwykły prompt w trybie PLAN, a gotową linię
  `/goal …` rozmowa poda użytkownikowi po zatwierdzeniu drogi, w tej samej postaci jednego wiersza.

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
  Nazwa katalogu z myślnikami to pełna ścieżka, w której każdy znak inny niż litera łacińska albo cyfra
  zamieniono na myślnik. Gdy wszędzie wychodzi 0 (repozytorium zmieniło miejsce, inny komputer), nie
  zgadujesz: pytasz o katalog przed oddaniem (krok 4), z zaleceniem katalogu, w którym leży `CLAUDE.md`
  projektu. 26.11.2026 zewnętrzny tester zgłosił, że po przeniesieniu repozytorium liczenie dało 0 wszędzie.
- Trybu, modelu, poziomu myślenia ani doradcy Claude nie ustawi sam, dlatego są etykietami albo osobnymi
  liniami do wysłania, a nie zdaniami w prompcie. Polecenia `/model`, `/effort` (w tym `ultracode on`) i `/advisor`
  istnieją (sprawdzone 25.11.2026). Gdy jest linia `/advisor fable`, prompt zawiera wstawkę „Doradca”,
  która mówi modelowi, kiedy ma do niego sięgać.
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
   faktycznie zostało uruchomione. Zużycie każdej rozmowy liczy
   `dziennik.py zuzycie --rozmowa <plik.jsonl>`, a nie meldunek pomocnika. Stan zleceń bez wyniku sprawdzasz
   też w późniejszych rozmowach tego projektu, zanim zapytasz użytkownika (25.11.2026 autor odpowiedział na to pytanie
   „sprawdź sobie status”, a odpowiedź stała w rozmowie o godzinę późniejszej).
3. Każdą poprawkę użytkownika przypisz do przyczyny w poleceniu: brakujący fakt, zła wstawka, zły układ, zły
   katalog. Zmień plik umiejętności, który tę przyczynę usuwa, i dopisz datę oraz zdarzenie jednym zdaniem.
4. Sprawdź w zapisach rozmów, czy po wpisanym `/goal ` i wklejonym warunku program wypisał „Goal set”.
   Gdy dwa razy z rzędu nie wypisał, zgłoś to użytkownikowi i oddawaj zwykły prompt bez celu.
5. Progi przejścia szczebel wyżej i drabinę w `references/modele.md` zmieniaj dopiero przy dziesięciu
   zamkniętych wierszach; wcześniej to za mało danych. Zmieniasz wtedy tylko kolumnę „Model dziś” w „Drabinie
   ról”, z datą i numerami wierszy. Nowy model wprowadzasz regułą przyjęcia z tego samego pliku: kandydat
   w rolach poprzednika, decyzja po trzech zamkniętych wierszach (użytkownik, 26.11.2026).

Kalibrację rób w nowej rozmowie, nie w tej, która układała polecenia.

## Czego nie robisz

- Nie wskazujesz trybu koordynatora (`CLAUDE_CODE_COORDINATOR_MODE`). Badanie autora z 26.11.2026 (program,
  dokumentacja, lista zmian) pokazało, że tryb nie ma dokumentacji ani polecenia, a w rozmowie prowadzonej
  na komputerze użytkownika wyłącza się sam: działa tylko w uruchomieniu bez rozmowy (`claude -p`, Agent SDK)
  albo w sesji zdalnej. Pracę wielu pomocników dajesz przez wstawkę „Podzadania” albo ULTRACODE.
- Nie układasz polecenia dla prostego sprawdzenia ani dla drobnej reszty. Odpowiedź jest tańsza niż zlecenie.
- Nie układasz polecenia, gdy przyczyną zastoju jest granica zewnętrzna.
- Nie wskazujesz Opusa 5.5 na poziomie max, a xhigh tylko do długiego programowania według specyfikacji
  z testami. Powód stoi w `references/modele.md`.
- Nie wpisujesz do polecenia umiejętności „na wszelki wypadek”. Każda nazwa ma krok, którym rządzi.
- Nie zostawiasz warunku końca w rodzaju „SEO działa”. Koniec ma sprawdzenie, które widać w rozmowie.
- Nie uruchamiasz dużej pracy sam w tej rozmowie. Długa rozmowa czyta całą swoją historię przy każdym
  kroku, więc nowa rozmowa z gotowym poleceniem kosztuje kilka razy mniej.
