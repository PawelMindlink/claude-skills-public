# Szkielet polecenia i wstawki

Polecenie składasz ze szkieletu i tylko tych wstawek, które pasują do rodzaju zadania. Pustej sekcji nie
zostawiasz. Tekst w nawiasach ostrych zastępujesz faktami; fakty, które znasz, wpisujesz wprost, zamiast
kazać je czytać od nowa.

## Szkielet

~~~
# Zlecenie: <krótka nazwa>

## Cel
<Jedno lub dwa zdania: co ma być prawdą na końcu i po co to użytkownikowi.>

## Gotowe, gdy
<Ponumerowane dowody, które pokażesz w rozmowie. Każdy da się sprawdzić poleceniem, liczbą albo
obejrzeniem. Zatwierdzenie przez użytkownika jest dobrym dowodem.>

## Co już wiadomo
<Fakty z plików i z rozmowy, z pełnymi ścieżkami. Liczby z jednostką i źródłem.>

## Jak pracować
<Wstawki: Pierwszy etap, Pytania w trakcie, Podzadania, Zadanie oceniane okiem.>

## Zgody
<Wstawka Zgody.>

## Dokończenie pracy
<Wstawka Dokończenie pracy.>

## Wynik
<Zostaw puste. Wypełnia je rozmowa wykonująca: co powstało, czym sprawdzone, co nie wyszło i dlaczego.>
~~~

## Wstawki

### Pierwszy etap

Dla każdego zadania większego niż wykonanie według opisu. Użytkownik bywa niepewny, jaka droga jest najlepsza,
więc drogę proponuje model, a użytkownik ją zatwierdza.

~~~
Zanim cokolwiek zmienisz:
1. Napisz jednym zdaniem, co zamierzasz zrobić.
2. Zbierz fakty: przeczytaj <pliki i źródła> oraz rozejrzyj się szerzej, także w źródłach, których to
   zlecenie nie wymienia, jeśli mogą dotyczyć sprawy.
3. Zadaj mi „Pytania na start” z tego zlecenia i dopytaj o wszystko, czego jeszcze brakuje, a czego nie da
   się ustalić z plików. Do każdego pytania dodaj własne zalecenie.
4. Pokaż drogę do wyniku: docelowy kształt, potem kroki z tym, czym każdy się sprawdza. Zapisz ją w pliku
   <pełna ścieżka pliku postępu> i odhaczaj w nim kroki, żeby drogi nie zgubić po skróceniu rozmowy.
5. Pracuj dopiero, gdy odpowiem na pytania, od których zależy pierwszy krok.
~~~

### Pytania w trakcie

Zawsze. Użytkownik wybrał 25.11.2026, że zadanie pyta go także w trakcie pracy.

~~~
Gdy w trakcie trafisz na niejasność albo decyzję, która należy do mnie, zadaj pytanie od razu, z własnym
zaleceniem i z tym, co zmienia każda odpowiedź. Tego promptu nie pisałem sam i nie znam go na pamięć,
więc każde pytanie ma być zrozumiałe bez niego: napisz, czego potrzebujesz i po co, zamiast odsyłać do
zdania z promptu. Gdy na pytanie odpowiem „nie wiem” albo „nie pamiętam”, powiedz, co przyjmujesz w to
miejsce, zanim pójdziesz dalej. Nie zgaduj i nie odkładaj pytań na koniec. Czekając na
odpowiedź, rób to, co od niej nie zależy. Gdy nic takiego nie zostało, napisz „Czekam na odpowiedź użytkownika”
i wymień otwarte pytania.
~~~

### Po nieudanych podejściach

Gdy krok „Historia” znalazł wcześniejsze podejścia.

~~~
To zadanie było podejmowane <N> razy:
- <data>: <co zrobiono> — stanęło, bo <przyczyna z pliku> (<pełna ścieżka źródła>).
- ...
Nie powtarzaj: <konkretne podejścia>.
Zacznij od diagnozy: nazwij jedną przyczynę, która łączy te podejścia, i pokaż mi ją, zanim zaproponujesz
drogę. Jeżeli nowa droga różni się od poprzednich tylko wykonaniem, a nie przyczyną, powiedz to wprost.
~~~

### Zadanie oceniane okiem

Dla strony, panelu, prezentacji, reklamy. Bez wzoru model wybiera własne domyślne rozwiązania i wynik
wygląda jak każdy inny.

~~~
Wzorem jest <pełna ścieżka albo adres>; podoba mi się w nim <co konkretnie>. Jeżeli wzoru nie podałem,
zapytaj o niego albo pokaż trzy różne kierunki na jednym ekranie i poczekaj na wybór, zanim zbudujesz
resztę.
Nie używaj: <nazwane rozwiązania, których użytkownik nie chce, np. kremowe tło, etykiety pisane czcionką
o stałej szerokości, przyciski-pigułki, ściana tekstu zamiast rysunku>.
Zacznij od widoku na telefonie (390 px), potem komputer.
Przed oddaniem obejrzyj wynik sam, na zrzucie ekranu, i popraw to, co widzisz. Oddajesz dopiero wersję,
którą obejrzałeś.
~~~

Ogólne „ma wyglądać dobrze” nie działa: modele reagują na nazwane wzorce do uniknięcia i na pokazany wzór.

### Podzadania

~~~
Tę rozmowę prowadzi jeden koordynator: planuje, zleca i sprawdza. Nie uruchamiaj tego zlecenia w drugiej
rozmowie.
- Części niezależne od siebie zleć równolegle (umiejętność superpowers:dispatching-parallel-agents).
- Plan z kolejnymi krokami wykonuj krok po kroku z pomocnikami (superpowers:subagent-driven-development).
- Model podawaj przy każdym pomocniku: sonnet do czytania i do wykonania według opisu, opus do budowy
  i poprawek w kodzie, haiku do obejrzenia jednego obrazu. Żaden pomocnik nie pracuje na Fable.
