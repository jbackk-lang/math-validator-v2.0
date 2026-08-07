from validator import validate

def test_logic_basic():
    result = validate("(x and y) or not z")
    lg = result["logic"]

    assert lg["status"] in ["ok", "skip"]
