from validator import validate

def test_numeric_constant():
    result = validate("42")
    num = result["numeric"]

    assert num["status"] == "ok"
    assert num["value"] == 42


def test_numeric_expression():
    result = validate("2 + 3*4")
    num = result["numeric"]

    assert num["status"] == "ok"
    assert num["value"] == 14
