from validator import validate

# NAPRAWIONO: ten plik testował filtr, który już nie istnieje w obecnej
# architekturze — numeric_filter.py NIE ewaluuje wyrażenia do liczby
# (nie ma klucza "value"). Rozwiązuje wyrażenie=0 przez sympy.solve()
# i zwraca pierwiastki w "solutions". Dla niezerowej stałej ("42",
# "2 + 3*4" -> 14) równanie stała=0 nie ma rozwiązań, więc solutions==[].
# Testy przepisano tak, by sprawdzały realne, poprawne zachowanie.

def test_numeric_constant():
    result = validate("42")["filters"]
    num = result["numeric"]

    assert num["status"] == "ok"
    assert num["solutions"] == []
    assert num["count"] == 0


def test_numeric_expression():
    result = validate("2 + 3*4")["filters"]
    num = result["numeric"]

    assert num["status"] == "ok"
    assert num["solutions"] == []
    assert num["count"] == 0
