from validator import validate

def test_prime_spectrum_small():
    result = validate("1000")
    ps = result["prime_spectrum"]

    assert ps["status"] == "ok"
    assert ps["prime_count"] > 0
    assert isinstance(ps["primes"], list)
    assert isinstance(ps["gaps"], list)
    assert isinstance(ps["ratios"], list)


def test_prime_spectrum_non_integer():
    result = validate("x + 1")
    assert result["prime_spectrum"]["status"] == "skip"
