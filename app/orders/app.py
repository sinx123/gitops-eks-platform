import os
import time
import uuid

import requests
from flask import Flask, Response, jsonify, request
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest

SERVICE = "orders"
CATALOG_URL = os.getenv("CATALOG_URL", "http://catalog")
app = Flask(__name__)

REQUESTS = Counter(
    "http_requests_total", "Total HTTP requests", ["service", "method", "endpoint", "status"]
)
LATENCY = Histogram(
    "http_request_duration_seconds", "HTTP request latency", ["service", "endpoint"]
)

ORDERS = {}  # in-memory store: this is a demo, not a database


@app.before_request
def _start_timer():
    request._start = time.time()


@app.after_request
def _record(resp):
    endpoint = request.url_rule.rule if request.url_rule else "unmatched"
    REQUESTS.labels(SERVICE, request.method, endpoint, resp.status_code).inc()
    LATENCY.labels(SERVICE, endpoint).observe(time.time() - getattr(request, "_start", time.time()))
    return resp


@app.get("/health")
def health():
    return jsonify(status="ok", service=SERVICE)


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


@app.get("/orders")
def list_orders():
    return jsonify(list(ORDERS.values()))


@app.post("/orders")
def create_order():
    body = request.get_json(silent=True) or {}
    product_id = body.get("product_id")
    qty = int(body.get("quantity", 1))
    if product_id is None:
        return jsonify(error="product_id is required"), 400
    try:
        resp = requests.get(f"{CATALOG_URL}/catalog/products/{product_id}", timeout=2)
    except requests.RequestException:
        return jsonify(error="catalog service unavailable"), 503
    if resp.status_code != 200:
        return jsonify(error="unknown product"), 400
    product = resp.json()
    order = {
        "id": str(uuid.uuid4()),
        "product": product["name"],
        "quantity": qty,
        "total": round(product["price"] * qty, 2),
    }
    ORDERS[order["id"]] = order
    return jsonify(order), 201