- Jedno zlecenie to jedno zadanie. Wpisz do niego fakty, które już znasz, pełne ścieżki i polecenie, którym
  pomocnik sam sprawdzi wynik. Jeden pomocnik pisze do jednej grupy plików.
- Małą resztę pracy (do trzech kroków w jednym lub dwóch plikach) zrób sam, bo zlecanie kosztuje wtedy
  więcej niż wykonanie.
- Sprawdź na dysku to, co pomocnik zameldował, zanim uznasz krok za zrobiony.
~~~

### Zgody

Wymieniasz konkretne działania. Ogólny zakaz blokuje też rutynę, a słowo „nigdy” Fable traktuje
bezwzględnie.

~~~
Bez pytania wolno: <np. czytać pliki i konta, pisać szkice, uruchamiać testy, zapisywać w katalogu X>.
Na moją zgodę czeka: <np. publikacja na żywo, wysyłka wiadomości, zmiana budżetu, usunięcie plików>.
Zgoda na jedną rzecz z tej listy <dotyczy / nie dotyczy> następnych tego samego rodzaju.
~~~

Ostatnie zdanie rozstrzygaj z użytkownikiem przed uruchomieniem: w jednym z projektów nowe strony stały dwa miesiące,
bo kilkanaście szkiców czekało na pojedyncze zgody.

### Dokończenie pracy

Dla pracy dłuższej niż kilka tur, zawsze przy Fable na poziomie medium i przy Sonnecie.

~~~
Pracuj, dopóki wszystko z „Gotowe, gdy” nie jest zrobione i pokazane. Nie kończ tury zapowiedzią
następnego kroku, ofertą „mogę kontynuować” ani listą tego, co zostało. Zwykłe przeszkody (błąd, przekroczony
czas, pusty wynik, zablokowany plik) najpierw zdiagnozuj i obejdź inną drogą.
Zatrzymaj się, gdy: czekasz na moją odpowiedź i nie masz nic niezależnego do zrobienia; następny krok jest
na liście zgód; trafiłeś na przeszkodę postawioną celowo. Napisz wtedy wprost, co zastałeś.
Co kilka kroków napisz jedno zdanie, gdzie jesteś. Na końcu wypełnij sekcję „Wynik” w pliku zlecenia: co
powstało, czym to sprawdziłeś, czego nie zrobiłeś.
~~~

### Zapis wyniku

Zawsze, jako ostatni akapit polecenia. Zanim oddasz polecenie, sam zakładasz wiersz zlecenia i wpisujesz
jego numer do polecenia:

`python3 -X utf8 ~/.claude/skills/zlecenie/scripts/dziennik.py start --projekt "<projekt>" --zadanie "<zadanie>" --rodzaj "<rodzaj>" --model <model> --poziom <poziom> --doradca <brak albo fable> --tryb <auto albo planowania> --forma <polecenie albo goal>`

~~~
Na końcu pracy, także gdy ją przerywasz, zapisz wynik tego zlecenia poleceniem:
python3 -X utf8 ~/.claude/skills/zlecenie/scripts/dziennik.py koniec --id <numer> --wynik <osiagniety albo nieosiagniety albo przerwany> --dowod "<polecenie albo liczba, która to pokazuje>" --tury <liczba tur> --tokeny <odczyt z /usage> --poprawki <ile razy poprawiałem kierunek albo odrzuciłem wynik> --przejscie "<puste albo powód mocniejszego układu>"
Wynik oceniasz według sprawdzeń z „Gotowe, gdy”, a nie według własnej opinii.
Gdy to samo sprawdzenie nie przechodzi po dwóch próbach naprawy, gdy dwa razy odrzucę wynik z tego samego
powodu albo gdy minie granica tur, a spełniona jest mniej niż połowa punktów „Gotowe, gdy”, zatrzymaj się
i napisz mi jedno polecenie do wpisania (<następny szczebel, np. /effort high>) razem z powodem. Sam modelu
ani poziomu nie zmienisz.
~~~

Następny szczebel wpisujesz konkretnie, według listy szczebli w `modele.md`. Gdy zlecenie jest już na
najwyższym szczeblu, zamiast polecenia stoi „zatrzymaj się i napisz, czego Ci brakuje”.

### Zakończenie rozmowy 1 w układzie dwóch rozmów

~~~
Ta rozmowa kończy się planem, a nie wykonaniem. Gdy zatwierdzę drogę, zapisz plan w <pełna ścieżka pliku
zlecenia> i pokaż mi polecenie dla rozmowy wykonującej razem z krokami uruchomienia: Opus 5.5 medium,
tryb auto, pomocnicy na Sonnecie, wiersz „Doradca: fable, po pracy wyłącz” i wstawka „Doradca”
w treści promptu. Napisz, czy wykonanie ma iść przez /goal, i jeśli tak, podaj warunek krótszy niż
1500 znaków.
~~~

### Doradca

Tylko gdy nagłówek bloku ma wiersz „Doradca”. Sam wiersz włącza doradcę; to zdanie mówi modelowi, kiedy
ma do niego sięgać, żeby nie pytał co krok (każde sięgnięcie czyta całą rozmowę od nowa po cenie Fable).

~~~
W tej rozmowie jest włączony doradca. Poradź się go w trzech momentach: zanim wybierzesz podejście, gdy
ten sam błąd wraca drugi raz i zanim ogłosisz koniec. W zwykłych krokach go nie pytaj. Gdy skończysz,
przypomnij mi, żebym wpisał /advisor off, bo ustawienie zostaje na stałe i obejmuje pomocników.
~~~
