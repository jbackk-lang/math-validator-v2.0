from validator import validate

def test_moebius_basic():
    # NAPRAWIONO: moebius_filter nie zwraca klucza "notes" — realne pole to
    # "indicators" (lista wskaźników wykrytych struktur Möbiusa).
    result = validate("x^2 - 1")["filters"]
    m = result["moebius"]

    assert m["status"] in ["ok", "skip", "error"]
    assert "indicators" in m
    assert m["indicators"] == []
    assert m["level"] == "none"
