import sys; sys.path.insert(0, '..')
from validator import validate


def test_syntax_ok():
    r = validate("x + 1")["filters"]
    assert r["syntax"]["ok"] is True

def test_syntax_error():
    # NAPRAWIONO: syntax_filter nie ma klucza "status" (str), tylko "ok" (bool)
    # + listę "issues". Oryginalny test odwoływał się do r["syntax"]["status"],
    # który nigdy nie istniał w tym filtrze.
    r = validate("x ++++ (")["filters"]
    assert r["syntax"]["ok"] is False
    assert "unbalanced_parens" in r["syntax"]["issues"]
    assert "double_operator" in r["syntax"]["issues"]

def test_tautology_simplified():
    # NAPRAWIONO: logic_filter nie zwraca klucza "verdict" — nigdy nie zwracał
    # (issues/is_finite/ok). Wykrywanie "upraszcza się, ale ma ukrytą
    # osobliwość" faktycznie leży w misleading_filter (hidden_singularity)
    # i singularity_filter (ρ_defects=1, status=singularity_found), więc test
    # sprawdza teraz właściwe filtry zamiast nieistniejącego pola.
    r = validate("(x+1)/(x+1)")["filters"]
    assert r["singularity"]["status"] == "singularity_found"
    assert r["singularity"]["ρ_defects"] == 1
    assert any("hidden_singularity" in issue for issue in r["misleading"]["misleading_issues"])

def test_clean_no_singularities():
    r = validate("x**2 - 4")["filters"]
    assert r["singularity"]["ρ_defects"] == 0
    assert r["singularity"]["twists"] == 0
