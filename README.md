# math-validator-2.0

Walidator wyrażeń matematycznych oparty na SymPy. Wyrażenie przepuszczane jest
raz przez parser (`core.py`), a następnie przez 12 niezależnych filtrów
analizujących różne aspekty: składnię, algebrę, logikę, rozwiązania numeryczne,
strukturę harmoniczną, "möbiusowość" (inwersje/pętle), topologię (dziedzinę
ciągłości), osobliwości i skręty τ, widmo liczb pierwszych, wyrażenia mylące
oraz powiązania z Problemami Milenijnymi.

Udostępniony jako REST API (FastAPI) z prostym interfejsem webowym zawierającym
edytor + klawiaturę matematyczną (cyfry, operatory, zmienne, funkcje).

**Historia:** ta wersja zastępuje `math-validator` (v1, zarchiwizowane repo) -
v1 było prototypem/szkieletem, w większości zaślepki (`return {"status": "ok",
"details": ...}`) bez realnej logiki. v2.0 to pierwsza w pełni działająca
implementacja tych 12 filtrów. Dalej rozwijana jako `math-validator-3.0`
(dodaje logikę zdaniową, jednostki fizyczne, algebrę liniową, CLI, wtyczki -
zachowując wszystkie filtry v2.0 bez zmian).

