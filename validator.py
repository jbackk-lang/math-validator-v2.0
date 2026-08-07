"""
validator.py — jedyny publiczny entry point systemu jbackk-lang/math-validator-2.0.

Poprawki v2:
  1. StabilityLayer przeniesiony do scope'u per-request (bezpieczeństwo asynchroniczne/wielowątkowe).
  2. Jedna, jednoznaczna definicja funkcji validate().
  3. Pełna optymalizacja AST — parse() wywoływane RAZ dla całego potoku.
  4. Wszystkie filtry topologiczne i algebraiczne wywoływane sekwencyjnie przez słownik mapowania.
"""

from typing import Optional, Dict, Any, Callable
from core import parse

# Importy filtrów bazowych i zaawansowanych
from filters.information_filter    import run as information_run
from filters.syntax_filter         import run as syntax_run
from filters.algebra_filter        import run as algebra_run
from filters.logic_filter          import run as logic_run
from filters.numeric_filter        import run as numeric_run
from filters.harmonic_filter       import run as harmonic_run
from filters.moebius_filter        import run as moebius_run
from filters.topology_filter       import run as topology_run
from filters.singularity_filter    import run as singularity_run
from filters.prime_spectrum_filter import run as prime_spectrum_run
from filters.misleading_filter     import run as misleading_run

# Słownik rejestracji filtrów potoku walidacji
FILTERS: Dict[str, Callable[[Any], Any]] = {
    "information":    information_run,
    "syntax":         syntax_run,
    "algebra":        algebra_run,
    "logic":          logic_run,
    "numeric":        numeric_run,
    "harmonic":       harmonic_run,
    "moebius":        moebius_run,
    "topology":       topology_run,
    "singularity":    singularity_run,
    "prime_spectrum": prime_spectrum_run,
    "misleading":     misleading_run,
}


# ── StabilityLayer Λ–τ–ρ ─────────────────────────────────────────────────────

class StabilityLayer:
    """
    Warstwa stabilności Λ→τ→ρ. Kontroluje ewolucję 10 pętli układu z bifurkacją po 5. kroku.

    Użycie per-request/per-session (izolacja stanu w środowiskach wielowątkowych typu FastAPI):
        session = StabilityLayer()
        result  = validate("x**2 + sin(x)", stability=session)
    """

    def __init__(self) -> None:
        self.loop_index: int = 0

    def step(self) -> Dict[str, Any]:
        """
        Wykonuje pojedynczy krok ewolucji fazowej na trójpętlowym toroidzie.
        Zwraca aktualny stan metryki układu.
        """
        self.loop_index += 1
        angle = 72 * self.loop_index

        # Detekcja punktu bifurkacji (5 pętli)
        if self.loop_index <= 5:
            phase = "UNDEFINED"        # Stan nieoznaczony / inicjalizacja trajektorii
        else:
            phase = "FORCED"           # System dąży do wymuszonego domknięcia topologicznego

        # Określenie orientacji przestrzennej na wstędze Möbiusa
        if phase == "FORCED" and angle < 720:
            orientation = "RETURNING"
        elif angle >= 720:
            orientation = "CLOSED"     # Domknięcie struktury (M²-closure)
        else:
            orientation = "M_PRIME"

        return {
            "cycle":       self.loop_index,
            "angle":       angle,
            "phase":       phase,
            "orientation": orientation,
        }


# ── Główny Punkt Wejścia (Public Entry Point) ────────────────────────────────

def validate(equation: str, stability: Optional[StabilityLayer] = None) -> Dict[str, Dict[str, Any]]:
    """
    Parsuje wejściowe wyrażenie matematyczne dokładnie raz, po czym przepuszcza je
    przez pełen zestaw filtrów topologiczno-algebraicznych Λ–τ–ρ.

    Parametry:
        equation  : Wyrażenie matematyczne w postaci ciągu znaków (str).
        stability : Instancja warstwy stabilności (StabilityLayer). 
                    W przypadku braku (None), tworzy instancję lokalną (stateless).

    Zwraca:
        Słownik zawierający szczegółowe wyniki poszczególnych filtrów oraz
        aktualny stan ewolucji warstwy stabilności.
    """
    # Zabezpieczenie przed współdzieleniem stanu (Thread-Safety Guard)
    if stability is None:
        stability = StabilityLayer()

    # Optymalizacja: Parsowanie AST wykonywane dokładnie jeden raz
    parsed_expression = parse(equation)
    
    # Przetwarzanie potokowe przez zarejestrowane filtry strukturalne
    filter_results = {name: filter_fn(parsed_expression) for name, filter_fn in FILTERS.items()}
    
    # Wyznaczenie kroku ewolucji fazy topologicznej
    stability_state = stability.step()

    return {
        "filters":    filter_results,
        "stability": stability_state,
    }
