from validator import validate

def test_logic_basic():
    # NAPRAWIONO: logic_filter zwraca "ok" (bool, zawsze True gdy parse się
    # udał) + "issues" (lista) + "is_finite" — nie ma klucza "status".
    result = validate("(x and y) or not z")["filters"]
    lg = result["logic"]

    assert lg["ok"] is True
    assert lg["is_finite"] is True
    assert lg["issues"] == []
