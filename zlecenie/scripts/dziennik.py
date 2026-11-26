"""Dziennik wyników zleceń: jedyna miara, czy dobór modelu i polecenia działa.

Użycie (zawsze z `python3 -X utf8`):
  dziennik.py start --projekt P --zadanie Z --rodzaj R --model M --poziom L
                    [--doradca brak] [--tryb auto] [--forma polecenie] [--plik ZLECENIE-*.md]
      Dopisuje wiersz ze stanem „w_toku” i wypisuje jego numer.
      --rodzaj to jeden z RODZAJE: „wykonanie wedlug opisu”, „budowa z podzadaniami”, „niejasna droga”,
      „po nieudanych podejsciach”, opcjonalnie z dopiskiem „ + oceniane okiem”. Inna wartość kończy się
      błędem bez wiersza, bo 26.11.2026 wolny tekst dał 16 wartości na 20 wierszy i `podsumowanie`
      nie porównywało układów.
      --plik wskazuje plik zlecenia; gdy go nie ma, błąd bez wiersza. Gdy ma ponad 4000 znaków przy
      „wykonanie wedlug opisu” albo ponad 7000 przy pozostałych, ostrzega na stderr, a wiersz i tak powstaje;
      próg z SKILL.md krok 6 (26.11.2026, zewnętrzny tester: pliki po ok. 9 KB niezależnie od zadania).
  dziennik.py koniec --id N --wynik osiagniety|nieosiagniety|przerwany --dowod "..."
                     [--tury 0] [--tokeny N] [--rozmowa plik.jsonl] [--poprawki 0] [--przejscie ""]
      Zamyka wiersz o numerze N. Bez --tokeny liczy zużycie sam z zapisu rozmowy (jak `zuzycie`).
      Gdy zapisu rozmowy nie znajdzie, zostawia tokeny puste i mówi to na stderr, zamiast wpisać 0
      (26.11.2026, uwaga 6 zewnętrznego testera: zera zaniżały średnią w `podsumowanie`).
  dziennik.py zuzycie [--rozmowa plik.jsonl]
      Tokeny rozmowy i jej pomocników z zapisu Claude Code, razem z odczytem pamięci podręcznej.
      Bez --rozmowa bierze zapis bieżącej rozmowy po zmiennej CLAUDE_CODE_SESSION_ID, którą Claude Code
      ustawia w każdym poleceniu. Do 26.11.2026 brał najnowszy zapis ze wszystkich projektów i przy
      równoległych rozmowach liczył cudzą (wiersze 12 i 15 dziennika: po 20,71 mln z tej samej rozmowy).
      Dodane 25.11.2026: model nie czyta /usage, więc zlecenia wpisywały 0 albo sumę z meldunków
      pomocników (SEO: 1,8 mln wpisane, 92 mln w zapisie).
  dziennik.py wiszace
      Wypisuje zlecenia, które ruszyły i nie zapisały wyniku.
  dziennik.py podsumowanie
      Dla każdego układu: ile zleceń, ile osiągniętych, średnie tokeny i poprawki.

Plik: ~/.claude/zlecenia-wyniki.csv (średniki, UTF-8 z BOM, żeby otwierał się
w Excelu). Zapis idzie przez moduł csv, więc średnik albo cudzysłów w treści pola nie psuje wiersza.
Odczyt i zapis idą pod blokadą pliku `<dziennik>.lock` (26.11.2026, uwaga 7 zewnętrznego testera: trzy
równoległe przebiegi pisały do jednego pliku). Blokada starsza niż minuta jest uznawana za porzuconą.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import os
import sys
import time
from contextlib import contextmanager
from pathlib import Path

POLA = ["id", "data", "projekt", "zadanie", "rodzaj", "model", "poziom", "doradca", "tryb", "forma",
        "wynik", "dowod", "tury", "tokeny", "poprawki_uzytkownika", "przejscie_wyzej", "data_konca"]
WYNIKI = ("osiagniety", "nieosiagniety", "przerwany")
RODZAJE = ("wykonanie wedlug opisu", "budowa z podzadaniami", "niejasna droga", "po nieudanych podejsciach")
DOPISEK = " + oceniane okiem"
PROG_WYKONANIA, PROG_POZOSTALYCH = 4000, 7000


def rodzaj_dozwolony(rodzaj: str) -> bool:
    """Tylko rodzaj z RODZAJE, z dopiskiem DOPISEK albo bez: 26.11.2026 wolny tekst dał 16 wartości na
    20 wierszy, więc `podsumowanie` nie porównywało układów."""
    glowny = rodzaj[: -len(DOPISEK)] if rodzaj.endswith(DOPISEK) else rodzaj
    return glowny in RODZAJE


def sprawdz_plik(plik: str, rodzaj: str) -> bool:
    """Fałsz, gdy pliku zlecenia nie ma; ostrzeżenie o długości według progu z SKILL.md krok 6
    (26.11.2026, zewnętrzny tester: pliki po ok. 9 KB niezależnie od zadania)."""
    sciezka_pliku = Path(plik)
    if not sciezka_pliku.is_file():
        print(f"Nie ma pliku zlecenia {sciezka_pliku}; wiersz nie powstał.", file=sys.stderr)
        return False
    znakow = len(sciezka_pliku.read_text(encoding="utf-8"))
    prog = PROG_WYKONANIA if rodzaj.startswith(RODZAJE[0]) else PROG_POZOSTALYCH
    if znakow > prog:
        print(f"Uwaga: plik zlecenia ma {znakow} znaków, próg dla tego rodzaju to {prog}. "
              "Skróć »Co już wiadomo«: fakt do przeczytania jednym odczytem zastąp ścieżką.", file=sys.stderr)
    return True


def sciezka() -> Path:
    return Path(os.environ.get("ZLECENIA_DZIENNIK") or Path.home() / ".claude" / "zlecenia-wyniki.csv")


@contextmanager
def blokada():
    """Wyłączny dostęp do dziennika; czeka do ZLECENIA_BLOKADA_CZAS sekund (domyślnie 30)."""
    zamek = Path(str(sciezka()) + ".lock")
    zamek.parent.mkdir(parents=True, exist_ok=True)
    termin = time.monotonic() + float(os.environ.get("ZLECENIA_BLOKADA_CZAS") or 30)
    while True:
        try:
            uchwyt = os.open(zamek, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            break
        except FileExistsError:
            try:
                if time.time() - zamek.stat().st_mtime > 60:
                    zamek.unlink()
                    continue
            except FileNotFoundError:
                continue
            if time.monotonic() > termin:
                raise TimeoutError(f"Dziennik {sciezka()} jest zablokowany przez inny przebieg ({zamek}).")
            time.sleep(0.05)
    try:
        os.write(uchwyt, str(os.getpid()).encode())
        os.close(uchwyt)
        yield
    finally:
        zamek.unlink(missing_ok=True)


def wczytaj() -> list[dict]:
    plik = sciezka()
    if not plik.exists():
        return []
    with plik.open(encoding="utf-8-sig", newline="") as f:
        return [{p: w.get(p, "") or "" for p in POLA} for w in csv.DictReader(f, delimiter=";")]


def zapisz(wiersze: list[dict]) -> None:
    plik = sciezka()
    plik.parent.mkdir(parents=True, exist_ok=True)
    tymczasowy = plik.with_suffix(".tmp")
    with tymczasowy.open("w", encoding="utf-8-sig", newline="") as f:
        pisarz = csv.DictWriter(f, fieldnames=POLA, delimiter=";", quoting=csv.QUOTE_MINIMAL)
        pisarz.writeheader()
        pisarz.writerows(wiersze)
    tymczasowy.replace(plik)


def start(a: argparse.Namespace) -> int:
    if not rodzaj_dozwolony(a.rodzaj):
        print(f"Rodzaj „{a.rodzaj}” spoza listy; wiersz nie powstał. Dozwolone: "
              + ", ".join(f"„{r}”" for r in RODZAJE) + f", każdy także z dopiskiem „{DOPISEK}”.",
              file=sys.stderr)
        return 1
    if a.plik and not sprawdz_plik(a.plik, a.rodzaj):
        return 1
    with blokada():
        wiersze = wczytaj()
        numer = max((int(w["id"]) for w in wiersze if w["id"].isdigit()), default=0) + 1
        wiersze.append({**{p: "" for p in POLA}, "id": str(numer), "data": dt.date.today().isoformat(),
                        "projekt": a.projekt, "zadanie": a.zadanie, "rodzaj": a.rodzaj, "model": a.model,
                        "poziom": a.poziom, "doradca": a.doradca, "tryb": a.tryb, "forma": a.forma,
                        "wynik": "w_toku"})
        zapisz(wiersze)
    print(numer)
    return 0


def tokeny_pliku(plik: Path) -> int:
    """Suma wejścia, odczytu i zapisu pamięci podręcznej oraz wyjścia; jedna odpowiedź liczona raz."""
    widziane, razem = set(), 0
    with plik.open(encoding="utf-8", errors="replace") as f:
        for linia in f:
            try:
                d = json.loads(linia)
            except ValueError:
                continue
            m = d.get("message") if d.get("type") == "assistant" else None
            u = m.get("usage") if isinstance(m, dict) else None
            klucz = d.get("requestId") or (m or {}).get("id")
            if not u or klucz in widziane:
                continue
            widziane.add(klucz)
            razem += sum(u.get(k) or 0 for k in ("input_tokens", "cache_read_input_tokens",
                                                 "cache_creation_input_tokens", "output_tokens"))
    return razem


def rozmowa_sesji() -> Path | None:
    """Zapis bieżącej rozmowy: plik o nazwie z CLAUDE_CODE_SESSION_ID w katalogu projektów."""
    sesja = os.environ.get("CLAUDE_CODE_SESSION_ID")
    if not sesja:
        return None
    katalog = Path(os.environ.get("ZLECENIA_PROJEKTY") or Path.home() / ".claude" / "projects")
    pliki = list(katalog.glob(f"*/{sesja}.jsonl"))
    return max(pliki, key=lambda p: p.stat().st_mtime) if pliki else None


def policz(rozmowa: str | None) -> tuple[int, int, Path | None]:
    plik = Path(rozmowa) if rozmowa else rozmowa_sesji()
    if not plik or not plik.exists():
        return 0, 0, None
    pomocnicy = sum(tokeny_pliku(p) for p in plik.with_suffix("").glob("subagents/agent-*.jsonl"))
    return tokeny_pliku(plik), pomocnicy, plik


def zuzycie(a: argparse.Namespace) -> int:
    glowna, pomocnicy, plik = policz(a.rozmowa)
    if not plik:
        print("Nie znalazłem zapisu rozmowy.", file=sys.stderr)
        return 1
    print(glowna + pomocnicy)
    print(f"rozmowa {glowna}, pomocnicy {pomocnicy}, plik {plik}")
    return 0


def koniec(a: argparse.Namespace) -> int:
    tokeny = "" if a.tokeny is None else str(a.tokeny)
    if a.tokeny is None:
        glowna, pomocnicy, plik = policz(a.rozmowa)
        if plik:
            tokeny = str(glowna + pomocnicy)
        else:
            print("Uwaga: nie policzyłem tokenów, bo nie znalazłem zapisu tej rozmowy; pole zostaje puste. "
                  "Podaj --rozmowa <plik.jsonl>, jeśli go znasz.", file=sys.stderr)
    with blokada():
        wiersze = wczytaj()
        for w in wiersze:
            if w["id"] == str(a.id):
                w.update(wynik=a.wynik, dowod=a.dowod, tury=str(a.tury), tokeny=tokeny,
                         poprawki_uzytkownika=str(a.poprawki), przejscie_wyzej=a.przejscie,
                         data_konca=dt.date.today().isoformat())
                zapisz(wiersze)
                print(f"Zapisano wynik zlecenia {a.id}: {a.wynik}")
                return 0
    print(f"Nie ma zlecenia o numerze {a.id} w {sciezka()}", file=sys.stderr)
    return 1


def wiszace(_: argparse.Namespace) -> int:
    lista = [w for w in wczytaj() if w["wynik"] == "w_toku"]
    if not lista:
        print("Brak zleceń bez zapisanego wyniku.")
    for w in lista:
        print(f"{w['id']}: {w['data']} | {w['projekt']} | {w['zadanie']} | {w['model']} {w['poziom']}")
    return 0


def podsumowanie(_: argparse.Namespace) -> int:
    grupy: dict[tuple, list[dict]] = {}
    for w in wczytaj():
        grupy.setdefault((w["rodzaj"], w["model"], w["poziom"], w["doradca"]), []).append(w)
    if not grupy:
        print("Dziennik jest pusty.")
    for (rodzaj, model, poziom, doradca), ws in sorted(grupy.items()):
        zamkniete = [w for w in ws if w["wynik"] in WYNIKI]
        trafione = [w for w in zamkniete if w["wynik"] == "osiagniety"]

        def srednia(pole: str, zbior: list[dict]) -> str:
            liczby = [int(w[pole]) for w in zbior if w[pole].isdigit()]
            return f"{sum(liczby) / len(liczby):.0f}" if liczby else "brak"

        print(f"{rodzaj} | {model} {poziom} | doradca: {doradca} | zleceń {len(ws)}, zamkniętych "
              f"{len(zamkniete)}, osiągniętych {len(trafione)}, w toku {len(ws) - len(zamkniete)} | "
              f"średnio tokenów na osiągnięty {srednia('tokeny', trafione)}, "
              f"poprawek użytkownika {srednia('poprawki_uzytkownika', zamkniete)}")
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="polecenie", required=True)
    s = sub.add_parser("start")
    for nazwa in ("projekt", "zadanie", "rodzaj", "model", "poziom"):
        s.add_argument(f"--{nazwa}", required=True)
    s.add_argument("--doradca", default="brak")
    s.add_argument("--tryb", default="auto")
    s.add_argument("--forma", default="polecenie")
    s.add_argument("--plik", default=None)
    s.set_defaults(f=start)
    k = sub.add_parser("koniec")
    k.add_argument("--id", type=int, required=True)
    k.add_argument("--wynik", choices=WYNIKI, required=True)
    k.add_argument("--dowod", required=True)
    k.add_argument("--tury", type=int, default=0)
    k.add_argument("--tokeny", type=int, default=None)
    k.add_argument("--rozmowa", default=None)
    k.add_argument("--poprawki", type=int, default=0)
    k.add_argument("--przejscie", default="")
    k.set_defaults(f=koniec)
    z = sub.add_parser("zuzycie")
    z.add_argument("--rozmowa", default=None)
    z.set_defaults(f=zuzycie)
    sub.add_parser("wiszace").set_defaults(f=wiszace)
    sub.add_parser("podsumowanie").set_defaults(f=podsumowanie)
    a = p.parse_args()
    try:
        return a.f(a)
    except TimeoutError as blad:
        print(blad, file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
