from validator import validate

def test_syntax_valid():
    result = validate("x + 1")["filters"]
    syn = result["syntax"]

    assert syn["ok"] is True
    assert syn["issues"] == []


def test_syntax_invalid():
    result = validate("x + ")["filters"]
    syn = result["syntax"]

    assert syn["ok"] is False
    assert syn["trailing_operator"] is True
