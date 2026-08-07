import sys; sys.path.insert(0, '..')
from validator import validate


def test_syntax_ok():
    r = validate("x + 1")
    assert r["syntax"]["status"] == "ok"

def test_syntax_error():
    r = validate("x ++++ (")
    assert r["syntax"]["status"] == "error"

def test_tautology_simplified():
    r = validate("(x+1)/(x+1)")
    assert r["logic"]["verdict"] == "simplified_with_hidden_singularity"

def test_clean_no_singularities():
    r = validate("x**2 - 4")
    assert r["singularity"]["ρ_defects"] == 0
    assert r["singularity"]["twists"] == 0
