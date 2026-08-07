import sys; sys.path.insert(0, '..')
from validator import validate


def test_inversion():
    r = validate("x**(-1)")
    assert r["moebius"]["inversion"] is True
    assert r["moebius"]["moebius_density"] >= 2

def test_no_inversion():
    r = validate("x**2 + 1")
    assert r["moebius"]["inversion"] is False

def test_high_density():
    r = validate("1/(x**(-1) + 1)")
    assert r["moebius"]["moebius_density"] >= 3
