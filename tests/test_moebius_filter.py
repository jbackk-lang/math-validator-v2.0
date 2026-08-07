from validator import validate

def test_moebius_basic():
    result = validate("x^2 - 1")
    m = result["moebius"]

    assert m["status"] in ["ok", "skip"]
    assert "notes" in m
