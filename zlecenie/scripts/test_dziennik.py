"""Testy liczenia zużycia w dzienniku (python3 -X utf8 -m pytest test_dziennik.py)."""
import json
import os
import subprocess
import sys
from pathlib import Path

SKRYPT = Path(__file__).with_name("dziennik.py")


def wpis(rid, wej, odczyt, zapis, wyj, model="claude-opus-5-5"):
    return json.dumps({"type": "assistant", "requestId": rid, "message": {"model": model, "usage": {
        "input_tokens": wej, "cache_read_input_tokens": odczyt,
        "cache_creation_input_tokens": zapis, "output_tokens": wyj}}})


def uruchom(*argi, srodowisko):
    # Testy biegną wewnątrz Claude Code, więc identyfikator prawdziwej rozmowy usuwamy, chyba że test go podaje.
    env = {k: v for k, v in os.environ.items() if k != "CLAUDE_CODE_SESSION_ID"}
    return subprocess.run([sys.executable, "-X", "utf8", str(SKRYPT), *argi], capture_output=True,
                          text=True, env={**env, **srodowisko})


def zacznij(env):
    return uruchom("start", "--projekt", "P", "--zadanie", "Z", "--rodzaj", "R", "--model", "m",
                   "--poziom", "l", srodowisko=env)


def przygotuj(tmp_path):
    rozmowa = tmp_path / "projekty" / "p" / "abc.jsonl"
    rozmowa.parent.mkdir(parents=True)
    # ten sam requestId dwa razy liczy się raz (Claude Code zapisuje kilka bloków jednej odpowiedzi)
    rozmowa.write_text("\n".join([wpis("r1", 10, 1000, 100, 5), wpis("r1", 10, 1000, 100, 5),
                                  wpis("r2", 1, 2000, 0, 9), '{"type":"user"}']), encoding="utf-8")
    pomocnik = tmp_path / "projekty" / "p" / "abc" / "subagents" / "agent-x.jsonl"
    pomocnik.parent.mkdir(parents=True)
    pomocnik.write_text(wpis("s1", 0, 500, 50, 50, "claude-sonnet-5-5"), encoding="utf-8")
    return rozmowa


def test_zuzycie_liczy_rozmowe_i_pomocnikow(tmp_path):
    rozmowa = przygotuj(tmp_path)
    w = uruchom("zuzycie", "--rozmowa", str(rozmowa), srodowisko={})
    assert w.returncode == 0, w.stderr
    pierwsza = w.stdout.splitlines()[0]
    assert pierwsza == "3725"  # 1115 + 2010 rozmowa, 600 pomocnik
    assert "pomocnicy 600" in w.stdout


def test_zuzycie_bez_wskazania_bierze_rozmowe_z_identyfikatora_sesji(tmp_path):
    przygotuj(tmp_path)
    w = uruchom("zuzycie", srodowisko={"ZLECENIA_PROJEKTY": str(tmp_path / "projekty"),
                                        "CLAUDE_CODE_SESSION_ID": "abc"})
    assert w.stdout.splitlines()[0] == "3725"


def test_koniec_nie_liczy_nowszej_cudzej_rozmowy(tmp_path):
    # 26.11.2026: wiersze 12 i 15 dziennika dostały po 20,71 mln tokenów z tej samej, cudzej rozmowy,
    # bo program brał najnowszy zapis ze wszystkich projektów.
    przygotuj(tmp_path)
    cudza = tmp_path / "projekty" / "inny" / "xyz.jsonl"
    cudza.parent.mkdir(parents=True)
    cudza.write_text(wpis("c1", 99999, 0, 0, 0), encoding="utf-8")
    env = {"ZLECENIA_DZIENNIK": str(tmp_path / "d.csv"), "ZLECENIA_PROJEKTY": str(tmp_path / "projekty"),
           "CLAUDE_CODE_SESSION_ID": "abc"}
    zacznij(env)
    w = uruchom("koniec", "--id", "1", "--wynik", "osiagniety", "--dowod", "x", srodowisko=env)
    assert w.returncode == 0, w.stderr
    assert ";3725;" in (tmp_path / "d.csv").read_text(encoding="utf-8-sig")


def test_koniec_bez_zapisu_rozmowy_zostawia_puste_tokeny(tmp_path):
    # Uwaga 6 zewnętrznego testera (26.11.2026): brak pomiaru zapisywał się jako 0 i zaniżał średnią.
    (tmp_path / "projekty").mkdir()
    env = {"ZLECENIA_DZIENNIK": str(tmp_path / "d.csv"), "ZLECENIA_PROJEKTY": str(tmp_path / "projekty")}
    zacznij(env)
    w = uruchom("koniec", "--id", "1", "--wynik", "osiagniety", "--dowod", "x", srodowisko=env)
    assert w.returncode == 0, w.stderr
    wiersz = (tmp_path / "d.csv").read_text(encoding="utf-8-sig").splitlines()[1].split(";")
    assert wiersz[13] == ""
    assert "nie policzyłem tokenów" in w.stderr


def test_zajeta_blokada_nie_dopuszcza_zapisu(tmp_path):
    # Uwaga 7 zewnętrznego testera (26.11.2026): trzy równoległe przebiegi pisały do jednego pliku bez blokady.
    dziennik = tmp_path / "d.csv"
    (tmp_path / "d.csv.lock").write_text("inny przebieg", encoding="utf-8")
    w = zacznij({"ZLECENIA_DZIENNIK": str(dziennik), "ZLECENIA_BLOKADA_CZAS": "1"})
    assert w.returncode != 0
    assert not dziennik.exists()


def test_rownolegle_starty_dostaja_rozne_numery(tmp_path):
    env = {**{k: v for k, v in os.environ.items() if k != "CLAUDE_CODE_SESSION_ID"},
           "ZLECENIA_DZIENNIK": str(tmp_path / "d.csv")}
    procesy = [subprocess.Popen([sys.executable, "-X", "utf8", str(SKRYPT), "start", "--projekt", "P",
                                 "--zadanie", f"Z{i}", "--rodzaj", "R", "--model", "m", "--poziom", "l"],
                                stdout=subprocess.PIPE, text=True, env=env) for i in range(8)]
    numery = sorted(int(p.communicate()[0]) for p in procesy)
    assert numery == list(range(1, 9))
    assert len((tmp_path / "d.csv").read_text(encoding="utf-8-sig").splitlines()) == 9


def test_koniec_bez_tokenow_wpisuje_policzone(tmp_path):
    rozmowa = przygotuj(tmp_path)
    env = {"ZLECENIA_DZIENNIK": str(tmp_path / "d.csv")}
    uruchom("start", "--projekt", "P", "--zadanie", "Z", "--rodzaj", "R", "--model", "m", "--poziom", "l",
            srodowisko=env)
    w = uruchom("koniec", "--id", "1", "--wynik", "osiagniety", "--dowod", "x", "--rozmowa", str(rozmowa),
                srodowisko=env)
    assert w.returncode == 0, w.stderr
    assert ";3725;" in (tmp_path / "d.csv").read_text(encoding="utf-8-sig")
