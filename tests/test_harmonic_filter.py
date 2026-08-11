from validator import validate

def test_harmonic_sin():
    result = validate("sin(x)")["filters"]
    h = result["harmonic"]

    assert h["status"] in ["ok", "skip", "error"]
    assert "notes" in h
    assert h["harmonic"] is True
    assert h["trig_count"] == 1
