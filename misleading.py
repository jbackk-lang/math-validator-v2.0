# misleading.py

import re

class MisleadingDetector:
    """
    Wykrywa problemy mylne:
    - wielokrotne '='
    - łańcuchowe porównania
    - niejednoznaczne konstrukcje
    """

    def is_misleading(self, expression: str) -> bool:
        expr = expression.replace(" ", "")

        # 1. Wielokrotne '=' → np. 1=1=1
        if expr.count("=") > 1:
            return True

        # 2. Łańcuchowe porównania typu a=b=c
        if re.search(r"[a-zA-Z]+\=[a-zA-Z]+\=[a-zA-Z]+", expr):
            return True

        # 3. Konstrukcje typu (a=b=c)
        if re.search(r"\([^\)]*\=[^\)]*\=[^\)]*\)", expr):
            return True

        # 4. Wyrażenia typu 0^0 (niejednoznaczne)
        if "0^0" in expr:
            return True

        # 5. Wyrażenia typu x/x bez kontekstu (może być 0/0)
        if re.fullmatch(r"[a-zA-Z]+/[a-zA-Z]+", expr):
            return True

        return False
