"""Dziennik wyników zleceń: jedyna miara, czy dobór modelu i polecenia działa.

Użycie (zawsze z `python3 -X utf8`):
  dziennik.py start --projekt P --zadanie Z --rodzaj R --model M --poziom L
                    [--doradca brak] [--tryb auto] [--forma polecenie]
      Dopisuje wiersz ze stanem „w_toku” i wypisuje jego numer.
  dziennik.py koniec --id N --wynik osiagniety|nieosiagniety|przerwany --dowod "..."
                     [--tury 0] [--tokeny 0] [--poprawki 0] [--przejscie ""]
      Zamyka wiersz o numerze N.
  dziennik.py wiszace
      Wypisuje zlecenia, które ruszyły i nie zapisały wyniku.
  dziennik.py podsumowanie
      Dla każdego układu: ile zleceń, ile osiągniętych, średnie tokeny i poprawki.

Plik: ~/.claude/zlecenia-wyniki.csv (średniki, UTF-8 z BOM, żeby otwierał się
w Excelu). Zapis idzie przez moduł csv, więc średnik albo cudzysłów w treści pola nie psuje wiersza.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import os
import sys
from pathlib import Path

POLA = ["id", "data", "projekt", "zadanie", "rodzaj", "model", "poziom", "doradca", "tryb", "forma",
        "wynik", "dowod", "tury", "tokeny", "poprawki_uzytkownika", "przejscie_wyzej", "data_konca"]
WYNIKI = ("osiagniety", "nieosiagniety", "przerwany")


def sciezka() -> Path:
    return Path(os.environ.get("ZLECENIA_DZIENNIK") or Path.home() / ".claude" / "zlecenia-wyniki.csv")


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
    wiersze = wczytaj()
    numer = max((int(w["id"]) for w in wiersze if w["id"].isdigit()), default=0) + 1
    wiersze.append({**{p: "" for p in POLA}, "id": str(numer), "data": dt.date.today().isoformat(),
                    "projekt": a.projekt, "zadanie": a.zadanie, "rodzaj": a.rodzaj, "model": a.model,
                    "poziom": a.poziom, "doradca": a.doradca, "tryb": a.tryb, "forma": a.forma,
                    "wynik": "w_toku"})
    zapisz(wiersze)
    print(numer)
    return 0


def koniec(a: argparse.Namespace) -> int:
    wiersze = wczytaj()
    for w in wiersze:
        if w["id"] == str(a.id):
            w.update(wynik=a.wynik, dowod=a.dowod, tury=str(a.tury), tokeny=str(a.tokeny),
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
    s.set_defaults(f=start)
    k = sub.add_parser("koniec")
    k.add_argument("--id", type=int, required=True)
    k.add_argument("--wynik", choices=WYNIKI, required=True)
    k.add_argument("--dowod", required=True)
    k.add_argument("--tury", type=int, default=0)
    k.add_argument("--tokeny", type=int, default=0)
    k.add_argument("--poprawki", type=int, default=0)
    k.add_argument("--przejscie", default="")
    k.set_defaults(f=koniec)
    sub.add_parser("wiszace").set_defaults(f=wiszace)
    sub.add_parser("podsumowanie").set_defaults(f=podsumowanie)
    a = p.parse_args()
    return a.f(a)


if __name__ == "__main__":
    sys.exit(main())
