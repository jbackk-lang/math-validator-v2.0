import sys; sys.path.insert(0, '..')
from validator import validate


def test_division_by_zero():
    r = validate("1/(x-x)")
    assert r["algebra"]["status"] == "error"

def test_clean_expr():
    r = validate("x**2 - 4")
    assert r["algebra"]["status"] == "ok"

def test_no_singularity_polynomial():
    r = validate("x**3 + x + 1")
    assert r["algebra"]["status"] == "ok"
    assert r["singularity"]["ρ_defects"] == 0
