"""
test_prime_spectrum_filter.py — rozszerzony po portowaniu naprawy z
math-validator-3.0 (rekalibracja na model Cramera/Gallaghera, patrz
naglowek filters/prime_spectrum_filter.py). To repo mialo jeszcze
ORYGINALNA, nigdy nie naprawiona wersje tego filtra (sztywny prog 0.25,
niepoparte twierdzenie o TIMDR) - ta sesja portuje obie naprawy naraz.
"""
from validator import validate
from filters import prime_spectrum_filter as psf
import numpy as np


def test_prime_spectrum_small():
    result = validate("1000")["filters"]
    ps = result["prime_spectrum"]

    assert ps["status"] == "ok"
    assert ps["prime_count"] > 0
    assert isinstance(ps["primes"], list)
    assert isinstance(ps["gaps"], list)
    assert isinstance(ps["ratios"], list)


def test_prime_spectrum_non_integer():
    result = validate("x + 1")["filters"]
    assert result["prime_spectrum"]["status"] == "skip"


def test_male_n_daje_insufficient_data_nie_zgaduje():
    """Naprawa: N=999999 dawal kiedys PEWNA etykiete "log_spiral_1_over_f"
    na 24 lukach. Po naprawie: <30 luk -> filtr jawnie mowi "za malo
    danych", zamiast klasyfikowac."""
    result = validate("999999")["filters"]
    ps = result["prime_spectrum"]
    assert ps["prime_count"] < 31
    assert ps["spectrum_type"] == "insufficient_data_for_cramer_test"
    assert ps["mean_normalized_gap"] is None


def test_wystarczajaco_duze_n_daje_pelna_klasyfikacje():
    result = validate("2100000")["filters"]
    ps = result["prime_spectrum"]
    assert ps["prime_count"] - 1 >= 30
    assert ps["spectrum_type"] in ("cramer_consistent", "cramer_finite_size_deviation")
    assert ps["mean_normalized_gap"] is not None
    assert ps["ks_pvalue"] is not None
    assert 0.0 <= ps["ks_pvalue"] <= 1.0


def test_brak_starej_etykiety_log_spiral():
    for n in ["50", "5000", "999999", "2100000"]:
        ps = validate(n)["filters"]["prime_spectrum"]
        assert ps.get("spectrum_type") != "log_spiral_1_over_f"
        all_notes = " ".join(ps.get("notes", []))
        assert "log_spiral" not in all_notes
        assert "Λ–τ–ρ" not in all_notes


def test_ks_nie_odrzuca_prawdziwego_exp1():
    rng = np.random.default_rng(0)
    x = list(rng.exponential(1.0, size=2000))
    d, p = psf._ks_two_sided_vs_exp1(x)
    assert p > 0.05


def test_ks_odrzuca_ciag_staly():
    x = [1.0] * 2000
    d, p = psf._ks_two_sided_vs_exp1(x)
    assert p < 0.01


def test_prawdziwe_pierwsze_do_10_6_replikuja_wynik_sesji_kalibracyjnej():
    from sympy import primerange
    primes = list(primerange(2, 10**6 + 1))
    assert len(primes) == 78498
    gaps = [primes[i + 1] - primes[i] for i in range(len(primes) - 1)]
    x = psf._normalized_gaps(primes, gaps)
    mean_x = sum(x) / len(x)
    assert 0.95 < mean_x < 1.05
    r, p = psf._serial_pearson_r(x)
    assert -0.1 < r < -0.02
    assert p < 1e-10
