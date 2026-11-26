import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app import app  # noqa: E402


def test_health():
    r = app.test_client().get("/health")
    assert r.status_code == 200 and r.json["status"] == "ok"


def test_products():
    c = app.test_client()
    assert len(c.get("/catalog/products").json) == 3
    assert c.get("/catalog/products/1").json["name"] == "Mechanical Keyboard"
    assert c.get("/catalog/products/99").status_code == 404
