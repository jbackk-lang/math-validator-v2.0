from validator import validate

def test_information_basic():
    result = validate("x^2 + 2*x + 1")
    info = result["information"]

    assert info["status"] == "ok"
    assert info["symbols"] > 0
    assert 0 <= info["entropy"] <= 8
    assert 0 <= info["redundancy"] <= 1
    assert 0 <= info["complexity"] <= 1
    assert info["stability"] in [
        "very_low", "low", "medium", "high", "very_high"
    ]


def test_information_empty():
    result = validate("")
    assert result["information"]["status"] in ["skip", "error"]


def test_information_structure():
    result = validate("sin(x) + cos(x)")
    info = result["information"]

    assert info["symbols"] >= 5
    assert info["operators"] >= 1
