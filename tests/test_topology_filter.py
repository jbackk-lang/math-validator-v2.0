from validator import validate

def test_topology_circle():
    result = validate("x^2 + y^2 = 1")
    topo = result["topology"]

    assert topo["status"] in ["ok", "skip"]
    assert "notes" in topo


def test_topology_line():
    result = validate("y = 2*x + 1")
    topo = result["topology"]

    assert topo["status"] in ["ok", "skip"]
