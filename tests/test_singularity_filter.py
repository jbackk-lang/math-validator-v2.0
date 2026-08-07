from validator import validate

def test_singularity_simple():
    result = validate("1/x")
    sing = result["singularity"]

    assert sing["status"] == "ok"
    assert "singularities" in sing


def test_singularity_none():
    result = validate("x + 1")
    sing = result["singularity"]

    assert sing["status"] == "ok"
