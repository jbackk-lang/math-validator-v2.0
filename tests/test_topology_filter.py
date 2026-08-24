from validator import validate

# NAPRAWIONO: "x^2 + y^2 = 1" i "y = 2*x + 1" nie są poprawnym wejściem dla
# core.parse() — gołe "=" to w Pythonie przypisanie, nie równość, więc
# sympify rzuca SyntaxError już na etapie parsowania (potwierdzone
# empirycznie: result["filters"]["topology"] == {"ok": False, "error": ...}).
# Prawidłowy zapis równości w tym systemie wymaga Eq(...) albo "==".
# Oryginalny test zakładał klucz "status" (["ok","skip"]), którego topology
# filter nigdy nie zwraca (ma "ok"/"domain"/"is_all_reals" przy sukcesie,
# "ok"/"error" przy błędzie) — testy przepisano na realne zachowanie.

def test_topology_bare_equals_is_parse_error():
    result = validate("x^2 + y^2 = 1")["filters"]
    topo = result["topology"]

    assert topo["ok"] is False
    assert "error" in topo


def test_topology_line_bare_equals_is_parse_error():
    result = validate("y = 2*x + 1")["filters"]
    topo = result["topology"]

    assert topo["ok"] is False


def test_topology_domain_with_singularity():
    result = validate("1/x")["filters"]
    topo = result["topology"]

    assert topo["ok"] is True
    assert topo["is_all_reals"] is False
    assert "0" in topo["domain"]


def test_topology_domain_all_reals():
    result = validate("x**2 - 4")["filters"]
    topo = result["topology"]

    assert topo["ok"] is True
    assert topo["is_all_reals"] is True
    assert topo["domain"] == "Reals"
