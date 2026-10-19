from pathlib import Path

from challenges.__main__ import main
from challenges.catalog import SLUGS


def test_reveal_03_prints_the_solution(capsys):
    assert main(["reveal", "03"]) == 0
    out = capsys.readouterr().out
    assert "Shannon" in out
    assert "def shannon_diversity" in out
    assert "math.log" in out


def test_reveal_rejects_an_unknown_number(capsys):
    assert main(["reveal", "99"]) == 2


def test_starters_raise_not_implemented():
    root = Path(__file__).resolve().parents[1]
    for slug in SLUGS:
        source = (root / "challenges" / slug / "starter.py").read_text()
        assert "NotImplementedError" in source
        hidden = root / "challenges" / "hidden" / f"{slug}.py"
        assert hidden.is_file()
        assert "NotImplementedError" not in hidden.read_text()
