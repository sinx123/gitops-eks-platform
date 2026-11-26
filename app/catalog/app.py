import time

from flask import Flask, Response, jsonify, request
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest

SERVICE = "catalog"
app = Flask(__name__)

REQUESTS = Counter(
    "http_requests_total", "Total HTTP requests", ["service", "method", "endpoint", "status"]
)
LATENCY = Histogram(
    "http_request_duration_seconds", "HTTP request latency", ["service", "endpoint"]
)

PRODUCTS = {
    1: {"id": 1, "name": "Mechanical Keyboard", "price": 89.99},
    2: {"id": 2, "name": "Wireless Mouse", "price": 29.5},
    3: {"id": 3, "name": "USB-C Dock", "price": 129.0},
}


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


@app.get("/catalog/products")
def list_products():
    return jsonify(list(PRODUCTS.values()))


@app.get("/catalog/products/<int:product_id>")
def get_product(product_id):
    product = PRODUCTS.get(product_id)
    if not product:
        return jsonify(error="product not found"), 404
    return jsonify(product)
