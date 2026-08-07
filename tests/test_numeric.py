import sys; sys.path.insert(0, '..')
from validator import validate


def test_quadratic_solutions():
    r = validate("x**2 - 4")
    assert r["numeric"]["status"] == "ok"
    sols = r["numeric"]["solutions"]
    assert "-2" in sols and "2" in sols

def test_no_real_solutions():
    r = validate("x**2 + 1")
    assert r["numeric"]["status"] == "ok"
    assert r["numeric"]["solutions"] == []
    assert len(r["numeric"]["complex_solutions"]) == 2

def test_linear():
    r = validate("x - 5")
    assert "5" in r["numeric"]["solutions"]
