# filters/tourosomobius_filter.py
# Klasyfikacja Λ–τ–ρ dla struktur tourosomobius

def classify(L, t, r):
    if L == 0 and t == 0 and r == 0:
        return "trywialny"
    if L in (0.5, 1.5):
        return "niedokonczony"
    if L == 0 and t > 0 and r == 0:
        return "torusowy"
    if L == 0 and t == 0 and r > 0:
        return "helikalny"
    if L == 0 and t > 0 and r > 0:
        return "mieszany"
    if L in (1, 2) and t >= 2 and r >= 2:
        return "stabilny"
    if L in (1, 2):
        return "rozdzielony"
    return "nieokreślony"


def run(parsed):
    """
    Oczekuje, że parsed.expr zawiera trzy parametry:
    Λ, τ, ρ — np. jako liczby lub symbole.
    Jeśli nie — filtr zwraca neutralny wynik.
    """

    try:
        L = float(parsed.get("Lambda", 0))
        t = float(parsed.get("Tau", 0))
        r = float(parsed.get("Rho", 0))
    except Exception:
        return {
            "valid": False,
            "error": "Brak parametrów Λ–τ–ρ",
            "class": None
        }

    cls = classify(L, t, r)

    return {
        "valid": True,
        "Lambda": L,
        "Tau": t,
        "Rho": r,
        "class": cls,
        "is_trivial": cls == "trywialny",
        "is_unfinished": cls == "niedokonczony",
        "is_stable": cls == "stabilny",
        "is_split": cls == "rozdzielony",
        "is_torus_only": cls == "torusowy",
        "is_helix_only": cls == "helikalny",
        "is_mixed": cls == "mieszany"
    }
