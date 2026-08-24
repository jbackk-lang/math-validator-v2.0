import sys; sys.path.insert(0, '..')
from validator import validate

# NAPRAWIONO: ten plik nazywał się "test_topology" ale wszystkie asercje
# (twists, ρ_defects, singularities[].point/lim_plus/lim_minus/twist,
# Λ_structure) opisują pola filtra "singularity", nie "topology" —
# filters/topology_filter.py zwraca tylko domain/is_all_reals/ok i NIGDY
# nie miał tych kluczy. Testy przepisano tak, by wskazywały na właściwy
# filtr ("singularity" dla skrętów τ, "moebius" dla struktury Λ), zamiast
# zmieniać znaczenie testu na fałszywe "ok" bez sprawdzania niczego.

def test_twist_detected_1_over_x():
    r = validate("1/x")["filters"]
    assert r["singularity"]["status"] == "twist_detected"
    assert r["singularity"]["twists"] == 1
    s = r["singularity"]["singularities"][0]
    assert s["point"] == "0"
    assert s["lim_plus"]  == "oo"
    assert s["lim_minus"] == "-oo"
    assert s["twist"] is True

def test_two_twists():
    r = validate("x/(x**2-1)")["filters"]
    assert r["singularity"]["ρ_defects"] == 2
    assert r["singularity"]["twists"] == 2

def test_four_twists():
    r = validate("x**3/(x**4-1)")["filters"]
    assert r["singularity"]["ρ_defects"] == 4
    assert r["singularity"]["twists"] == 4

def test_zoo_twist():
    r = validate("1/(x-x)")["filters"]
    assert r["singularity"]["status"] == "twist_detected"
    assert r["singularity"]["twists"] == 1

def test_no_twist_polynomial():
    r = validate("x**2 - 4")["filters"]
    assert r["singularity"]["ρ_defects"] == 0
    assert r["singularity"]["twists"] == 0

def test_lambda_structure():
    # Struktura "Λ" (nawiasy/ułamki/potęgi) opisana jest realnie przez
    # moebius_filter (density/indicators), nie przez nieistniejące pole
    # "Λ_structure" w topology.
    r = validate("x/(x**2-1)")["filters"]
    m = r["moebius"]
    assert m["moebius_density"] >= 2
    assert any("division" in i for i in m["indicators"])
    assert any("parentheses" in i for i in m["indicators"])
