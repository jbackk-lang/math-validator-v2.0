"""
topology.py — moduł root: deleguje do filters/topology_filter.
Naprawka: oryginalny plik był placeholderem zwracającym {"status": "ok", "message": "placeholder"}.
"""
from core import parse
from filters.topology_filter import run


def check_topology(expr: str) -> dict:
    return run(parse(expr))
