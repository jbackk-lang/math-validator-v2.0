# filter_252.py
# Filtr dopuszczalności stanów F4-RED (252 konfiguracje)
# Wersja zgodna z TIMDER PC

from dataclasses import dataclass
from typing import List


@dataclass
class F4State:
    """
    Stan F4-RED: 9 pierwiastków strukturalnych (ΔS, τ, Λ × 3 ramiona)
    Każdy w stanie +1 lub -1.
    """
    bits: List[int]

    def is_valid(self) -> bool:
        if len(self.bits) != 9:
            return False
        if any(b not in (-1, 1) for b in self.bits):
            return False

        n_plus = sum(1 for b in self.bits if b == 1)
        n_minus = 9 - n_plus

        return abs(n_plus - n_minus) <= 1


class F4Filter252:
    """
    Filtr dopuszczalności: przepuszcza tylko 252 stany F4-RED.
    """

    def __init__(self):
        self.accepted = 0
        self.rejected = 0

    def apply(self, state: F4State) -> bool:
        ok = state.is_valid()
        if ok:
            self.accepted += 1
        else:
            self.rejected += 1
        return ok

    def stats(self):
        return {
            "accepted": self.accepted,
            "rejected": self.rejected
        }