> **⚠️ Ta wersja (v2.0) jest legacy.** Aktywnie rozwijana jest
> [`math-validator-3.0`](https://github.com/jbackk-lang/math-validator-3.0) -
> zawiera te same 12 filtrów (bez zmian) PLUS: logikę zdaniową
> (tautologia/CNF/DNF), jednostki fizyczne (SI), algebrę liniową (macierze),
> analizę zmiennych wolnych/związanych, wykrywanie niejednoznaczności zapisu
> (`a/b*c`, `-a^b`), bogatszą diagnostykę błędów, wykrywanie paradoksów w
> sekwencji kroków derywacji, system wtyczek, CLI i bogatszy REST API
> (osobne endpointy per domena, np. `/millennium`, `/api/v3/paradox`,
> `/solve`, `/latex`) - v2.0 ma tylko `GET /validate?expr=`.
>
> To repo dostaje wyłącznie **fixy do 12 wspólnych filtrów** (portowane z
> v3.0, gdy tam coś się naprawi - patrz "Historia poprawek" niżej), NIE nowe
> funkcje v3 - te zostają wyłącznie w v3.0. Jeśli potrzebujesz czegoś z listy
> wyżej, użyj `math-validator-3.0` zamiast tego repo.

---

## Uruchomienie

```
run.bat
```

Skrypt instaluje `fastapi`, `uvicorn`, `sympy` i odpala serwer pod
`http://127.0.0.1:8000`. Interfejs webowy jest pod `/`, samo API pod
`/validate?expr=...`.

Ręcznie:
```
pip install fastapi uvicorn sympy
uvicorn api:app --reload
```

---

## Filtry

| Filtr | Co sprawdza |
|---|---|
| `information` | entropia/redundancja/złożoność zapisu wyrażenia |
| `syntax` | niedomknięte nawiasy, podwójne operatory, urwane operatory |
| `algebra` | dzielenie przez zero (`zoo`), wartości zespolone |
| `logic` | nieskończoności (`oo`, `-oo`), `nan`, `zoo` jako wynik |
| `numeric` | rozwiązania równania `wyrażenie = 0` (rzeczywiste i zespolone) |
| `harmonic` | obecność funkcji trygonometrycznych, okresowość, π |
| `moebius` | inwersje (`**-1`, `**(-1)`), dzielenie, zagnieżdżenia — "gęstość Möbiusa" |
| `topology` | dziedzina ciągłości (czy `is_all_reals`, czy są wykluczone punkty) |
| `singularity` | osobliwości i skręty τ (lim(0⁺) ≠ lim(0⁻)) |
| `prime_spectrum` | dla wyrażeń całkowitych: rozkład liczb pierwszych ≤ N^(1/3) |
| `misleading` | wyrażenia pozornie proste, które ukrywają osobliwość po uproszczeniu (`x/x`, upraszczalne ułamki) |
| `millennium` | dopasowanie słów kluczowych/struktury do 7 Problemów Milenijnych |

**Uwaga o `misleading`:** filtr wykrywa konkretnie trzy przypadki —
`misleading_zero` (upraszcza się do 0, ale ma dzielnik), `simplifiable_fraction`
(ułamek do uproszczenia przez `cancel()`) i `hidden_singularity` (domena po
uproszczeniu różni się od domeny oryginału, np. `x/x`). Nie wykrywa tautologii
tekstowych typu `1=1=1` czy `0^0=1` — to wymagałoby osobnego parsera składni
"=", którego obecnie nie ma (patrz sekcja Ograniczenia).

### Problemy Milenijne rozpoznawane przez `millennium`

| ID | Nazwa | Status |
|---|---|---|
| P_vs_NP | P vs NP | otwarty |
| Riemann | Hipoteza Riemanna | otwarty |
| Birch_Swinnerton_Dyer | Hipoteza Bircha i Swinnertona-Dyera | otwarty |
| Yang_Mills | Yang–Mills i luka masowa | otwarty |
| Navier_Stokes | Równania Naviera–Stokesa | otwarty |
| Poincare | Hipoteza Poincarégo | **rozwiązany** (Perelman, 2003) |
| Hodge | Hipoteza Hodge'a | otwarty |

---

## Kształt odpowiedzi

```json
{
  "filters": {
    "information": {...}, "syntax": {...}, "algebra": {...}, "logic": {...},
    "numeric": {...}, "harmonic": {...}, "moebius": {...}, "topology": {...},
    "singularity": {...}, "prime_spectrum": {...}, "misleading": {...},
    "millennium": {...}
  },
  "stability": { "cycle": 1, "angle": 72, "phase": "UNDEFINED", "orientation": "M_PRIME" }
}
```

Każdy filtr zwraca własny, niezależny słownik — dokładny kształt pól znajdziesz
w danym pliku `filters/*.py` lub w testach (`tests/`), które sprawdzają realne
wartości dla konkretnych wyrażeń.

---

## Ograniczenia

- Równości zapisane jako gołe `x = y` **nie parsują się** — Python traktuje `=`
  jako przypisanie, nie porównanie, więc `sympify()` rzuca `SyntaxError` już na
  starcie (`syntax`/wszystkie filtry zwracają `ok: False`). Trzeba używać
  zapisu bez `=` (samo wyrażenie) albo jawnie `Eq(lewa, prawa)`.
- `misleading` nie łapie tautologii tekstowych (`1=1=1`) z tego samego powodu.
- `millennium` to dopasowanie po słowach kluczowych/strukturze symbolicznej —
  nie jest to dowód matematyczny ani ocena poprawności rozwiązania.

---

## Testy

```
pytest tests/ -q
```

43 testów, wszystkie sprawdzają realny kształt odpowiedzi `validate()`
(`result["filters"][...]`) na konkretnych wyrażeniach — nie mocki.

---

## Historia poprawek (ten pakiet)

- **Rekalibrowano `prime_spectrum_filter.py`** (ta sesja) — repo miało
  jeszcze ORYGINALNĄ, nigdy nie naprawioną wersję tego filtra (sztywny
  próg 0.25 na ad hoc metryce, bez modelu zerowego, z niepopartym
  twierdzeniem "widmo zgodne z logarytmiczną spiralą / 1/f
  (Λ–τ–ρ/TIMDR)"). `math-validator-3.0` przeszedł tymczasem DWIE
  niezależne naprawy tego samego pliku, których to repo nigdy nie
  dostało (duplication-drift). Sportowano obie naraz: (1) model zerowy
  z losowych ciągów zamiast stałej 0.25, (2) rekalibracja na
  właściwy, ugruntowany w analitycznej teorii liczb model Cramera/
  Gallaghera (znormalizowana luka gap/log(p) ~ Exp(1) asymptotycznie).
  Wynik na 78498 prawdziwych pierwszych do 10^6: średnia=1.0017
  (zgodna z modelem), korelacja sąsiednich luk r=-0.0568, p≈4.4e-57
  (mała, ale realna struktura wykraczająca poza sam model Cramera —
  znany w literaturze efekt, NIE potwierdzony związek z TIMDR).
  Etykieta "log_spiral_1_over_f" i twierdzenie o TIMDR Λ–τ–ρ usunięte
  całkowicie. Filtr teraz uczciwie odmawia klasyfikacji przy <30
  lukach zamiast zgadywać (przez ograniczenie do pierwszych ≤N^(1/3)
  sensowna statystyka wymaga N ≥ ok. 2 048 383). Testy: 37 → 43.
- **Naprawiono crash** `information_filter.py`: `p.original` → `p.raw`
  (`ParsedExpr` nie ma pola `original`; każde poprawne wyrażenie crashowało API).
- **Naprawiono `millennium_filter`**: usunięto martwy import
  `from sympy import Laplacian` (nie istnieje w top-level sympy, cicho wyłączał
  całą detekcję przez `try/except`) i dopięto filtr do `validator.py` — wcześniej
  w ogóle nie był wołany mimo że był w pełni zaimplementowany.
- **Naprawiono `moebius_filter`**: `inversion` było `False` dla `x**(-1)` (regex
  łapał tylko dosłowne `**-1` bez nawiasu). Rozszerzono na `**-1`, `**(-1)`, `** -1`.
- **Naprawiono 35/35 testów** — wszystkie odwoływały się do `result["nazwa"]`
  zamiast `result["filters"]["nazwa"]`, plus kilkanaście głębszych niezgodności
  kluczy (np. `syntax`/`logic` nie mają `"status"`, tylko `"ok"`) — przepisane na
  realne zachowanie filtrów, zweryfikowane bezpośrednio na `validate()`.
- Dodano klawiaturę matematyczną w UI (`api.py`): cyfry, operatory, nawiasy,
  zmienne/stałe (x, y, z, e, ∞, Λ, τ, ρ), funkcje (sin, cos, tan, log, exp, abs).
- **Przycięto paczkę** do plików faktycznie używanych przez `validator.py` /
  `api.py` (12 filtrów + `core.py` + testy). Usunięto ~15 nieużywanych,
  niepodpiętych nigdzie skryptów (m.in. `entropy_flow.py`,
  `mini‑structure‑validator.py`, `topology.py`, `parser.py`, `app.py`) oraz
  nieużywany 824 KB plik graficzny — w tym plik z nazwą zawierającą niestandardowy
  znak `‑` (U+2011, nie zwykły myślnik), który najpewniej blokował rozpakowywanie
  archiwum w Eksploratorze Windows.

---

## Licencja

MIT — patrz `LICENSE`.
