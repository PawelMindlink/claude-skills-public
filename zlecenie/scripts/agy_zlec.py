"""Jedno sprawdzone zlecenie dla modelu Gemini: najpierw przez `agy -p`, klucz Gemini API jako zapas.

Użycie (zawsze z `python3 -X utf8`):
  agy_zlec.py --model gemini-4-neon-high --polecenie plik.md --wynik wynik.json
              [--czas 900] [--zapas api|brak] [--droga agy|api]

Dlaczego tak (26.11.2026, zlecenie 21, odczyt dokumentacji Antigravity i próby w tej rozmowie):
- `agy` wczytuje do każdego wywołania plik zasad `~/.gemini/GEMINI.md`, opisy umiejętności (u użytkownika cały
  `~/.claude/skills`, z nazwami klientów), umiejętności wtyczek i usługi MCP. Dokumentacja nie ma przełącznika,
  który to wyłącza na jedno uruchomienie. Program podaje więc pusty katalog domowy (USERPROFILE, HOME):
  „OK” kosztowało 11 817 tokenów wejścia zamiast 31 521 i 6 s zamiast 50 s; logowanie dalej działa.
- Katalog roboczy jest pusty i poza repozytorium git, więc nie dochodzą zasady projektu.
- Bez `--mode plan`: ten tryb dokleja `/plan` i 3735 znaków instrukcji „think and plan carefully”, a w próbie
  26.11 Hydrogen zamiast pliku z kodem próbował zapisać `implementation_plan.md` (2 z 3 zadań niezaliczone).
  Bezpieczeństwo dają zakazy w `--settings` (według dokumentacji obowiązują w każdym trybie; zakaz zapisu
  sprawdzony 26.11 komunikatem „Matches user-configured deny rule”) i `--sandbox`. Zgoda użytkownika 26.11.
- `useG1Credits: false` w każdym wywołaniu, bo wpis w pliku ustawień potrafi zniknąć (26.11: plik `{}`).
- Wejście zamknięte (`stdin=DEVNULL`) i `--print-timeout`, bo agy potrafił wisieć na Windows.
- Polecenie idzie argumentem wiersza poleceń; Windows przyjmuje najwyżej 32 767 znaków, więc granica 28 000.

Kody wyjścia: 0 sukces, 3 błąd modelu, 4 wyczerpany limit, 5 przekroczony czas, 2 zły argument.
Przy kodach 3, 4 i 5 z `--zapas api` program powtarza zlecenie przez Gemini API (klucz `GEMINI_API_KEY`)
i oddaje jego kod. Ścieżkę do `agy` można podmienić zmienną `AGY_BIN` (testy).
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

AGY_DOMYSLNY = shutil.which("agy") or str(Path.home() / ".gemini" / "bin" / ("agy.exe" if os.name == "nt" else "agy"))
BAZA = Path(os.environ.get("LOCALAPPDATA", str(Path.home()))) / "agy-zlecenie"
GRANICA_ZNAKOW = 28_000
API_ADRES = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
USTAWIENIA = {
    "useG1Credits": False,
    "permissions": {"deny": ["write_file(*)", "command(*)", "execute_url(*)", "read_url(*)", "mcp(*)"]},
}
WZOR_LIMITU = re.compile(r"quota|rate.?limit|resource.?exhausted|weekly limit|limit.*reached|429", re.I)
WZOR_CZASU = re.compile(r"print timeout|print_timeout", re.I)

OK, BLAD, LIMIT, CZAS, ZLY_ARGUMENT = 0, 3, 4, 5, 2


def rozbij_model(model: str) -> tuple[str, str | None]:
    """`gemini-4-neon-high` -> (`gemini-4-neon`, `high`); nazwa bez poziomu -> (nazwa, None)."""
    m = re.fullmatch(r"(.+?)-(low|medium|high|xhigh)", model)
    return (m.group(1), m.group(2)) if m else (model, None)


def katalogi() -> tuple[Path, Path]:
    dom, praca = BAZA / "dom", BAZA / "praca"
    dom.mkdir(parents=True, exist_ok=True)
    praca.mkdir(parents=True, exist_ok=True)
    return dom, praca


def przez_agy(model: str, polecenie: str, czas: int) -> dict:
    dom, praca = katalogi()
    agy = os.environ.get("AGY_BIN", AGY_DOMYSLNY)
    # AGY_BIN jako lista JSON (testy): pliki .cmd gubią polskie litery w ścieżce.
    poczatek = json.loads(agy) if agy.startswith("[") else [agy]
    srodowisko = dict(os.environ, USERPROFILE=str(dom), HOME=str(dom))
    komenda = [*poczatek, "-p", polecenie, "--model", model, "--sandbox",
               "--print-timeout", f"{czas}s", "--output-format", "json",
               "--settings", json.dumps(USTAWIENIA)]
    start = time.time()
    try:
        wynik = subprocess.run(komenda, cwd=praca, env=srodowisko, stdin=subprocess.DEVNULL,
                               capture_output=True, text=True, encoding="utf-8", errors="replace",
                               timeout=czas + 60)
    except subprocess.TimeoutExpired:
        return {"droga": "agy", "model": model, "kod": CZAS, "status": "TIMEOUT",
                "czas_s": round(time.time() - start, 1), "stderr": "proces przerwany po czasie"}
    czas_s = round(time.time() - start, 1)
    try:
        dane = json.loads(wynik.stdout) if wynik.stdout.strip() else {}
    except json.JSONDecodeError:
        dane = {"response": wynik.stdout}
    status = dane.get("status", "BRAK")
    tekst_bledu = f"{wynik.stderr}\n{dane.get('error', '')}"
    if wynik.returncode == 0 and status == "SUCCESS" and dane.get("response", "").strip():
        kod = OK
    elif WZOR_CZASU.search(tekst_bledu) or dane.get("finished_reason") == "print_timeout":
        kod = CZAS
    elif WZOR_LIMITU.search(tekst_bledu):
        kod = LIMIT
    else:
        kod = BLAD
    return {"droga": "agy", "model": model, "kod": kod, "status": status,
            "odpowiedz": dane.get("response", ""), "uzycie": dane.get("usage", {}),
            "czas_s": czas_s, "kod_agy": wynik.returncode, "stderr": wynik.stderr[-2000:],
            "conversation_id": dane.get("conversation_id")}


def myslenie_z_rozmowy(conversation_id: str | None, odpowiedz: str) -> str:
    """Tok myślenia Gemini z lokalnej bazy rozmowy agy (krok typu 15, odczyt 26.11.2026, agy 1.5.18).

    Baza to SQLite z krokami w formacie protobuf; bez opisu formatu bierzemy najdłuższe ciągi tekstu
    z kroku odpowiedzi, które nie są samą odpowiedzią. Przy zmianie formatu zwraca pusty napis.
    """
    import sqlite3
    if not conversation_id:
        return ""
    baza = BAZA / "dom" / ".gemini" / "antigravity-cli" / "conversations" / f"{conversation_id}.db"
    if not baza.is_file():
        return ""
    try:
        with sqlite3.connect(baza) as c:
            wiersze = c.execute("select step_payload from steps where step_type = 15 order by idx").fetchall()
    except sqlite3.Error:
        return ""
    poczatek_odpowiedzi = odpowiedz.strip()[:60]
    teksty = []
    for (dane,) in wiersze:
        for kawalek in re.findall(rb"(?:[\x20-\x7e\n\t]|[\xc2-\xf4][\x80-\xbf]+){200,}", dane or b""):
            t = kawalek.decode("utf-8", "replace").strip()
            if poczatek_odpowiedzi and poczatek_odpowiedzi in t:
                continue
            teksty.append(t)
    return "\n\n".join(teksty)


def przez_api(model: str, polecenie: str, czas: int) -> dict:
    klucz = os.environ.get("GEMINI_API_KEY")
    nazwa, poziom = rozbij_model(model)
    if not klucz:
        return {"droga": "api", "model": model, "kod": BLAD, "status": "BRAK_KLUCZA",
                "stderr": "brak GEMINI_API_KEY"}
    konfiguracja: dict = {"maxOutputTokens": 65536}
    if poziom:
        konfiguracja["thinkingConfig"] = {"thinkingLevel": poziom}
    cialo = {"contents": [{"role": "user", "parts": [{"text": polecenie}]}],
             "generationConfig": konfiguracja}
    zadanie = urllib.request.Request(API_ADRES.format(model=nazwa), data=json.dumps(cialo).encode(),
                                     headers={"Content-Type": "application/json",
                                              "x-goog-api-key": klucz}, method="POST")
    start = time.time()
    try:
        with urllib.request.urlopen(zadanie, timeout=czas) as odp:
            dane = json.load(odp)
    except urllib.error.HTTPError as e:
        tresc = e.read().decode("utf-8", "replace")[-2000:]
        kod = LIMIT if e.code == 429 else BLAD
        return {"droga": "api", "model": model, "kod": kod, "status": f"HTTP_{e.code}",
                "czas_s": round(time.time() - start, 1), "stderr": tresc}
    except (TimeoutError, urllib.error.URLError) as e:
        return {"droga": "api", "model": model, "kod": CZAS, "status": "TIMEOUT",
                "czas_s": round(time.time() - start, 1), "stderr": str(e)}
    czas_s = round(time.time() - start, 1)
    kandydat = (dane.get("candidates") or [{}])[0]
    czesci = kandydat.get("content", {}).get("parts", [])
    tekst = "".join(c.get("text", "") for c in czesci if not c.get("thought"))
    meta = dane.get("usageMetadata", {})
    uzycie = {"input_tokens": meta.get("promptTokenCount", 0),
              "output_tokens": meta.get("candidatesTokenCount", 0),
              "thinking_tokens": meta.get("thoughtsTokenCount", 0),
              "cache_read_tokens": meta.get("cachedContentTokenCount", 0),
              "total_tokens": meta.get("totalTokenCount", 0)}
    kod = OK if tekst.strip() and kandydat.get("finishReason") in ("STOP", None) else BLAD
    return {"droga": "api", "model": model, "kod": kod, "status": kandydat.get("finishReason", "BRAK"),
            "odpowiedz": tekst, "uzycie": uzycie, "czas_s": czas_s}


def zlec(model: str, polecenie: str, czas: int = 900, droga: str = "agy", zapas: str = "api") -> dict:
    if len(polecenie) > GRANICA_ZNAKOW and droga == "agy":
        return {"droga": "agy", "model": model, "kod": ZLY_ARGUMENT, "status": "ZA_DLUGIE",
                "stderr": f"polecenie ma {len(polecenie)} znaków, granica {GRANICA_ZNAKOW}"}
    wynik = przez_agy(model, polecenie, czas) if droga == "agy" else przez_api(model, polecenie, czas)
    if wynik["kod"] in (BLAD, LIMIT, CZAS) and droga == "agy" and zapas == "api":
        pierwszy = {k: wynik.get(k) for k in ("kod", "status", "czas_s", "stderr")}
        wynik = przez_api(model, polecenie, czas)
        wynik["po_nieudanym_agy"] = pierwszy
    return wynik


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--model", required=True)
    p.add_argument("--polecenie", required=True, type=Path)
    p.add_argument("--wynik", required=True, type=Path)
    p.add_argument("--czas", type=int, default=900)
    p.add_argument("--droga", choices=["agy", "api"], default="agy")
    p.add_argument("--zapas", choices=["api", "brak"], default="api")
    a = p.parse_args(argv)
    if not a.polecenie.is_file():
        print(f"brak pliku polecenia: {a.polecenie}", file=sys.stderr)
        return ZLY_ARGUMENT
    wynik = zlec(a.model, a.polecenie.read_text(encoding="utf-8"), a.czas, a.droga, a.zapas)
    wynik["polecenie"] = str(a.polecenie)
    a.wynik.parent.mkdir(parents=True, exist_ok=True)
    if wynik["droga"] == "agy":
        myslenie = myslenie_z_rozmowy(wynik.get("conversation_id"), wynik.get("odpowiedz", ""))
        if myslenie:
            a.wynik.with_name(a.wynik.stem + "-myslenie.md").write_text(myslenie, encoding="utf-8")
    a.wynik.write_text(json.dumps(wynik, ensure_ascii=False, indent=2), encoding="utf-8")
    u = wynik.get("uzycie", {})
    print(f"{wynik['droga']} {wynik['model']} kod={wynik['kod']} status={wynik['status']} "
          f"czas={wynik.get('czas_s')}s wejście={u.get('input_tokens')} wyjście={u.get('output_tokens')} "
          f"myślenie={u.get('thinking_tokens')}")
    return wynik["kod"]


if __name__ == "__main__":
    sys.exit(main())
