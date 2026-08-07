from validator import validate

def test_syntax_valid():
    result = validate("x + 1")
    syn = result["syntax"]

    assert syn["status"] == "ok"


def test_syntax_invalid():
    result = validate("x + ")
    syn = result["syntax"]

    assert syn["status"] == "error"
