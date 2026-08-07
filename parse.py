# core/parse.py
# Minimalny, stabilny parser zgodny z validator.py i filtrami

class ParsedExpr:
    """
    Prosty kontener na wyrażenie + parametry.
    - expr: oryginalny string równania
    - data: słownik dodatkowych parametrów (Lambda, Tau, Rho, itp.)
    """

    def __init__(self, expr: str, data: dict | None = None):
        self.expr = expr
        self._data = data or {}

    def get(self, key, default=None):
        return self._data.get(key, default)


def _extract_params(expr: str) -> dict:
    """
    Bardzo prosty ekstraktor Λ–τ–ρ z tekstu.
    Format:
      Lambda=1
      Tau=2
      Rho=3

    Jeśli nie ma takich fragmentów — zwraca pusty słownik.
    Dzięki temu tourosomobius_filter ma co czytać,
    ale zwykłe równania dalej działają.
    """
    data = {}
    for name in ("Lambda", "Tau", "Rho"):
        marker = name + "="
        if marker in expr:
            try:
                # np. "Lambda=1 " albo "Lambda=1, Tau=2"
                tail = expr.split(marker, 1)[1]
                value_str = ""
                for ch in tail:
                    if ch in "0123456789.-":
                        value_str += ch
                    else:
                        break
                if value_str:
                    data[name] = float(value_str)
            except Exception:
                # jak coś pójdzie nie tak, po prostu ignorujemy
                pass
    return data


def parse(equation: str) -> ParsedExpr:
    """
    Jedyna funkcja, której używa validator.py.

    Zwraca obiekt:
      parsed.expr  -> oryginalne równanie (string)
      parsed.get() -> dostęp do parametrów (Lambda, Tau, Rho, itd.)

    Dzięki temu:
      - millennium_filter może robić str(parsed.expr)
      - misleading_filter może czytać expr
      - tourosomobius_filter może czytać Lambda/Tau/Rho
      - inne filtry mogą używać parsed.get() jeśli chcą
    """
    expr = equation.strip()
    data = _extract_params(expr)
    return ParsedExpr(expr, data)
