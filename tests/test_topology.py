import sys; sys.path.insert(0, '..')
from validator import validate


def test_twist_detected_1_over_x():
    r = validate("1/x")
    assert r["topology"]["status"] == "twist_detected"
    assert r["topology"]["twists"] == 1
    s = r["topology"]["singularities"][0]
    assert s["point"] == "0"
    assert s["lim_plus"]  == "oo"
    assert s["lim_minus"] == "-oo"
    assert s["twist"] is True

def test_two_twists():
    r = validate("x/(x**2-1)")
    assert r["topology"]["ρ_defects"] == 2
    assert r["topology"]["twists"] == 2

def test_four_twists():
    r = validate("x**3/(x**4-1)")
    assert r["topology"]["ρ_defects"] == 4
    assert r["topology"]["twists"] == 4

def test_zoo_twist():
    r = validate("1/(x-x)")
    assert r["topology"]["status"] == "twist_detected"
    assert r["topology"]["twists"] == 1

def test_no_twist_polynomial():
    r = validate("x**2 - 4")
    assert r["topology"]["ρ_defects"] == 0
    assert r["topology"]["twists"] == 0

def test_lambda_structure():
    r = validate("x/(x**2-1)")
    lam = r["topology"]["Λ_structure"]
    assert lam["fractions"] >= 1
    assert lam["powers"] >= 1
