from validator import validate

def test_singularity_simple():
    # NAPRAWIONO: dla "1/x" filtr faktycznie wykrywa skręt τ w x=0
    # (lim 0+ = +oo, lim 0- = -oo), więc status to "twist_detected", nie "ok".
    result = validate("1/x")["filters"]
    sing = result["singularity"]

    assert sing["status"] == "twist_detected"
    assert sing["twists"] == 1
    assert "singularities" in sing


def test_singularity_none():
    result = validate("x + 1")["filters"]
    sing = result["singularity"]

    assert sing["status"] == "ok"
    assert sing["ρ_defects"] == 0
