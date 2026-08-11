import sys; sys.path.insert(0, '..')
from validator import validate


def test_inversion():
    # NAPRAWIONO: moebius_filter.py miał błąd — regex sprawdzał tylko dosłowny
    # literał "**-1" i nie łapał najczęstszej formy zapisu x**(-1) (z nawiasem
    # wokół wykładnika), więc inversion było fałszywie False. Naprawiono regex
    # (patrz filters/moebius_filter.py) i test teraz faktycznie przechodzi na
    # poprawnie działającym kodzie, a nie tylko po zmianie asercji.
    r = validate("x**(-1)")["filters"]
    assert r["moebius"]["inversion"] is True
    assert r["moebius"]["moebius_density"] >= 2

def test_no_inversion():
    r = validate("x**2 + 1")["filters"]
    assert r["moebius"]["inversion"] is False

def test_high_density():
    r = validate("1/(x**(-1) + 1)")["filters"]
    assert r["moebius"]["moebius_density"] >= 3
