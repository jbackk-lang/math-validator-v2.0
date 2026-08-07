from validator import validate

def test_harmonic_sin():
    result = validate("sin(x)")
    h = result["harmonic"]

    assert h["status"] in ["ok", "skip"]
    assert "notes" in h
