import os
import sys
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app import app  # noqa: E402


def test_health():
    assert app.test_client().get("/health").status_code == 200


def test_create_order_calls_catalog():
    fake = MagicMock(status_code=200)
    fake.json.return_value = {"id": 1, "name": "Wireless Mouse", "price": 10.0}
    with patch("app.requests.get", return_value=fake):
        r = app.test_client().post("/orders", json={"product_id": 1, "quantity": 3})
    assert r.status_code == 201 and r.json["total"] == 30.0


def test_create_order_requires_product():
    assert app.test_client().post("/orders", json={}).status_code == 400
