"""Testy agy_zlec.py na sztucznym `agy` (bez sieci i bez limitu Google)."""
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent))
import agy_zlec  # noqa: E402

SZTUCZNY = '''import json, os, sys
tryb = os.environ["SZTUCZNY_TRYB"]
zapis = os.environ.get("SZTUCZNY_ZAPIS")
if zapis:
    open(zapis, "w", encoding="utf-8").write(json.dumps({"argv": sys.argv[1:], "cwd": os.getcwd(),
        "home": os.environ.get("USERPROFILE"), "stdin_tty": sys.stdin.isatty()}))
if tryb == "ok":
    print(json.dumps({"status": "SUCCESS", "response": "odpowiedz", "usage": {"input_tokens": 5}}))
elif tryb == "limit":
    sys.stderr.write('AGY_ERROR: {"status": "RESOURCE_EXHAUSTED", "message": "weekly quota"}\\n'); sys.exit(3)
elif tryb == "czas":
    sys.stderr.write("[agy] print timeout after 5s\\n"); sys.exit(3)
elif tryb == "pusty":
    print(json.dumps({"status": "SUCCESS", "response": ""}))
'''


@pytest.fixture
def agy(tmp_path, monkeypatch):
    skrypt = tmp_path / "sztuczny_agy.py"
    skrypt.write_text(SZTUCZNY, encoding="utf-8")
    monkeypatch.setenv("AGY_BIN", json.dumps([sys.executable, str(skrypt)]))
    monkeypatch.setattr(agy_zlec, "BAZA", tmp_path / "baza")
    zapis = tmp_path / "wywolanie.json"
    monkeypatch.setenv("SZTUCZNY_ZAPIS", str(zapis))

    def ustaw(tryb):
        monkeypatch.setenv("SZTUCZNY_TRYB", tryb)
        return zapis
    return ustaw


def test_sukces_i_izolacja(agy, tmp_path):
    zapis = agy("ok")
    w = agy_zlec.zlec("gemini-4-hydrogen-low", "pytanie", czas=30, zapas="brak")
    assert w["kod"] == agy_zlec.OK and w["odpowiedz"] == "odpowiedz"
    wyw = json.loads(zapis.read_text(encoding="utf-8"))
    argv = wyw["argv"]
    assert "--mode" not in argv and "--sandbox" in argv
    assert "--disable-slash-commands" not in argv
    ustawienia = json.loads(argv[argv.index("--settings") + 1])
    assert ustawienia["useG1Credits"] is False and "write_file(*)" in ustawienia["permissions"]["deny"]
    assert Path(wyw["home"]) == tmp_path / "baza" / "dom"
    assert Path(wyw["cwd"]) == tmp_path / "baza" / "praca"


@pytest.mark.parametrize("tryb,kod", [("limit", agy_zlec.LIMIT), ("czas", agy_zlec.CZAS),
                                      ("pusty", agy_zlec.BLAD)])
def test_kody_bledow_bez_zapasu(agy, tryb, kod):
    agy(tryb)
    assert agy_zlec.zlec("gemini-4-neon-high", "x", czas=30, zapas="brak")["kod"] == kod


def test_zapas_api_po_limicie(agy, monkeypatch):
    agy("limit")
    monkeypatch.setattr(agy_zlec, "przez_api",
                        lambda m, p, c: {"droga": "api", "model": m, "kod": 0, "status": "STOP"})
    w = agy_zlec.zlec("gemini-4-neon-high", "x", czas=30, zapas="api")
    assert w["droga"] == "api" and w["kod"] == 0
    assert w["po_nieudanym_agy"]["kod"] == agy_zlec.LIMIT


def test_za_dlugie_polecenie(agy):
    agy("ok")
    w = agy_zlec.zlec("gemini-4-neon-high", "a" * (agy_zlec.GRANICA_ZNAKOW + 1), zapas="api")
    assert w["kod"] == agy_zlec.ZLY_ARGUMENT


def test_rozbij_model():
    assert agy_zlec.rozbij_model("gemini-4-neon-xhigh") == ("gemini-4-neon", "xhigh")
    assert agy_zlec.rozbij_model("gemini-3.8-flash-medium") == ("gemini-3.8-flash", "medium")
    assert agy_zlec.rozbij_model("gemini-4-neon") == ("gemini-4-neon", None)
